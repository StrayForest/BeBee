# P8 release capture set

The release candidate capture set is produced by the exact-source HTML5 CI workflow and is not committed as generated binary output.

Required evidence:

- Chromium desktop reference: 1280x720;
- responsive portal sizes: 1031x580, 836x470 and 640x360;
- mobile landscape: 844x390;
- movement empty/dense motion evidence;
- Moon Garden start, mid, complete and settled reload states;
- release-negative checks prove the development QA bridges are absent from the release bundle.

Artifact names are SHA-bound (visual-qa-head, movement-qa-head, storage-qa-head, html5-playable-head, html5-ci-evidence-head). Retain the exact head, browser version, screenshot hashes and zero-error diagnostics in the evidence manifest.
