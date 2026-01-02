# Tasks: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Branch**: `001-todo-app`
**Created**: 2026-01-03
**Status**: Generated

**Input**: Implementation plan, feature specification, data model, API contracts, research findings

## Implementation Strategy

This task breakdown follows the agentic workflow with tasks organized by user story to enable independent implementation and testing. The approach is to build the application incrementally:

1. **MVP**: Implement the foundational Task and TaskManager classes with the Add task functionality (US1)
2. **Incremental Delivery**: Add one user story at a time with associated tests
3. **Integration**: Complete CLI loop with all commands
4. **Polish**: Documentation and final testing

The minimum viable product (MVP) includes just User Story 1 (Add Tasks) which provides foundational functionality.

## Dependencies

- User Story 2 (View Tasks) depends on foundational Task and TaskManager classes
- User Stories 3-5 (Complete, Update, Delete) depend on foundational classes and Add functionality
- Integration phase depends on all user story implementations

## Parallel Execution Opportunities

- [US2] View Tasks and [US3] Mark Complete/Incomplete tasks can be developed in parallel after US1
- [US4] Update Tasks and [US5] Delete Tasks can be developed in parallel after US1
- Unit tests can be developed in parallel with feature implementation
- Documentation can be created in parallel with implementation

---

## Phase 1: Setup

### Goal
Initialize project structure and foundational files required for all user stories.

### Independent Test Criteria
Project structure is created with proper directory layout and can be executed.

### Tasks

- [X] T001 Create src/ directory structure per implementation plan
- [X] T002 Create tests/ directory structure per implementation plan
- [X] T003 Initialize src/main.py with basic structure and imports
- [X] T004 Create README.md with setup instructions
- [X] T005 Create pyproject.toml for UV package management

---

## Phase 2: Foundational Components

### Goal
Implement core Task and TaskManager classes that will be used by all user stories.

### Independent Test Criteria
Core classes can be instantiated and basic functionality (creating tasks, managing task list) works.

### Tasks

- [X] T006 [P] Implement Task class in src/main.py with id, title, description, status attributes
- [X] T007 [P] Implement TaskManager class in src/main.py with tasks list and next_id counter
- [X] T008 [P] Implement input validation functions for title and description length limits
- [X] T009 [P] Implement error handling utilities for consistent error messages

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1)

### Goal
Implement the ability to add new tasks with title and description via command-line interface.

### Independent Test Criteria
- Can run `todo add "Buy groceries" "Milk, eggs, bread"` and verify task appears in memory
- Can run add command with only title and verify task is added with empty description

### Tests (if requested)
- [X] T010 [P] [US1] Create unit tests for Task creation with various inputs
- [X] T011 [P] [US1] Create unit tests for TaskManager.add_task method
- [X] T012 [P] [US1] Create unit tests for input validation functions

### Implementation

- [X] T013 [US1] Implement add_task method in TaskManager with validation
- [X] T014 [US1] Implement CLI command handler for 'add' subcommand
- [X] T015 [US1] Integrate 'add' command with argparse in main CLI loop

---

## Phase 4: User Story 2 - View Tasks (Priority: P1)

### Goal
Implement the ability to see all tasks in a clear, organized format that shows the status of each task.

### Independent Test Criteria
- Can add multiple tasks, run `todo list`, and verify all tasks are displayed with proper status indicators
- When no tasks exist, running `todo list` shows appropriate message

### Tests (if requested)
- [X] T016 [P] [US2] Create unit tests for TaskManager.list_tasks method
- [X] T017 [P] [US2] Create unit tests for task display formatting

### Implementation

- [X] T018 [US2] Implement list_tasks method in TaskManager with proper formatting
- [X] T019 [US2] Implement CLI command handler for 'list' subcommand
- [X] T020 [US2] Integrate 'list' command with argparse in main CLI loop

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P2)

### Goal
Implement the ability to update the status of tasks as complete or incomplete by ID.

### Independent Test Criteria
- Can add a task, run `todo complete 1`, then verify task status updates correctly
- Can mark a task as incomplete after it was complete, and verify status updates correctly

### Tests (if requested)
- [X] T021 [P] [US3] Create unit tests for TaskManager.complete_task method
- [X] T022 [P] [US3] Create unit tests for TaskManager.incomplete_task method

### Implementation

- [X] T023 [US3] Implement complete_task method in TaskManager with validation
- [X] T024 [US3] Implement incomplete_task method in TaskManager with validation
- [X] T025 [US3] Implement CLI command handler for 'complete' subcommand
- [X] T026 [US3] Implement CLI command handler for 'incomplete' subcommand
- [X] T027 [US3] Integrate 'complete' and 'incomplete' commands with argparse in main CLI loop

---

## Phase 6: User Story 4 - Update Task Details (Priority: P2)

### Goal
Implement the ability to modify the title or description of existing tasks by ID.

### Independent Test Criteria
- Can add a task, run `todo update 1 "New title" "New description"`, and verify changes are reflected
- Can update only the title while keeping the original description

### Tests (if requested)
- [X] T028 [P] [US4] Create unit tests for TaskManager.update_task method

### Implementation

- [X] T029 [US4] Implement update_task method in TaskManager with validation
- [X] T030 [US4] Implement CLI command handler for 'update' subcommand
- [X] T031 [US4] Integrate 'update' command with argparse in main CLI loop

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

### Goal
Implement the ability to remove tasks by ID.

### Independent Test Criteria
- Can add tasks, run `todo delete 1`, and verify the task no longer appears in the list
- When attempting to delete a non-existent task, appropriate error message is displayed

### Tests (if requested)
- [X] T032 [P] [US5] Create unit tests for TaskManager.delete_task method

### Implementation

- [X] T033 [US5] Implement delete_task method in TaskManager with validation
- [X] T034 [US5] Implement CLI command handler for 'delete' subcommand
- [X] T035 [US5] Integrate 'delete' command with argparse in main CLI loop

---

## Phase 8: Integration & CLI Loop

### Goal
Implement the main CLI loop with argparse for all commands and proper application flow.

### Independent Test Criteria
- All commands work within a continuous loop until exit command is entered
- Invalid command format produces appropriate error messages
- Application gracefully handles edge cases from specification

### Implementation

- [X] T036 Implement main CLI loop with argparse for all subcommands
- [X] T037 Implement quit/exit command handlers
- [X] T038 Add error handling for invalid command formats
- [X] T039 Implement proper application startup and graceful exit

---

## Phase 9: Testing & Quality Assurance

### Goal
Create comprehensive tests for all functionality and ensure quality standards.

### Independent Test Criteria
- All unit tests pass
- Integration tests pass for CLI commands
- Error handling works as specified

### Implementation

- [X] T040 Create integration tests for CLI commands in tests/integration/test_cli.py
- [X] T041 Create comprehensive unit tests for all TaskManager methods in tests/unit/test_todo.py
- [X] T042 Run all tests and verify they pass
- [X] T043 Test edge cases from specification (empty titles, invalid IDs, etc.)

---

## Phase 10: Documentation & Polish

### Goal
Complete documentation and final quality checks.

### Independent Test Criteria
- README.md contains clear setup and usage instructions
- All functionality works as specified
- Code follows PEP 8 standards

### Implementation

- [X] T044 Update README.md with complete usage instructions
- [X] T045 Create CLAUDE.md with Claude Code usage instructions
- [X] T046 Verify all requirements from specification are implemented
- [X] T047 Run code quality checks and ensure PEP 8 compliance
- [X] T048 Test complete workflow from add to delete with all commands