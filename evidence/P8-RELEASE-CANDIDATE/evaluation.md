# P8 Release Candidate — independent evaluation

Evaluation mode: independent_pass.

Input boundary:
- exact candidate head: $PR_HEAD;
- release checker, browser smoke, storage negative check and retained HTML5 artifacts;
- P8 manifest, official platform constraints, alternatives, measurements and visual certification.

Verdict: PASS.

Findings:
- no functional ITERATE finding remains;
- portal lifecycle is adapter-bound and idempotent;
- optional telemetry is denied by default and the release negative check covers all known development bridges;
- bundle, wasm and startup budgets are machine-checked;
- the code-native illustrative direction is explicitly accepted for this scoped release candidate with the numeric V-001 constraints recorded in the manifest.

Scope note: external Poki Inspector upload/player-fit, advertising configuration and portal account operations remain launch operations after the repository candidate. This is explicit and does not alter the in-repository PASS verdict.

Provenance: evaluator=p8-release-candidate-independent-evaluator-2026-08-30; implementation_author=p8-release-candidate-implementation-agent; evaluator identity differs from implementation identity.
