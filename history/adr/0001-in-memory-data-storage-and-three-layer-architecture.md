# ADR-0001: In-Memory Data Storage and Three-Layer Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-18
- **Feature:** 001-console-todo-app
- **Context:** Need to establish the foundational architecture for a Phase I console-based todo application that balances simplicity with maintainability and testability.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

We will implement a three-layer architecture with in-memory data storage for the Phase I console todo application:

- **Data Storage**: In-memory storage using Python dict[int, Task] with no persistence
- **Architecture Layers**: Clean separation of concerns with Models → Services → CLI layers
- **Technology Stack**: Python 3.13+ with standard library only (no external dependencies)

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- Simplified implementation and debugging for Phase I learning objectives
- Fast iteration cycles without database complexity
- Clear separation of concerns enabling better testability
- Reduced external dependencies aligning with constitution requirements
- Easy to reason about data flow and state management

### Negative

- All data is lost on application exit (by design for Phase I)
- Limited scalability compared to persistent storage solutions
- Potential memory growth issues with large numbers of tasks
- Architecture decisions may need reconsideration for Phase II persistence

## Alternatives Considered

Alternative A: File-based persistence using JSON/CSV files
- Pros: Simple persistence mechanism, data survives application restarts
- Cons: Adds complexity to Phase I, violates constitution's "no persistence" requirement for Phase I

Alternative B: Database storage (SQLite/PostgreSQL)
- Pros: Production-ready storage solution, supports complex queries
- Cons: Significantly increases complexity, violates constitution's minimal dependency requirement

Alternative C: Single-layer monolithic architecture
- Pros: Faster initial implementation, fewer files to manage
- Cons: Poor testability, difficult to maintain, violates clean architecture principles in constitution

## References

- Feature Spec: ../specs/001-console-todo-app/spec.md
- Implementation Plan: ../specs/001-console-todo-app/plan.md
- Related ADRs: ADR-0002 (Task Data Model), ADR-0003 (Console UI and Error Handling)
- Evaluator Evidence: ../specs/001-console-todo-app/research.md <!-- link to eval notes/PHR showing graders and outcomes -->
