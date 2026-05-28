# Implementation Checklist

Track every deliverable from the assignment. Work top to bottom.

---

## Project Setup

- [x] Create virtual environment and `requirements.txt` (playwright, pytest, pytest-xdist, pytest-playwright)
- [x] Create `pytest.ini` with base config (testpaths, parallel workers, Playwright options)
- [x] Create `config/settings.py` — centralised env-var config (BASE_URL, API_BASE_URL, BROWSER, HEADED, TIMEOUT)
- [x] Create `conftest.py` with shared fixtures (browser context per test, page, api_client)

---

## Part 1 — UI Tests (Swag Labs)

### Page Objects (`pages/`)

- [x] `login_page.py` — username input, password input, login button, error message locator
- [x] `inventory_page.py` — inventory item list, add-to-cart buttons, cart badge, sort dropdown
- [x] `cart_page.py` — cart item list (name + price), remove buttons, checkout button
- [x] `checkout_page.py` — first name, last name, zip inputs; continue button; item total; finish button; confirmation message

### Tests (`tests/ui/`)

- [x] `test_login.py` — Scenario 1: login happy path → lands on inventory, items visible
- [x] `test_login.py` — Scenario 2: invalid credentials → visible error with exact message text
- [x] `test_cart.py` — Scenario 3: add 2+ products → verify badge count AND cart contents (name + price)
- [x] `test_checkout.py` — Scenario 4: add product → checkout flow (Info → Overview → Finish) → order confirmation visible
- [x] (Bonus) `test_sorting.py` — product sort price low-to-high; cart badge updates on add/remove

### Anti-flakiness (UI)

- [x] Zero `time.sleep` calls — use Playwright auto-waits and `expect()` assertions only
- [x] All locators use `data-test` attributes (Swag Labs exposes them) — no brittle XPath/CSS chains
- [x] Each test gets a fresh browser context via fixture (no shared login state between tests)
- [ ] Run 10 consecutive times in CI and confirm green — check Actions history

---

## Part 2 — API Tests (JSONPlaceholder)

### API Client (`client/`)

- [x] `api_client.py` — base URL, default headers, timeout, session reuse; one method per verb (get, post, put, delete)

### Tests (`tests/api/`)

- [x] `test_posts_get.py` — Scenario 1: GET /posts → 200, JSON array, length > 0, schema check (userId, id, title, body)
- [x] `test_posts_get.py` — Scenario 2: GET /posts/1 → 200 valid id; GET /posts/99999 → 404 non-existent id
- [x] `test_posts_crud.py` — Scenario 3: POST /posts → 201, response echoes payload, includes generated `id`
- [x] `test_posts_crud.py` — Scenario 4: PUT /posts/1 → 200 with updated body; DELETE /posts/1 → 200 or 204

### Anti-flakiness (API)

- [x] Tests are order-independent (no shared state, no depends on previous test)
- [x] Assert response schema, not just status code

---

## Part 3 — Framework Architecture

- [x] No locators in test files — all in page objects
- [x] No hardcoded URLs anywhere in tests or pages — all via `config/settings.py`
- [x] `client/api_client.py` is the single place to change base URL, headers, timeouts, retry policy
- [x] Clean separation: `tests/` vs `pages/` vs `client/` vs `config/`
- [x] Each test owns its own setup and teardown via fixtures — no mutable shared state

---

## Part 4 — Anti-Flakiness, Parallelism & Reporting

- [x] Confirm zero sleeps across entire codebase (`grep -r "time.sleep" tests/ pages/` returns nothing)
- [x] Confirm zero implicit waits
- [x] `pytest -n 4` runs without test interference — verified locally (11/11 passed)
- [x] Playwright HTML report generated on every run (`playwright-report/index.html`)
- [x] Failed tests capture: screenshot + Playwright trace (configured in `conftest.py`)
- [x] Confirm artifacts are downloadable from GitHub Actions run

---

## Part 5 — DESIGN.md

- [x] **Language and framework choice** — why Python + Playwright; when would you pick Selenium instead
- [x] **Anti-flakiness strategy** — concrete techniques used; what would you add at scale (1000+ tests)
- [x] **Parallelism and isolation** — how tests are isolated; what breaks first when you scale workers up
- [x] **Reporting and triage** — what the on-call engineer sees at 3am; path to root cause
- [x] **What you would do next** — next thing to build if you had 2 more days, and why
- [x] **AI tools used** — document what Claude was used for (as required by assignment rules)

---

## Part 6 — CI/CD

- [x] `.github/workflows/tests.yml` — triggers on push and PR to main
- [x] Pipeline: install deps → `playwright install` → run UI + API tests → upload HTML report + failure artifacts
- [x] UI and API test jobs run in parallel in the pipeline
- [x] Pipeline is green on main before submission
- [ ] (Optional) `Dockerfile` that produces the same green run

---

## Final Submission Checks

- [x] Repo is public
- [x] `README.md` — prerequisites, setup, run locally, run in parallel, view reports, link to CI run
- [x] `DESIGN.md` at repo root
- [x] Latest CI run on main is green
- [x] Update README CI badge link to point to actual passing run
- [ ] Send repo URL by replying to the email
