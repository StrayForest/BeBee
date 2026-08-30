# P8 release-candidate research

## Question

How should BeBee close a small HTML5 release candidate around the selected Poki distribution target while keeping direct web deterministic, optional telemetry private, and the current authored visual language coherent?

## Shipped reference pool

- A Short Hike — compact authored routes and landmarks; selected for orientation language.
- Alba: A Wildlife Adventure — habitat distinction through approachable local objectives; selected for natural identity.
- Mini Metro — readable interaction under small-screen pressure; rejected as a structural UI model for BeBee.
- Alto's Odyssey — silhouette and motion readability; rejected as a tonal and interaction model because its endless-runner loop differs.
- Spiritfarer — management-heavy counter-model; rejected to avoid scope expansion.

## Observations and inferences

A Short Hike supports named local places and landmark-led traversal in a compact authored world. The inference for BeBee is to preserve authored region names, world-space objectives and continuous movement rather than add a map or management layer.

Alba supports differentiating habitats with visual context and gentle objectives. The inference for BeBee is to preserve distinct flowers, regional palettes and redundant state cues while keeping movement-through pollination as the only restoration verb.

Spiritfarer is the anti-pattern: its broader management surfaces are valuable for a different product but would make this small release candidate harder to read, validate and run.

## Official technical constraints used

- Poki quality guidance requires lifecycle signals at first input and interruption, with no duplicate signals.
- The Defold Poki extension supplies the pinned 4.0.0 integration surface; the adapter keeps SDK availability optional for direct web.
- CrazyGames remains a secondary safe adapter, not a gameplay dependency.
- Defold HTML5 uses wasm and browser-backed asynchronous persistence; the release check therefore measures startup and runs a negative release-bridge probe.
- Defold application lifecycle and size guidance make interruption handling and fixed bundle budgets part of the candidate contract.

Sources: https://developers.poki.com/guide/requirements-quality; https://defold.com/extension-poki-sdk/; https://defold.com/extension-crazygames/crazygames_api/; https://defold.com/manuals/html5/; https://defold.com/manuals/application-lifecycle/; https://defold.com/manuals/optimize-size/.

The QA diagnostic boundary treats requests and browser warnings whose endpoint is an identified Poki/CrazyGames platform SDK as platform traffic, not as BeBee application traffic. Unknown external requests and all game/runtime errors remain blocking. A transient Defold extender failure is infrastructure noise only when the build is retried and the retained exact-head run passes.

## Selected implementation

Use an adapter-bound Poki lifecycle with direct-web fallback, deny-by-default optional telemetry, a repository privacy policy, pinned dependency/license metadata, exact-head browser/storage evidence and a machine-checked negative release surface. Certify current code-native art for this scoped candidate with measured V-001 constraints; schedule broader market-art refinement separately.
