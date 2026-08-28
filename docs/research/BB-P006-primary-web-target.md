# BB-P006 — Primary web distribution target

Research snapshot: **2026-08-28**.

Decision: **Poki is the primary external validation/distribution target. CrazyGames is the secondary/fallback portal. Direct web remains the owned development/QA target and optional distribution channel.**

This is a platform decision, not an exclusivity decision. BeBee must keep portal SDKs behind adapters so the target can change without gameplay-domain rewrites.

## Problem

P-1 must select one portal early enough that onboarding, aspect ratio, storage, loading budgets and SDK lifecycle can be tested against concrete requirements rather than a generic idea of “HTML5”. The selected target should also improve the project's evidence loop by making real-player validation feasible.

## Candidates

### Direct web

Strengths:

- complete hosting/UI/network control;
- standard Defold HTML5 bundle with no portal SDK dependency;
- best environment for CI/dev builds and deterministic browser automation.

Constraints:

- no built-in audience or portal playtest funnel;
- local browser persistence is origin-specific/best-effort unless BeBee adds its own account/backend;
- acquisition, cloud save, analytics/privacy and monetization would be BeBee's responsibility.

Role selected: **development/QA and optional owned distribution**, not the primary external validation target.

### Poki

Current official requirements include:

- desktop, mobile and tablet support;
- responsive **16:9** canvas;
- incognito playability;
- external requests blocked by default unless approved;
- minimal onboarding, ideally direct-to-gameplay;
- correct SDK lifecycle events, including `gameplayStart()` on the player's first input;
- small/progressively loaded builds; Poki's current engine guidance recommends targeting roughly **<=5 MB initial and <=8 MB total** for a good web game rather than treating those figures as hard publication limits.

Poki's account system automatically syncs monitored `localStorage`/IndexedDB game-save data for logged-in users, with a current **1 MB gzip cloud-gamesave limit**.

Most importantly for BeBee's development method, Poki supports early prototype uploads and a staged testing flow. Its current documentation describes playtests that return **10 gameplay recordings**, followed by a player-fit test with **500 players** before later web-fit/release stages.

Defold fit is unusually strong:

- Poki's engine guide calls Defold an official partner and describes it as well suited to desktop/mobile web;
- Defold maintains an official `extension-poki-sdk`;
- Defold includes a Poki HTML5 game template and the extension supports a Poki-specific build/Inspector path.

Risks:

- platform access is curated and must be obtained through Poki for Developers;
- external networking/analytics are intentionally restricted and require approval;
- the aggressive loading target will constrain asset production early.

For BeBee these restrictions are mostly beneficial at the vertical-slice stage: there is no required backend/multiplayer, analytics are already behind an adapter, and the project wants a small mobile-capable 2D build.

### CrazyGames

Current official requirements/process include:

- Basic Launch may ship without SDK integration and has monetization disabled;
- current hard limits include **<=50 MB initial**, **<=250 MB total**, and **<=1500 files**; **<=20 MB initial** is required for mobile-homepage eligibility;
- Full Implementation should land new users directly in gameplay or require at most one click;
- current Data-module cloud save limit is **1 MB**; guest data falls back to local storage and can sync after login;
- Basic Launch evaluates live KPIs over at least 7 days / 500 plays, with a maximum 21-day test period when 500 plays are not reached;
- current guidance says top-performing Basic Launch titles commonly load in under 10 seconds and stay below 20 MB.

Defold also maintains an official CrazyGames extension with game/ad/user/data modules and a QA tool integration.

CrazyGames is therefore a strong target, and it is selected as the **fallback/secondary portal**. Compared with Poki, however, its published early validation loop is more KPI-oriented, while Poki explicitly supplies gameplay recordings during playtesting. For a repository whose development process depends on visual/behavioral evidence, the recording-based early loop is the stronger first fit.

## Decision matrix

| Criterion | Direct web | Poki | CrazyGames |
|---|---|---|---|
| Official Defold HTML5 path | Strong | Strong + Poki-specific extension/template | Strong + official extension |
| Concrete mobile requirement | Self-imposed | Hard desktop/mobile/tablet requirement | Mobile supported; mobile-homepage constraints apply |
| Early real-player validation supplied by platform | None | Strong: recorded playtests + staged fit testing | Strong: Basic Launch KPI test |
| Direct observational evidence for UX iteration | Must build/recruit | Strongest of the three | More KPI-centric in public docs |
| Save without BeBee backend | Local browser only | Local + transparent cloud sync for logged-in users | Local + Data/APS cloud options |
| External-network freedom | Highest | Lowest; blocked by default | Portal rules/SDK constraints |
| Loading pressure | Self-imposed | Most aggressive guidance | Larger hard ceilings; <20 MB recommended for strong conversion |
| Fits no-backend vertical slice | Yes | Yes | Yes |
| Supports future multi-portal adapter strategy | N/A | Yes | Yes |

