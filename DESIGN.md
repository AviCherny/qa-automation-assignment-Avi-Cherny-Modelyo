# Design Rationale

## Language and Framework Choice

**Python + Playwright + pytest.**

Python was chosen for readability and speed — the test intent reads like plain English, which matters in a team where developers also review tests. pytest's fixture model handles setup/teardown with zero boilerplate.

Playwright over Selenium because Playwright ships with auto-waits built into every action and assertion. There is no `WebDriverWait(driver, 10).until(...)` noise; the framework waits for the element to be actionable before clicking. This eliminates an entire class of race-condition flakiness by default. Selenium remains the right choice when you need to test on IE11, a legacy corporate environment, or an in-house Selenium Grid that is already funded and maintained — otherwise Playwright wins on reliability and developer experience.

## Anti-Flakiness Strategy

Concrete techniques used:

- **No `time.sleep`** anywhere in the codebase. Every pause is condition-based.
- **Playwright auto-waits** handle element readiness before every `click`, `fill`, and `select_option`.
- **`expect()` assertions** (Playwright's built-in retry-assertion) poll until the condition is true or the timeout is reached, rather than asserting a snapshot at a single instant.
- **`data-test` attributes only** for locators. Swag Labs exposes them on every interactive element. These are stable across CSS refactors and layout changes.
- **Isolated browser context per test** — each test gets a fresh context and page, so no authentication state or localStorage bleeds between tests.

At scale (1000+ tests): introduce test sharding across multiple CI runners, a flakiness detection pipeline (auto-retry on failure + flag tests that fail intermittently), and a dedicated test stability dashboard. Replace Allure with a persistent test-results database to track flakiness rates over time.

## Parallelism and Isolation

Tests are isolated because:

- Each UI test opens its own `browser.new_context()` — no shared cookies, local storage, or session state.
- API tests use a shared `requests.Session` (session-scoped) but hit a read-only sandbox; each test is stateless by definition.
- No shared mutable fixtures between tests.

Run with: `pytest -n 4`

What breaks first when you turn parallelism up: if you share a single `browser` instance across workers without context isolation, you get race conditions on navigation. The current setup shares the browser process (cheap) but isolates the context (safe). The next bottleneck at very high parallelism is outbound network — JSONPlaceholder will rate-limit you.

## Reporting and Triage

When a test fails in CI at 3am, the on-call engineer sees an Allure report (linked in the GitHub Actions summary) with:

1. The exact failed assertion and stack trace
2. A screenshot taken at the moment of failure
3. A Playwright trace file (open at trace.playwright.dev) — step-by-step browser recording with network, console, and DOM snapshots
4. Browser console errors captured inline

Path to root cause: open the trace, scrub to the failed step, inspect the DOM snapshot and network tab. No need to reproduce locally for most failures.

## What I Would Do Next

**Parameterized cross-browser runs (chromium + firefox + webkit) in CI.**

Swag Labs is a controlled environment so cross-browser failures are unlikely here, but in a real product this is the highest-value addition: it surfaces layout and JS compatibility bugs that only appear in non-Chromium engines. The CI matrix is trivial to add; the payoff in caught bugs is high.

After that: a contract test layer between the UI and API using Pact, so frontend assumptions about response shapes are verified automatically without running E2E tests.

## AI Tools Used

Claude (claude-sonnet-4-6) was used for: scaffolding the project structure, generating the fixture boilerplate (conftest.py), and drafting this document. All test logic, selector choices, and architectural decisions were reviewed and validated manually.
