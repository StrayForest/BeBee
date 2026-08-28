# 16 — CI Trust Boundary & Human Gates

## 1. Purpose

BeBee's evidence rules are useful only if a pull request cannot rewrite the validator that judges the same pull request.

The repository therefore separates:

```text
trusted policy from the PR base/default branch
                    ↓
candidate PR checkout used as data
                    ↓
diff / manifest / evidence validation
```

The candidate may change policy files, but those changes do not become the authority until after they have passed the previous trusted policy and merged.

## 2. Trusted workflow model

The required `PR evidence` workflow uses `pull_request_target`, whose workflow context comes from the base/default branch.

Security rules:

- workflow permissions are read-only;
- `actions/checkout` is pinned to a full commit SHA;
- the base commit is checked out into `trusted/`;
- the exact PR head is checked out separately into `candidate/`;
- no candidate runtime/build/test code is executed by the trusted workflow;
- validators/tests executed as policy come only from `trusted/`;
- candidate files, manifests and git diff are inspected from `candidate/`.

This closes the self-modifying-validator bypass where a PR changes `check_pr_evidence*.py` and its own tests to always pass.

## 3. Governance-critical paths

The trust-boundary validator treats at least these as governance-critical:

- `.github/workflows/**`;
- `.github/CODEOWNERS`;
- `.github/PULL_REQUEST_TEMPLATE.md`;
- `AGENTS.md`;
- `DECISIONS.md`;
- evidence-governance/workflow hardening docs;
- `scripts/check_pr_evidence.py`;
- `scripts/check_pr_evidence_policy.py`;
- `scripts/check_trust_boundary.py`;
- `scripts/policy_tests/**`.

A governance-critical PR must:

1. use `Change class: process`;
2. change `evidence/<ticket>/manifest.json` in the same PR;
3. record `governance.trust_boundary_change`, `governance.bypass_analysis`, `governance.rollback` and `governance.human_review_required = true`;
4. receive an exact-head independent GitHub approval once the trusted-base gate is active.

## 4. Exact-head human approval

Human approval is not represented by prose or by an agent-created file.

For P2, P4, P6 and governance-critical policy changes, the trusted workflow checks GitHub review data.

A qualifying approval must be:

- `APPROVED`;
- attached to the exact current PR head commit;
- from a reviewer different from the PR author;
- from a non-bot account.

An approval attached to an older commit does not count.

This means a solo-author PR cannot self-approve a human gate. A designated second human GitHub identity/collaborator is required for these gates.

## 5. Diff-classification additions

The additional trust-boundary policy intentionally fails closed for previously ambiguous runtime/content files.

Examples:

- `data/flowers*`, `data/regions*`, `data/meadows*` are player-facing content, not generic technical changes;
- an otherwise unclassified `.lua` or `.script` runtime file requires at least technical evidence;
- governance files cannot be downgraded into an ordinary process PR without governance evidence.

As the production source tree grows, adversarial classification tests must grow with it.

## 6. Reference identity

URL uniqueness is insufficient evidence diversity.

Player-facing/economy manifests therefore identify shipped references with `product_id`.

Five different pages for one game are still one product. Candidate and deep-reference sets must use distinct product identities when the required count applies.

## 7. Official-document parsing

PR template fields are parsed line-by-line.

A blank field such as:

```text
If official-doc research is not applicable, explain why:
```

cannot consume text from the next paragraph and pretend to be filled.

## 8. Remaining repository-setting requirement

The active `Protect main` ruleset already requires PRs, blocks non-fast-forward changes and requires `validate-pr-evidence`.

However, the required-status-check policy must also require branches to be up to date before merging.

Until GitHub reports strict required status checks enabled, a stale green PR can theoretically merge after `main` changed without being revalidated against the new base.

This setting cannot be corrected by repository code. Issue #4 remains the settings-level P-1 blocker until strict/up-to-date enforcement is active and verified.

## 9. Bootstrap note

The migration PR that introduces this trust boundary is necessarily judged by the previous policy.

After this change lands in `main`, subsequent governance-critical PRs are judged by the trusted-base version and require the exact-head independent human gate described above.
