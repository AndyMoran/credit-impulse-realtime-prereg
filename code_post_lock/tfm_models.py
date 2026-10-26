"""
TimesFM extension: model back-ends (plan: timesfm/PLAN.md, Section 2).

Public back-ends (this file may be published under the repository's MIT licence):
  - 'dummy'  : an iterated AR(2) used only to test the pipeline. It is not TimesFM and is never reported.
  - 'tfm25'  : TimesFM 2.5 (200M, Apache-2.0 weights), univariate and with credit through XReg.
TimesFM 3.0 lives in tfm30_private.py, which is not published (plan Section 2, licence handling).

Every back-end returns, for each input series, a dict:
  point : array (5,)    median forecast for steps 1..5 (step 5 = target o+4)
  q     : array (5, 9)  quantiles 0.1, 0.2, ..., 0.9
"""
import numpy as np

STEPS = 5
QUANTILES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
MAX_CONTEXT = 256        # covers 1965Q1 to 2018Q3 (215 quarters); multiple of the 32-step input patch
MAX_HORIZON = 128        # compile-time maximum; only 5 steps are requested and scored
XREG_MODE = 'xreg + timesfm'   # package default: linear credit fit first, TimesFM on the residuals


class Dummy:
    """Pipeline test only: iterated AR(2) by OLS on the context; quantiles from residual quantiles."""
    name = 'dummy'

    def _one(self, y):
        y = np.asarray(y, float); X = np.column_stack([np.ones(len(y) - 2), y[1:-1], y[:-2]])
        b, *_ = np.linalg.lstsq(X, y[2:], rcond=None); r = y[2:] - X @ b
        hist = list(y[-2:]); pts = []
        for _ in range(STEPS):
            f = b[0] + b[1] * hist[-1] + b[2] * hist[-2]; pts.append(f); hist.append(f)
        pts = np.array(pts); qs = np.quantile(r, QUANTILES) - np.median(r)
        return dict(point=pts, q=pts[:, None] + qs[None, :] * np.sqrt(np.arange(1, STEPS + 1))[:, None])

    def forecast(self, inputs):
        return [self._one(y) for y in inputs]

    def forecast_past_cov(self, inputs, covs):
        return self.forecast(inputs)            # stand-in: ignores the covariate; tests plumbing only

    def forecast_xreg(self, inputs, lag_covs):
        out = []
        for y, C in zip(inputs, lag_covs):
            n = len(y); base = self._one(y)
            Xtr = np.column_stack([np.ones(n), C[:, :n].T]); b, *_ = np.linalg.lstsq(Xtr, np.asarray(y), rcond=None)
            adj = np.column_stack([np.ones(STEPS), C[:, n:].T]) @ b - np.mean(Xtr @ b)
            out.append(dict(point=base['point'] + adj, q=base['q'] + adj[:, None]))
        return out


class TFM25:
    """TimesFM 2.5, used as published: no fine-tuning, package normalisation, settings fixed below."""
    name = 'tfm25'
    REPO = 'google/timesfm-2.5-200m-pytorch'

    def __init__(self, revision=None):
        import timesfm, torch  # noqa: F401
        self.timesfm = timesfm
        self.model = timesfm.TimesFM_2p5_200M_torch.from_pretrained(self.REPO, revision=revision)
        self.model.compile(timesfm.ForecastConfig(
            max_context=MAX_CONTEXT, max_horizon=MAX_HORIZON,
            normalize_inputs=True,
            use_continuous_quantile_head=True,
            force_flip_invariance=True,
            infer_is_positive=False,          # GDP growth can be negative
            fix_quantile_crossing=True,
            return_backcast=True,             # required by XReg
        ))

    @staticmethod
    def _pack(point, quant):
        point = np.asarray(point); quant = np.asarray(quant)
        # TimesFM 2.5 returns 10 outputs per step: index 0 = mean, 1..9 = quantiles 0.1..0.9.
        return dict(point=point[:STEPS].astype(float), q=quant[:STEPS, 1:10].astype(float))

    def forecast(self, inputs):
        point, quant = self.model.forecast(horizon=STEPS, inputs=[np.asarray(y, float) for y in inputs])
        return [self._pack(p, q) for p, q in zip(point, quant)]

    def forecast_xreg(self, inputs, lag_covs):
        """Credit enters through XReg as four dynamic covariates (lags 6-9 of the impulse relative to each
        position). Every value, including those over the horizon, was published by the origin."""
        dyn = {f'ci_lag{j}': [np.asarray(C[j], float) for C in lag_covs] for j in range(lag_covs[0].shape[0])}
        res = self.model.forecast_with_covariates(
            inputs=[np.asarray(y, float) for y in inputs],
            dynamic_numerical_covariates=dyn,
            xreg_mode=XREG_MODE, normalize_xreg_target_per_input=True, ridge=0.0)
        point, quant = res[0], res[1]
        return [self._pack(p, q) for p, q in zip(point, quant)]


def get(name, **kw):
    if name == 'dummy': return Dummy()
    if name == 'tfm25': return TFM25(**kw)
    if name == 'tfm30':
        from tfm30_private import TFM30            # private file, not published
        return TFM30(**kw)
    raise ValueError(name)
