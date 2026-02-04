# Code of Conduct for This Test Project

This document defines how we structure automated UI tests, with a focus on the Page Object Model (POM). It is written for both humans and agents, so the rules are explicit and actionable.

----

## 1) Page Object Model (POM) Rules

### 1.1 Core Principles
- **Separation of concerns**: Page Objects describe how to interact with the UI. Tests describe what should happen and verify outcomes.
- **Stability over convenience**: Prefer stable locators and reusable methods to reduce maintenance.
- **Readable tests**: Tests should read like a scenario, not like a sequence of low-level UI commands.

### 1.2 What Belongs in a Page Object
- Element locators for a single page/screen.
- UI actions (click, type, select, wait) related to that page.
- Composite UI actions (e.g., `login(user, pass)`), built from atomic actions.
- Data extraction helpers (e.g., `get_title_text()`, `get_cards()`), returning values to tests.

### 1.3 What Does NOT Belong in a Page Object
- Business logic and test assertions.
- Cross-page orchestration (use tests or fixtures for flows).
- Test data setup (credentials, expected values, datasets).

### 1.4 Assertions and Checks
- **Default rule**: assertions live in tests.
- **Allowed exception**: small validation helpers that return booleans (e.g., `is_header_visible()`), but avoid hard `assert` inside Page Objects unless explicitly agreed.

### 1.5 Single Action vs Composite Action
- **Atomic methods**: one direct UI interaction (click, input, select).
- **Composite methods**: sequence of atomic actions representing a user action (login, apply filter).
- Composite methods are encouraged for readability and reuse.

### 1.6 Locators Strategy
- Prefer locators in this order:
  1. `data-testid` / `data-test` / `data-id`
  2. `id`
  3. stable CSS selectors
  4. XPath as last resort
- Store locators in a dedicated locators module per page/component.

----

## 2) Page Objects vs Page Components

### 2.1 Definitions
- **Page Object**: models a full page/screen.
- **Page Component**: reusable UI block used across multiple pages (e.g., header, plan selector).

### 2.2 When to Create a Component
- UI block is reused across multiple pages.
- UI block has complex interaction logic.
- UI block can be tested/used independently of a page.

----

## 3) Project Structure (Current)

```
src/
  api/                  # API helpers used by tests/pages
  components/           # reusable UI components (POM components)
  configs/              # project configuration and constants
  pages/                # page objects
  tests/                # tests grouped by feature
  utils/                # utilities shared across project
conftest.py             # pytest fixtures and CLI options
pytest.ini              # pytest configuration
```

**Notes**
- `pages/` should contain only page-level interactions.
- `components/` should contain reusable blocks (each with its own locators).
- `utils/` should contain generic helpers (no UI logic).

----

## 4) Code Style and Maintainability

- Use descriptive method names (`open_filters`, `select_mmo_genre`).
- Keep methods small and focused.
- Do not duplicate locators or hardcode selectors in tests.
- Prefer reusable helpers to reduce duplication (DRY).
- Avoid mixing test logic and UI logic in the same method.

----

## 5) Test Writing Guidelines

- Tests define: **input data**, **steps**, and **assertions**.
- Tests should not contain direct Selenium calls.
- Use fixtures to prepare test context (driver, auth, data).
- Use markers to group tests (`@pytest.mark.cloud`, etc.).

----

## 6) Git Workflow (Short Version)

- Create a separate branch per task.
- Branch name format: `ALLIANCE-12345/short-description`.
- Commit format: `ALLIANCE-12345: short imperative summary`.
- Keep commits small and focused.

----

## 7) Useful References

- Page Object Model (Selenium docs): https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
- POM Guide: https://testengineer.ru/bolshoj-gajd-po-page-object-model/
- Pytest docs: https://docs.pytest.org/en/stable/
