# BB-P008 evidence package

Primary evidence: `manifest.json`.

Supporting sources:

- `config/visual-qa.json` — machine-readable runtime/capture contract;
- `docs/18-deterministic-visual-qa.md` — human-readable implementation specification;
- `docs/research/BB-P008-deterministic-visual-qa.md` — current official-doc research and alternatives;
- `tools/visual_qa/check_visual_qa_plan.py` — static contract validator;
- `tools/visual_qa/test_visual_qa_plan.py` — adversarial invariant tests.

This task validates the **design contract** only. Real Defold HTML5 capture is a P0/BB-006 implementation requirement and is not claimed here.
