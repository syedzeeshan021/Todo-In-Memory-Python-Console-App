<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- Principle 1: Template → Spec-Driven Development
- Principle 2: Template → Agentic Workflow
- Principle 3: Template → No Manual Coding
- Principle 4: Template → Clean Code and Structure
- Principle 5: Template → Transparency and Review
- Principle 6: Added → Technology Constraints
Added sections: Rules and Regulations section
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/sp.constitution.md ✅ updated
Follow-up TODOs: None
-->

# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Spec-Driven Development
All features must originate from a written specification. No implementation without a spec, plan, and tasks. This ensures clear requirements, testable outcomes, and prevents scope creep during development.

### II. Agentic Workflow
Follow the sequence strictly - Write spec → Clarify ambiguities → Generate plan → Break into tasks → Implement via AI tools (Claude Code). Iterations are allowed but must be documented. This maintains discipline in the development process and ensures proper planning before implementation.

### III. No Manual Coding
Developers (human or AI) must not write code directly. All code generation happens through Claude Code or equivalent AI tools. This enforces the agentic development methodology and ensures consistency in the development approach.

### IV. Clean Code and Structure
Adhere to PEP 8 standards, modular design, proper error handling, and a logical project structure (e.g., /src for code, separation of concerns). This ensures maintainable, readable, and professional code quality.

### V. Transparency and Review
All prompts, iterations, specs, plans, tasks, and outputs must be versioned and stored for review. The process will be judged on fidelity to this workflow. This enables accountability and allows for process improvement.

### VI. Technology Constraints
Use UV for environment management, Python 3.13+, Claude Code for implementation, Spec-Kit Plus for spec management. No additional libraries unless specified and justified in the plan. This maintains consistency in the development environment and tooling.

## Rules and Regulations

- **Features**: Implement exactly the 5 basic functionalities - Add task (with title and description), Delete task (by ID), Update task details, View/List all tasks (with status indicators), Mark task as complete/incomplete.
- **Storage**: In-memory only (e.g., using lists or dictionaries in Python; no persistence to files or databases).
- **User Interface**: Command-line interface (CLI) only, using standard input/output. Keep interactions simple and intuitive.
- **Technology Constraints**: Use UV for environment management, Python 3.13+, Claude Code for implementation, Spec-Kit Plus for spec management. No additional libraries unless specified and justified in the plan.
- **Testing**: Include basic unit tests generated via the workflow. Demonstrate functionality in the console app.
- **Documentation**: README.md must include setup instructions (e.g., UV setup, running the app). CLAUDE.md must detail Claude Code usage instructions and prompts used.
- **GitHub Repository Structure**: Root must contain constitution file, specs history folder (with all spec versions), /src folder (Python code), README.md, CLAUDE.md.
- **Evaluation Criteria**: Completeness of features, adherence to workflow, quality of prompts/iterations, clean code, and working demo.

## Governance

This constitution establishes the foundational rules, principles, and constraints for developing a basic command-line todo application that stores tasks in memory. All development must adhere to spec-driven methodologies using AI-assisted tools, ensuring no manual coding occurs. The goal is to demonstrate disciplined, agentic development practices. Violations of these principles invalidate the development phase. Amendments require explicit approval in subsequent phases.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date required | **Last Amended**: 2026-01-03