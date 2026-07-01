# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
3 core actions: Entering pet information, adding/editing tasks, generating a schedule based on off information entered


- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Class: Owner
Attributes: name, hour_available_per_day, preferences
Methods: add_task(), add_pet()
*This class allows new users to join and set up their accounts and pet information as well as tasks needed for the pet.

Class: Pet
Attributes: name, breed, weight, age, health_conditions
Methods: update_info()
*This class is used to input all information on a pet and constantly updates information if user decides to adjust.

Class: Schedule
Attributes: list_of_tasks, time_available
Methods: create_plan(), sort_by_priority()
*This class is used to create a schedule daily catered towards what the pet is, what their lifestyle or health is.

Class: Task
Attributes: name(walk/feed/meds), duration, priority, pet
Methods: is_high_priority()
*This class allows a new task to be added for the pet and can be labeled based off importance, which adjusts your schedule to take priority the most important tasks.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Added PRIORITY_ORDER with "high": 3, "medium":2, etc so that sort_by_priority can rank by number instead of strings
Changed Owner.hours_available: float to Owner.minutes_available: int so that all time is measured in minutes for less bugs and easy way to track time. Same happened to Scheduler.time_available: float became Scheduler.minutes_available: int
Added Owner.remove_task() to remove any task that may have been added but not wanted anymore.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My conflict detection (`Scheduler.detect_conflicts()`) only flags tasks that share the
*exact same* start time ("HH:MM"). It does **not** account for overlapping durations — a
30-minute walk starting at 9:00 and a task starting at 9:15 will not be reported as a
conflict, even though they actually overlap in real life. I chose this "lightweight"
approach on purpose: it groups tasks into time buckets in a single pass (O(n)), needs no
end-time math, and returns plain warning strings instead of raising, so the program keeps
running. For a busy pet owner who mostly just wants to be warned "you double-booked 6pm,"
exact-match detection catches the common mistake without the added complexity of interval
overlap logic. If the app later stores end times, `detect_conflicts()` could be upgraded to
a sweep-line overlap check (sort by start, compare each start against the previous end).

I also chose readability over cleverness in `sort_by_time()`: it uses a small named
`time_key` helper with a comment rather than a dense one-line lambda, because a human
reader needs to understand *why* unscheduled tasks sort to the end.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
