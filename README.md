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

## ✨ Features

The scheduling algorithms all live in `pawpal_system.py` and are surfaced through both the Streamlit UI (`app.py`) and a CLI demo (`main.py`):

- **Priority sorting** — orders tasks high → medium → low using a numeric `PRIORITY_ORDER` rank, so priorities sort by importance rather than alphabetically.
- **Sorting by time** — parses each `"HH:MM"` start time into an `(hour, minute)` tuple, so `"9:00"` correctly precedes `"10:00"` even when unpadded; unscheduled tasks sort to the end.
- **Filtering** — narrow the task list by pet (`filter_by_pet`) or by completion status (`filter_by_status`).
- **Conflict warnings** — buckets tasks by exact start time and flags any slot holding more than one task, naming the clashing tasks and their pets (works across the same pet *or* different pets).
- **Daily & weekly recurrence** — completing a recurring task auto-spawns a fresh, incomplete copy for the next due date (`due_date + timedelta`, so month/year rollover is handled); `once` tasks don't repeat, and re-completing a done task won't create duplicates.
- **Greedy daily planner** — selects the highest-priority pending tasks that fit within the owner's available minutes, then returns them in clock order so the plan reads as a timeline.
- **Plan explanation** — renders the generated plan as a human-readable summary of what was scheduled and how many minutes it uses.

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

### Confidence Level: ⭐⭐⭐⭐⭐ (5/5)

All 10 tests pass and cover the core scheduling logic — recurrence, sorting, and conflict
detection — including several edge cases (double-completion, unattached recurring tasks,
unpadded times, empty plans). The logic layer is well-exercised and behaves predictably.

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

## 🎬 Demo Walkthrough

PawPal+ runs two ways: an interactive **Streamlit app** (`streamlit run app.py`) and a scripted **CLI demo** (`python main.py`) that prints every scheduler feature in one pass.

### Main UI features (Streamlit)

From top to bottom, the app lets a pet owner:

- **Set owner details** — name and the number of care minutes available today.
- **Add pets** — name and species; every added pet becomes selectable when creating tasks.
- **Add tasks** — title, duration, priority (low/medium/high), start time, and repeat frequency (once/daily/weekly), each assigned to a specific pet.
- **See conflict warnings first** — any time two tasks share a start time, a highlighted warning appears at the top of the task list naming the clashing tasks and pets, with a tip to reschedule.
- **Sort and filter the task list** — sort by time of day or priority; filter by pet and by status (all/pending/completed), rendered in a clean table.
- **Mark tasks complete** — completing a recurring task automatically schedules its next occurrence and reports the new due date.
- **Generate today's schedule** — builds a timeline that fits the highest-priority tasks into the available minutes and shows how many were used.

### Example workflow

1. Enter the owner's name and set **Time available today** to `90` minutes.
2. **Add a pet** — e.g. `Rex` (dog) — then add a second, `Mia` (cat).
3. **Add tasks** to each pet with start times and priorities (e.g. Rex's *Morning walk* at 09:00 high, Mia's *Feed dinner* at 18:30 high).
4. Watch the **conflict warning** fire if two tasks land on the same time (e.g. Rex's evening walk and Mia's dinner both at 18:30).
5. **Sort by time** to read the day as a timeline, or **filter by pet** to focus on one animal.
6. **Mark** the daily *Morning walk* **complete** and see tomorrow's occurrence appear automatically.
7. Click **Generate schedule** to get the final plan that fits inside 90 minutes.

### Key Scheduler behaviors shown

- **Time sorting** — tasks entered out of order (and with an unpadded `9:00`) print in true chronological order.
- **Filtering** — separates pending vs. completed tasks, and isolates a single pet's tasks.
- **Conflict warnings** — detects the two tasks booked at `18:30` and names both.
- **Daily recurrence** — completing *Morning walk* grows Rex's task count from 3 to 4, with the next occurrence due the following day.
- **Greedy planning** — the schedule packs the highest-priority tasks into exactly the available minutes.

### Sample CLI output (`python main.py`)

```
========================================
All tasks, sorted by time
========================================
  08:00  Give medication (Mia)
   9:00  Morning walk (Rex)
  10:45  Brush coat (Rex)
  12:15  Play with feather toy (Mia)
  18:30  Evening walk (Rex)
  18:30  Feed dinner (Mia)

========================================
Filter: pending vs. completed
========================================
  Pending:
    - Evening walk
    - Morning walk
    - Brush coat
    - Play with feather toy
    - Feed dinner
  Completed:
    - Give medication

========================================
Filter: Rex's tasks only
========================================
  - Evening walk [18:30]
  - Morning walk [9:00]
  - Brush coat [10:45]

========================================
Conflict detection
========================================
  WARNING: 2 tasks clash at 18:30: Evening walk (Rex), Feed dinner (Mia)

========================================
Recurring task rollover
========================================
  Before: Rex has 3 tasks. 'Morning walk' due 2026-07-02.
  Completed 'Morning walk'.
  After:  Rex has 4 tasks. Next occurrence due 2026-07-03 (completed=False).

========================================
Today's Schedule
========================================
Planned 4 task(s) using 90 of 90 available minutes:
  - Morning walk (Rex) [high, 30 min]
  - Play with feather toy (Mia) [medium, 20 min]
  - Evening walk (Rex) [high, 30 min]
  - Feed dinner (Mia) [high, 10 min]
```
