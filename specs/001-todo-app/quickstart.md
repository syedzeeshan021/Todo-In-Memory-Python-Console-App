# Quickstart Guide: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Date**: 2026-01-03
**Status**: Complete

## Prerequisites

- Python 3.13+ installed
- UV package manager installed

## Setup

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment using UV:
   ```bash
   uv venv
   ```
4. Activate the virtual environment:
   ```bash
   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

## Running the Application

To run the Todo application:

```bash
python src/main.py
```

The application will start in interactive mode, waiting for commands.

## Available Commands

### Add a Task
```bash
todo add "Task Title" "Task Description"
```
- Title is required (max 200 characters)
- Description is optional (max 1000 characters)
- Returns a unique ID for the created task

### List All Tasks
```bash
todo list
```
- Displays all tasks with ID, title, description, and status
- Status shown as [X] for complete, [ ] for incomplete

### Update a Task
```bash
todo update 1 "New Title" "New Description"
```
- Updates the title and description of task with specified ID
- Both title and description are optional (can update one or both)

### Mark Task Complete
```bash
todo complete 1
```
- Marks the task with specified ID as complete
- Status will show as [X]

### Mark Task Incomplete
```bash
todo incomplete 1
```
- Marks the task with specified ID as incomplete
- Status will show as [ ]

### Delete a Task
```bash
todo delete 1
```
- Removes the task with specified ID from the list

### Exit the Application
```bash
quit
```
or
```bash
exit
```
- Terminates the application

## Example Workflow

1. Add a task:
   ```
   todo add "Buy groceries" "Milk, eggs, bread"
   ```

2. List tasks:
   ```
   todo list
   ```

3. Mark task as complete:
   ```
   todo complete 1
   ```

4. Exit:
   ```
   quit
   ```

## Error Handling

The application provides specific error messages:
- "Task with ID X not found" - when referencing a non-existent task ID
- "Title cannot be empty" - when trying to add a task with an empty title
- "Invalid command format" - when command syntax is incorrect