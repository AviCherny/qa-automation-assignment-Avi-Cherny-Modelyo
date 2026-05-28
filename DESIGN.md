# Design Rationale

## Language and Framework Choice

I went with **Python + Playwright + pytest**.

Python because test code gets read by more people than just QA engineers — developers review tests too, and Python reads close enough to plain English that the intent is clear without needing to understand framework internals first.

I chose Playwright over Selenium because I didn't want to manage explicit waits. With Selenium you end up writing `WebDriverWait(driver, 10).until(EC.element_to_be_clickable(...))` everywhere, and eventually someone gets lazy and drops a `time.sleep(2)` instead, and now you have a flaky suite. Playwright waits for elements to be actionable before every action, which removes that whole category of failure by default.

Selenium is still the right call if the company already has a mature Selenium Grid or needs to support legacy browsers. But for a new project with no existing investment, Playwright wins on reliability and developer experience.

## Anti-Flakiness Strategy

The principle I followed: tests should wait for real conditions, not for time.

- No `time.sleep` anywhere. Every wait is condition-based.
- Playwright auto-waits for actions — `click`, `fill`, `select_option` all wait for the element to be actionable before doing anything.
- Assertions use Playwright's `expect()`, which retries until the condition is true or the timeout is reached. This means a test won't fail just because the DOM updated half a second after the action.
- Locators use `data-test` attributes exclusively. Swag Labs exposes them on every interactive element, and they survive CSS refactors and layout changes. Class-based selectors break the moment someone touches the styling.
- Each UI test gets a fresh browser context. No cookies, localStorage, or session state carried over from a previous test.

If this suite had to scale to 1000+ tests, the next investment would be around visibility into flakiness, not just prevention. That means automatic retry on failure, flagging tests that fail intermittently, and a way to track flakiness rates over time. At that scale the problem shifts from "how do we stop flakiness" to "how do we know which failures are real bugs vs. unstable tests."

## Parallelism and Isolation

Each UI test opens its own `browser.new_context()`, which gives full isolation — separate cookies, storage, and session — without the overhead of launching a new browser process per test. The browser process is shared; the context is not.

API tests use a shared `requests.Session` scoped to the session, but since the tests are read-only and stateless, there is no shared mutation between them.

The suite runs in parallel with:

```bash
pytest -n 4
```

The failure mode to watch for with higher parallelism is shared state: reused users, shared files, tests that depend on execution order. In this project the UI tests are isolated by context, so the more likely bottleneck under heavy load is the target environment itself — JSONPlaceholder will rate-limit before the test code breaks.

## Reporting and Triage

A failing test is only useful if someone can understand what went wrong without having to reproduce it locally.

Each failed test produces:
- The assertion that failed and the stack trace
- A screenshot from the moment of failure
- A Playwright trace file — a step-by-step recording of browser actions with DOM snapshots, network requests, and console output, viewable at trace.playwright.dev
- Console errors from the browser session

The triage flow is: open the report, find the failed test, open the trace, go to the failed step, look at the DOM and network state at that point. In most cases that's enough to know whether it's a product bug, an environment issue, or the test itself.

## What I Would Do Next

Not all tests should run on every push. The right split: smoke on PR (fast
gate), full regression nightly, cross-browser weekly.

At 500 tests, flakiness destroys team trust. Retry helps, but the real fix is
tracking pass rate per test over time and isolating the unstable ones — so one
bad test doesn't drag down the whole run.

The current setup uses a hardcoded user. The right solution is every test
responsible for its own data — creates its own user, cleans up after itself.
Nobody wants to build it, but everyone feels it when it's missing. We learned
that the hard way in a previous job. That's the kind of thing you carry with you.

After that, contract tests. E2E tests are too slow to be the first line of
defense against a broken API response shape.

## AI Tools Used

I designed the structure first — simple, easy to extend, easy to maintain.
Once the skeleton was in place, Claude implemented inside it. The structure
was the constraint. That's how I stayed in control of what came out.

Claude was my main tool. When I wasn't sure about something it produced,
I cross-checked with GPT — using one AI to check another.

The architectural decisions were mine: page object structure, isolation
strategy, selector approach, reporting. I made each one for a reason and can
explain the tradeoff.

If something breaks, I open the trace, find the failed step, and I know what
happened. I built it that way on purpose.
