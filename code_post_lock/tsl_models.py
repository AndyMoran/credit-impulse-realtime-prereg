"""
Timestral extension: the model back-end (plan: timestral/PLAN.md, Section 2).

Timestral-209M (Mistral AI), used as published: no fine-tuning, the package's default forecast settings
(symmetric averaging on, non-negative clipping on; clipping never applies here because every GDP context
contains negative values). The package is `timestral` 1.0.0 (Apache-2.0) at commit a534bdbd; the weights are
under Mistral's Modified MIT licence and are downloaded from Hugging Face, never committed.

The back-end returns the same structure as the TimesFM back-ends in tfm_models.py, so the locked TimesFM
statistics (compare, premium, L1, L2) are reused unchanged. For each input series, a dict:
  point : array (5,)    median forecast for steps 1..5 (step 5 = target o+4)
  q     : array (5, 9)  quantiles 0.1, 0.2, ..., 0.9
Each series is forecast in its own call (batch of one), because the contexts differ in length; no padding
is added by this code.
"""
import numpy as np

STEPS = 5
DECILES = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
REPO = 'mistralai/Timestral-209M'
REVISION = '9874d252ab0aae16f7f7c999f98f98d6ad7d8365'
WEIGHTS_SHA256 = '1456effb9927e3daa8c7234f10497e3424233869245a9c72b8ecebaf7ad2b7fa'
PACKAGE_COMMIT = 'a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff'


class Timestral:
    """Timestral, as published. `forecaster` may be injected (tests use a small random-weights model)."""
    name = 'timestral209m'

    def __init__(self, revision=REVISION, forecaster=None):
        import torch  # noqa: F401
        if forecaster is None:
            from timestral import TimestralForecaster
            forecaster = TimestralForecaster.from_pretrained(REPO, revision=revision, device='cpu')
        self.fc = forecaster
        levels = tuple(round(float(x), 6) for x in self.fc.quantile_levels)
        missing = [d for d in DECILES if d not in levels]
        if missing: raise ValueError(f'Timestral quantile levels {levels} lack {missing}')
        self.idx = [levels.index(d) for d in DECILES]

    def _pack(self, fc_out):
        q = fc_out.quantiles.detach().cpu().numpy()            # (1, 1, H, Q)
        if q.shape[:3] != (1, 1, STEPS):
            raise ValueError(f'unexpected Timestral output shape {q.shape} (expected (1, 1, {STEPS}, Q))')
        q = q[0, 0].astype(float)                               # (5, Q)
        med = fc_out.median.detach().cpu().numpy()[0, 0].astype(float)
        dec = q[:, self.idx]
        if not np.allclose(med, dec[:, 4]): raise ValueError('median differs from the 0.5 quantile')
        return dict(point=med, q=dec)

    def forecast(self, inputs):
        """GDP only. inputs: list of 1-D arrays (contexts ending at o-1)."""
        return [self._pack(self.fc.forecast(np.asarray(y, np.float32)[None, None, :], prediction_length=STEPS))
                for y in inputs]

    def forecast_past_cov(self, inputs, covs):
        """Credit as one past-only covariate, aligned by Rule B (tfm_data.credit_aligned): position t holds
        CI(t-1), so the covariate ends where GDP ends and holds nothing published after the origin."""
        out = []
        for y, c in zip(inputs, covs):
            y = np.asarray(y, np.float32); c = np.asarray(c, np.float32)
            if c.shape != y.shape: raise ValueError('covariate must cover exactly the GDP context')
            out.append(self._pack(self.fc.forecast(y[None, None, :], prediction_length=STEPS,
                                                   past_covariates=c[None, None, :])))
        return out


def get(name, **kw):
    if name == 'timestral': return Timestral(**kw)
    if name == 'dummy':
        import tfm_models
        return tfm_models.Dummy()
    raise ValueError(name)
