<!--
Sync Impact Report:
Version change: 0.1.0 → 1.0.0
Modified principles: All principles completely revised to match Phase I Todo Application requirements
Added sections: Core Principles, Key Standards, Constraints, Forbidden Features, Success Criteria, Multi-phase Context
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Phase I - In-Memory Python Console Todo Application Constitution

## Core Principles

### Simplicity First
Build only essential CRUD operations (Add, Delete, Update, View, Complete) - follow YAGNI principles and avoid feature creep until core functionality is solid.

### In-Memory Architecture
Data storage is in-memory only with NO persistence - data is intentionally lost on exit by design for Phase I, focusing on business logic before adding complexity.

### Type Safety Assurance
Full type hints required, leverage Python 3.13+ features, and maintain mypy strict compliance - no untyped code accepted in the codebase.

### Error Resilience
Never crash from user input, implement graceful degradation always - all user-facing functions must handle edge cases and invalid input safely.

### Test-Driven Development
Minimum 80% test coverage required, no feature implemented without accompanying tests - TDD approach with Red-Green-Refactor cycle strictly enforced.

## Key Standards

### Architecture Requirements
Clean layer separation required (UI → Services → Models) with no circular dependencies - maintain clear separation of concerns throughout the codebase.

### Code Style Compliance
PEP 8 compliance via ruff linter, Google-style docstrings for all public functions, and 100 character line limit for improved readability.

### Data Model Specification
Task dataclass must include id (int), title (str), description (str), completed (bool), and timestamps (datetime) fields - consistent data structure required.

### User Experience Design
Interactive console loop with clear prompts, confirmation required for destructive actions - prioritize user clarity and prevent accidental data loss.

### Testing Framework
pytest with pytest-cov required, mirror src/ structure in tests/ directory - maintain consistent test organization aligned with source code.

## Constraints

### Python Version Requirement
Python 3.13+ only is required - leverage latest language features and maintain version consistency across environments.

### Dependency Management
UV package manager required for all dependency management - standardize on modern, fast Python packaging tool.

### Standard Library Preference
Minimize external dependencies, prefer standard library solutions - reduce attack surface and maintenance overhead.

### State Management
No global state allowed - pass data explicitly through function parameters to maintain clear data flow.

### Task ID Management
Sequential integers starting from 1 for Task IDs, never reused after deletion - maintain consistent and predictable ID assignment.

### Development Methodology
Spec-Driven Development required - no manual coding, all code generated via Claude Code CLI from specifications to ensure consistency.

## Forbidden Features (Phase I Scope)

### Persistence Limitations
No data persistence features (files, databases, serialization) - maintain focus on core application logic without storage complexity.

### Feature Restrictions
No task priorities, categories, tags, or due dates - keep minimal feature set for Phase I foundation.

### Enhancement Prohibitions
No search, filter, or sort functionality beyond basic listing - avoid advanced features until core operations are stable.

### User System Exclusions
No user accounts or multi-user support - single-user console application only for Phase I.

### Advanced Operations
No undo/redo operations - maintain simplicity and focus on core CRUD functionality.

### Configuration Constraints
No configuration files or settings - avoid complexity around user preferences for initial phase.

### Formatting Limitations
No color/formatting libraries (plain text only) - keep UI simple and compatible across terminals.

### Logging Restrictions
No logging frameworks (use print for development only) - avoid complex logging infrastructure initially.

## Success Criteria

### Core Operations
All 5 core operations functional (add, delete, update, view, complete) - ensure full CRUD functionality meets requirements.

### Test Coverage
Test coverage ≥ 80% with all tests passing - maintain high quality standards through comprehensive testing.

### Type Checking
Type checking passes with zero mypy errors - ensure type safety across the entire codebase.

### Code Quality
Code passes ruff linting with zero warnings - maintain consistent code style and best practices.

### Error Handling
Application handles all error cases gracefully without crashes - ensure robust error handling throughout.

### Documentation Completeness
Documentation complete: README.md, CLAUDE.md, AGENTS.md with spec iteration history - provide comprehensive project documentation.

### Repository Structure
Repository structure follows Spec-Kit Plus conventions - maintain consistent project organization.

### Workflow Documentation
Spec-driven workflow fully documented - ensure reproducible development process.

## Multi-Phase Context

### Phase I Foundation
Current phase: In-memory console foundation - establish core architecture and patterns at console level.

### Phase II Web Application
Future phase: Full-stack web app (Next.js + FastAPI + SQLModel + Neon DB) - scale to web interface with persistent storage.

### Phase III AI Integration
Future phase: AI-powered chatbot (OpenAI ChatKit + Agents SDK + MCP) - add intelligent interaction capabilities.

### Phase IV Infrastructure
Future phase: Local K8s deployment (Docker + Minikube + Helm + kubectl-ai) - containerized orchestration setup.

### Phase V Production
Future phase: Cloud production (Kafka + Dapr + DigitalOcean DOKS) - enterprise-grade cloud deployment.

## Governance

### Amendment Process
Changes to this constitution require explicit approval and must align with multi-phase project vision - maintain consistency across development phases.

### Version Control Policy
Version follows semantic versioning: MAJOR for breaking changes, MINOR for additions, PATCH for corrections - maintain clear evolution path.

### Compliance Verification
All code submissions must verify compliance with all constitution principles - automated checks required in CI/CD pipeline.

**Version**: 1.0.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-11
