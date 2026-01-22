# ADR-0002: Task Data Model with Dataclass and Timestamp Management

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-18
- **Feature:** 001-console-todo-app
- **Context:** Need to define a robust, type-safe data model for the task entity that supports validation, immutability where appropriate, and proper timestamp management for the console todo application.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will implement the Task entity using a Python dataclass with the following characteristics:

- **Entity Structure**: Task dataclass with id, title, description, completed, created_at, updated_at, and completed_at fields
- **Type Safety**: Full type annotations including Optional for nullable fields
- **Validation**: Built-in validation for field constraints (title length, description length, etc.)
- **Timestamp Management**: Automatic timestamp handling with created_at immutable and updated_at managed by service layer

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Strong type safety reducing runtime errors
- Automatic generation of __init__, __repr__, and __eq__ methods
- Clear, readable data structure with explicit fields
- Built-in support for field defaults and ordering
- Easy serialization and debugging capabilities
- Complies with constitution's type safety assurance requirement

### Negative

- Potential immutability limitations (though dataclasses can be mutable)
- Learning curve for developers unfamiliar with dataclasses
- Slight overhead compared to plain dictionaries
- Possible performance implications for large numbers of tasks (minimal in practice)

## Alternatives Considered

Alternative A: Plain Python dictionary
- Pros: Simple, familiar, minimal overhead
- Cons: No type safety, no validation, verbose initialization, error-prone

Alternative B: Traditional class with manual __init__ and methods
- Pros: Full control over behavior, customizable
- Cons: More boilerplate, more prone to errors, less readable

Alternative C: Pydantic model
- Pros: Excellent validation, serialization capabilities, rich feature set
- Cons: Adds external dependency, violates constitution's standard library preference

Alternative D: NamedTuple
- Pros: Immutable, memory efficient, type safe
- Cons: Immutable (can't update fields), limited flexibility for state changes

## References

- Feature Spec: ../specs/001-console-todo-app/spec.md
- Implementation Plan: ../specs/001-console-todo-app/plan.md
- Related ADRs: ADR-0001 (In-Memory Storage), ADR-0003 (Console UI and Error Handling)
- Evaluator Evidence: ../specs/001-console-todo-app/research.md <!-- link to eval notes/PHR showing graders and outcomes -->
