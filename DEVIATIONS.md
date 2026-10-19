# Deviation and disclosure log (post-lock)

Locked: GitHub release `v1.0-lock`, commit 4eb084fb2c462fffec72574f108043ea9d796cc9, 19 Oct 2026 14:55 UTC, DOI 10.5281/zenodo.23477871.
Nothing in the locked release has been edited. Every entry below was added afterwards and says whether results had been seen.
The full audit log (Entries 1–26) is in `protocol_post_lock/protocol_v2.3_audit_log_to_entry26.pdf`.

| Entry | Date (2026) | What | Results seen? |
|---|---|---|---|
| 21 | 19 Oct | Lock recorded. The tag-commit files (`MANIFEST.txt`, `phase2.py`, protocol) were re-downloaded and their SHA-256 hashes match the bundle. The bundle zip named in the v1.0 release notes was not attached, but its 42 files are committed individually and hashed in `MANIFEST.txt`. | No |
| 22 | 19 Oct | Phase 2 run once in real mode with the locked `phase2.py` (SHA-256 da697030…), 15:00:47–15:01:25 UTC, exit code 0, no deviations. `results/results.json` SHA-256 9e4239dd116eaea7c9f65df83f85d349f338aeb4adb6ff16904a6793ed6fa99c. | Yes (this is the run) |
| 23 | 19 Oct | S5 recorded as "not supported". The protocol did not define support for S5 and the results were mixed. This is the conservative reading, chosen after results were seen. | Yes |
| 24 | 19 Oct | The §13 figures were drawn from the locked outputs by `code_post_lock/figures.py` (no new estimation). The fitted line in Fig. 6 is for display only. The k_o lag is constant at 2, so it is stated in the text rather than drawn. | Yes |
| 25 | 19 Oct | An independent agent, which had not seen the drafting, checked 77 claims in the manuscript: 63 OK, 9 wrong, 2 rounding, 3 unverifiable. Every estimate matched the locked outputs. The errors were descriptive (mainly about the 2008 episode) and have been corrected. See `checks/verification_report.md`. | Yes |
| 26 | 19 Oct | External feedback on the manuscript was adopted with corrections. Discussion of Keen's theory was moved to §6.1, "Discussion beyond the pre-registered map", and worded in terms of intervals. The extensions are flagged as each needing its own preregistration. References were verified against publisher or RePEc records. | Yes |

No analysis code, specification, sample or decision rule was changed after lock.
