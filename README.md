# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
Today's Schedule
========================================
Planned 4 task(s) using 75 of 90 available minutes:
  - Morning walk (Rex) [high, 30 min]
  - Give medication (Mia) [high, 10 min]
  - Play with feather toy (Mia) [medium, 20 min]
  - Brush coat (Rex) [low, 15 min]
```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the full automated test suite from the project root:

```bash
python -m pytest
```

The suite (`tests/test_pawpal.py`) covers the behaviors most likely to break:

- **Recurrence logic** — completing a daily task spawns a fresh copy due the next day; weekly tasks land 7 days out; `once` tasks don't recur; and re-completing an already-done task is a no-op (no duplicate spawned).
- **Recurrence edge cases** — a recurring task with no attached pet still returns its next occurrence without crashing.
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order, correctly placing `"9:30"` before `"10:00"` (numeric parse, not string compare).
- **Conflict detection** — the `Scheduler` flags two tasks sharing the same start time with a single warning naming both.
- **Plan generation** — an owner with no tasks yields an empty plan and a clear "No tasks fit" message.
- **Core model** — adding a task increases a pet's task count; `mark_complete()` flips completion status.

Successful test run:

```
============================= test session starts =============================
platform win32 -- Python 3.9.0, pytest-8.4.2, pluggy-1.6.0
rootdir: C:\Users\ishp1\ai110-module2show-pawpal-starter
collected 10 items

tests\test_pawpal.py ..........                                          [100%]

============================= 10 passed in 0.03s ==============================
```

### Confidence Level: ⭐⭐⭐⭐☆ (4/5)

All 10 tests pass and cover the core scheduling logic — recurrence, sorting, and conflict
detection — including several edge cases. Confidence is high but not maxed out because the
tests exercise the logic layer only; the Streamlit UI (`app.py`) is not yet covered by
automated tests.

## 📐 Smarter Scheduling

PawPal+ goes beyond a flat task list with four pieces of scheduling logic, all in
`pawpal_system.py`:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()`, `Scheduler.sort_by_time()` | Priority sort ranks high→low via `PRIORITY_ORDER`. Time sort parses `"HH:MM"` into an `(hour, minute)` tuple so `"9:00"` correctly precedes `"10:00"` even when unpadded; unscheduled tasks sort last. |
| Filtering | `Scheduler.filter_by_status()`, `Scheduler.filter_by_pet()` | Return just the completed/pending tasks, or only the tasks belonging to a named pet. |
| Conflict detection | `Scheduler.detect_conflicts()` | Buckets scheduled tasks by exact start time and returns a warning string for any slot holding more than one task (same pet **or** different pets). Never raises — the caller prints the warning and continues. |
| Recurring tasks | `Task.mark_complete()`, `Task.next_occurrence()`, `Task.is_recurring()` | Completing a `daily`/`weekly` task auto-creates a fresh, incomplete copy for the next due date (`due_date + timedelta`, so calendar rollover is handled). `once` tasks don't recur. |

### How the daily plan is built

`Scheduler.generate_plan()` greedily selects the highest-priority pending tasks that fit
inside the owner's `minutes_available`, then returns them ordered by time so the plan reads
as a timeline. `Scheduler.explain_plan()` renders that plan as human-readable text.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
