---
description: "Task list for Phase I In-Memory Python Console Todo Application"
---

# Tasks: Phase I - In-Memory Python Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included as requested in feature specification to achieve ≥80% coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/{models,services,cli}
- [X] T002 Initialize Python 3.13+ project with pyproject.toml
- [X] T003 [P] Configure linting (ruff) and type checking (mypy) tools in pyproject.toml
- [X] T004 [P] Create README.md with run and usage instructions
- [X] T005 [P] Initialize AGENTS.md and CLAUDE.md files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Implement Task dataclass with all required fields in src/models/task.py
- [X] T007 [P] Implement timestamp initialization logic in src/models/task.py
- [X] T008 [P] Add model-level type annotations and docstrings in src/models/task.py
- [X] T009 [P] Implement TaskService with in-memory storage in src/services/task_service.py
- [X] T010 [P] Implement auto-incrementing ID counter in src/services/task_service.py
- [X] T011 [P] Implement basic validation for task properties in src/services/task_service.py
- [X] T012 [P] Define domain-specific exceptions in src/services/task_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks to their todo list with a title and optional description

**Independent Test**: User can add a task with a title (1-200 characters) and optional description (max 1000 characters), and the system assigns it a sequential ID starting from 1 with creation timestamp. The task appears in the task list.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Unit test for add_task with valid title in tests/unit/test_task_service.py
- [X] T014 [P] [US1] Unit test for add_task with title and description in tests/unit/test_task_service.py
- [X] T015 [P] [US1] Unit test for add_task validation (title length) in tests/unit/test_task_service.py
- [X] T016 [P] [US1] Unit test for sequential ID assignment in tests/unit/test_task_service.py

### Implementation for User Story 1

- [X] T017 [US1] Implement add_task method with validation and ID generation in src/services/task_service.py
- [X] T018 [US1] Implement input parsing for add command in src/cli/main.py
- [X] T019 [US1] Add command routing for add functionality in src/cli/main.py
- [X] T020 [US1] Implement console UI for adding tasks in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Enable users to view all their tasks in a list format with ID, completion status, title, and timestamps

**Independent Test**: User can view all tasks with their ID, completion status ([ ] or [x]), title, and timestamps in a clear, readable format.

### Tests for User Story 2 ⚠️

- [X] T021 [P] [US2] Unit test for list_tasks functionality in tests/unit/test_task_service.py
- [X] T022 [P] [US2] Unit test for get_task functionality in tests/unit/test_task_service.py
- [X] T023 [P] [US2] Unit test for empty task list scenario in tests/unit/test_task_service.py
- [X] T024 [P] [US2] Integration test for viewing task list in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T025 [US2] Implement list_tasks method in src/services/task_service.py
- [X] T026 [US2] Implement get_task method in src/services/task_service.py
- [X] T027 [US2] Implement task list rendering format in src/cli/main.py
- [X] T028 [US2] Add command routing for list functionality in src/cli/main.py
- [X] T029 [US2] Implement console UI for displaying tasks in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P1)

**Goal**: Enable users to mark tasks as complete to track progress and distinguish between completed and pending tasks

**Independent Test**: User can toggle the completion status of any task, and the system updates the completion timestamp and status indicator accordingly.

### Tests for User Story 3 ⚠️

- [X] T030 [P] [US3] Unit test for toggle completion functionality in tests/unit/test_task_service.py
- [X] T031 [P] [US3] Unit test for completion timestamp handling in tests/unit/test_task_service.py
- [X] T032 [P] [US3] Unit test for invalid task ID in toggle completion in tests/unit/test_task_service.py

### Implementation for User Story 3

- [X] T033 [US3] Implement toggle_task_completion method in src/services/task_service.py
- [X] T034 [US3] Implement input parsing for toggle command in src/cli/main.py
- [X] T035 [US3] Add command routing for toggle functionality in src/cli/main.py
- [X] T036 [US3] Implement console UI for toggling task completion in src/cli/main.py

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional

---

## Phase 6: User Story 4 - Update Existing Tasks (Priority: P2)

**Goal**: Enable users to update the title and description of existing tasks while preserving the creation timestamp

**Independent Test**: User can modify the title and description of an existing task while the system preserves the original creation timestamp and updates the modification timestamp.

### Tests for User Story 4 ⚠️

- [X] T037 [P] [US4] Unit test for update_task functionality in tests/unit/test_task_service.py
- [X] T038 [P] [US4] Unit test for preserving created_at timestamp in tests/unit/test_task_service.py
- [X] T039 [P] [US4] Unit test for updating updated_at timestamp in tests/unit/test_task_service.py
- [X] T040 [P] [US4] Unit test for validation in update operations in tests/unit/test_task_service.py

### Implementation for User Story 4

- [X] T041 [US4] Implement update_task method preserving created_at in src/services/task_service.py
- [X] T042 [US4] Implement input parsing for update command in src/cli/main.py
- [X] T043 [US4] Add command routing for update functionality in src/cli/main.py
- [X] T044 [US4] Implement console UI for updating tasks in src/cli/main.py

**Checkpoint**: All user stories 1, 2, 3, and 4 should now be independently functional

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Enable users to delete tasks from their list with confirmation prompt to prevent accidental deletion

**Independent Test**: User can delete a specific task by ID with confirmation prompt, and the system removes it from the collection while preventing ID reuse.

### Tests for User Story 5 ⚠️

- [X] T045 [P] [US5] Unit test for delete_task functionality in tests/unit/test_task_service.py
- [X] T046 [P] [US5] Unit test for ID prevention after deletion in tests/unit/test_task_service.py
- [X] T047 [P] [US5] Unit test for invalid task ID in deletion in tests/unit/test_task_service.py
- [X] T048 [P] [US5] Integration test for delete confirmation flow in tests/integration/test_cli.py

### Implementation for User Story 5

- [X] T049 [US5] Implement delete_task method with existence checks in src/services/task_service.py
- [X] T050 [US5] Implement confirmation prompt for delete in src/cli/main.py
- [X] T051 [US5] Implement input parsing for delete command in src/cli/main.py
- [X] T052 [US5] Add command routing for delete functionality in src/cli/main.py
- [X] T053 [US5] Implement console UI for deleting tasks with confirmation in src/cli/main.py

**Checkpoint**: All user stories 1, 2, 3, 4, and 5 should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T054 [P] Implement interactive command loop in src/cli/main.py
- [X] T055 [P] Implement input parsing and command routing in src/cli/main.py
- [X] T056 [P] Handle Ctrl+C and quit command gracefully in src/cli/main.py
- [X] T057 [P] Implement error catching without stack traces in src/cli/main.py
- [X] T058 [P] Add comprehensive error handling throughout application
- [X] T059 [P] Write edge case tests (invalid IDs, empty store) in tests/unit/test_task_service.py
- [X] T060 [P] Verify test coverage ≥80% with pytest-cov
- [X] T061 [P] Run mypy --strict and fix all issues
- [X] T062 [P] Run ruff and resolve all warnings
- [X] T063 [P] Enforce line length ≤100 characters
- [X] T064 [P] Verify Python 3.13 runtime compatibility
- [X] T065 [P] Update README.md with complete usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1-US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for add_task with valid title in tests/unit/test_task_service.py"
Task: "Unit test for add_task with title and description in tests/unit/test_task_service.py"

# Launch all implementation for User Story 1 together:
Task: "Implement add_task method with validation and ID generation in src/services/task_service.py"
Task: "Implement input parsing for add command in src/cli/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence