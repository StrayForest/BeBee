# 16 — CI Trust Boundary & Autonomous Gates

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

The normal development path is fully autonomous. No second GitHub account, human reviewer, milestone approver, or manual approval is required by CI or the development process. Human review is optional and may be requested by the owner, but it is never a blocking dependency.

## 2. Trusted workflow model

The required evidence workflow uses `pull_request_target`, whose workflow context comes from the base/default branch.

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
3. record `governance.trust_boundary_change`, `governance.bypass_analysis` and `governance.rollback`;
4. pass the previous trusted-base policy and its adversarial test suite.

No reviewer identity is required. The owner may request a human review for a specific change if desired, but CI and milestone progression must not depend on it.

## 4. Milestone evaluation

P2, P4 and P6 remain stronger product checkpoints, but they are evidence gates rather than human gates.

A milestone package should include:

- runnable build/artifact;
- representative screenshots/video;
- objective measurements;
- completed comparison scorecard;
- acceptance-criteria evidence;
- separate evaluator findings;
- explicit known deviations.

`ITERATE` blocks progress. Human review does not.

This preserves the goal of preventing an implementation pass from merely declaring its own work good enough while keeping the entire development loop executable by agents.

## 5. Diff-classification additions

The trust-boundary policy intentionally fails closed for previously ambiguous runtime/content files.

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

## 8. Repository protection after migration — VERIFIED

The permanent target configuration for `Protect main` is:

- pull requests required;
- required approvals: `0`;
- code-owner approval not required;
- non-fast-forward changes blocked;
- deletion blocked;
- `validate-pr-evidence` required;
- branches required to be up to date before merge (`strict` / up-to-date enabled);
- bypass actors: none.

This target is no longer a pending migration instruction. On 2026-08-28, GitHub ruleset `21741136` reported:

- `enforcement=active`;
- target `~DEFAULT_BRANCH`;
- a `pull_request` rule with `required_approving_review_count=0` and no required reviewers;
- required status context `validate-pr-evidence`;
- `strict_required_status_checks_policy=true`;
- deletion and non-fast-forward rules enabled;
- `bypass_actors=[]`;
- `current_user_can_bypass=never`.

The exact observed fields are retained in `evidence/BB-P017-RULESET-CLOSEOUT/ruleset-snapshot.json`. Issue #4 is closed as completed.

This satisfies `R-010`, `R-019` and the repository-enforcement portion of the P-1 exit gate while preserving `R-020`: the normal autonomous merge path has no mandatory human approval.

Ruleset state is external repository configuration and can change independently of git history. Any future audit must re-read the live ruleset; if strict enforcement or the required context disappears, reopen a blocker rather than relying on this historical snapshot.

## 9. Bootstrap cleanup

The previous candidate-controlled `pull_request` bootstrap workflow has been removed from the final design.

Only `.github/workflows/pr-evidence-trusted.yml` should publish the permanent required `validate-pr-evidence` context. This avoids duplicate-context ambiguity and prevents a candidate-controlled workflow from becoming an alternate authority.