## Selected approach

### Primary: Poki

Use Poki requirements as the **strictest baseline profile** during P0–P6 where they do not conflict with BeBee product rules:

- 16:9 responsive gameplay baseline;
- desktop + mobile + tablet from the start;
- no required external runtime dependencies;
- direct/near-direct first-session entry;
- aggressive progressive loading and bundle budget;
- private/incognito-safe local play;
- platform lifecycle/ads/accounts only through an adapter.

This gives BeBee a narrow, measurable web target while preserving portability.

### Fallback: CrazyGames

If Poki developer access or external playtesting is unavailable when BeBee reaches its first portal audience test, switch the **external validation target** to CrazyGames. This is not a product redesign. The shared baseline intentionally satisfies the major overlapping requirements, and the CrazyGames SDK remains a separate adapter.

### Direct web

Direct web remains mandatory for:

- local development;
- CI/browser smoke tests;
- deterministic visual capture;
- sharing internal builds;
- an optional owned public build later.

It is not selected as the first distribution-validation target because it does not itself solve player acquisition/testing.

## Platform architecture consequences

P0 must implement a platform boundary roughly equivalent to:

```text
platform
  init()
  gameplay_start()
  gameplay_stop()
  loading_start()/loading_stop()
  request_commercial_break()
  request_rewarded_break()
  get_user_if_available()

storage
  load()
  save()
  flush()/durability signal where possible
```

Expected adapters:

```text
platform_direct
platform_poki
platform_crazygames

storage_local
storage_poki-compatible / platform-assisted path
storage_crazygames data/APS path where selected
```

Gameplay code must not call either portal SDK directly.

## Initial budgets for P0/P6

These are engineering targets, not invented portal hard requirements:

- first playable payload target: **<=5 MB compressed** where feasible;
- total vertical-slice payload target: **<=8 MB compressed** before evidence proves a justified exception;
- first input/playable target: **<10 seconds on representative constrained web connection**, with progressive loading preferred;
- 16:9 baseline plus representative mobile/tablet scaling;
- serialized BeBee save remains well below Defold's existing ~512 KB `sys.save()` limit and therefore also below current 1 MB portal cloud-save ceilings.

The 5/8 MB target deliberately adopts Poki's stronger current web-engine guidance. It should be treated as a performance budget and measured in CI once P0 has a bundle.

## Evidence sources

Poki official/current:

- https://developers.poki.com/guide/requirements-quality
- https://developers.poki.com/guide/easy-access
- https://developers.poki.com/guide/how-testing-works
- https://developers.poki.com/guide/web-engine
- https://developers.poki.com/guide/accounts
- https://developers.poki.com/guide/external-resources-policy
- https://developers.poki.com/guide/sdk-overview

CrazyGames official/current:

- https://docs.crazygames.com/requirements/intro/
- https://docs.crazygames.com/requirements/technical/
- https://docs.crazygames.com/requirements/gameplay/
- https://docs.crazygames.com/resources/basic-launch-metrics/
- https://docs.crazygames.com/sdk/data/
- https://docs.crazygames.com/requirements/account-integration/

Defold official/current:

- https://defold.com/manuals/html5/
- https://defold.com/manuals/automated-testing/
- https://defold.com/extension-crazygames/
- https://github.com/defold/extension-poki-sdk

Browser storage reference:

- https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria

## Validation status

The target selection is sufficiently supported to change `P-001` from `OPEN` to `VALIDATED`:

- it is based on current platform requirements and current Defold integrations;
- it does not lock BeBee into portal-specific gameplay architecture;
- it includes an explicit fallback condition;
- it creates stricter measurable P0 budgets rather than weakening quality requirements.

It remains `VALIDATED`, not `LOCKED`, because portal policy, access and product-market fit can change. A later switch to CrazyGames or another portal should be evidence-driven and should not require gameplay-domain changes.
