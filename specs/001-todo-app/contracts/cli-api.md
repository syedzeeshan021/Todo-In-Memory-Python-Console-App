# CLI API Contract: Todo In-Memory Python Console App

**Feature**: Todo In-Memory Python Console App
**Date**: 2026-01-03
**Status**: Complete

## Overview

This document defines the command-line interface contract for the Todo application. All commands follow the pattern `todo [command] [arguments]`.

## Commands

### Add Task
```
todo add "title" "description"
```

**Purpose**: Create a new task with a title and optional description
**Parameters**:
- `title` (required): String, max 200 characters
- `description` (optional): String, max 1000 characters
**Success Response**:
- Task created with unique ID
- Confirmation message: "Task added with ID: [ID]"
**Error Responses**:
- "Title cannot be empty" if title is empty
- "Title too long (max 200 characters)" if title exceeds limit
- "Description too long (max 1000 characters)" if description exceeds limit

### List Tasks
```
todo list
```

**Purpose**: Display all tasks with their status
**Parameters**: None
**Success Response**:
- List of all tasks in format: `[ID] [Status] Title - Description`
- Status indicator: [X] for complete, [ ] for incomplete
- If no tasks: "No tasks available"
**Error Responses**: None

### Update Task
```
todo update [ID] "title" "description"
```

**Purpose**: Update the title and/or description of an existing task
**Parameters**:
- `ID` (required): Integer, existing task ID
- `title` (optional): String, max 200 characters
- `description` (optional): String, max 1000 characters
**Success Response**:
- Confirmation message: "Task [ID] updated successfully"
**Error Responses**:
- "Task with ID [ID] not found" if ID doesn't exist
- "Title cannot be empty" if title is empty
- "Title too long (max 200 characters)" if title exceeds limit
- "Description too long (max 1000 characters)" if description exceeds limit

### Delete Task
```
todo delete [ID]
```

**Purpose**: Remove a task by its ID
**Parameters**:
- `ID` (required): Integer, existing task ID
**Success Response**:
- Confirmation message: "Task [ID] deleted successfully"
**Error Responses**:
- "Task with ID [ID] not found" if ID doesn't exist

### Complete Task
```
todo complete [ID]
```

**Purpose**: Mark a task as complete
**Parameters**:
- `ID` (required): Integer, existing task ID
**Success Response**:
- Confirmation message: "Task [ID] marked as complete"
**Error Responses**:
- "Task with ID [ID] not found" if ID doesn't exist

### Incomplete Task
```
todo incomplete [ID]
```

**Purpose**: Mark a task as incomplete
**Parameters**:
- `ID` (required): Integer, existing task ID
**Success Response**:
- Confirmation message: "Task [ID] marked as incomplete"
**Error Responses**:
- "Task with ID [ID] not found" if ID doesn't exist

### Exit Application
```
quit
```
or
```
exit
```

**Purpose**: Terminate the application
**Parameters**: None
**Success Response**:
- Application exits with message: "Goodbye!"
**Error Responses**: None