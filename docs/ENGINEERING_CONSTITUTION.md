# Universal Task AI — Engineering Constitution

This document is the project's internal source of truth for engineering decisions.

## 1. Prime Directive

Build a useful AI system without giving the model authority that the surrounding security architecture cannot safely constrain.

Capability is never a reason to bypass a control.

## 2. Reference Hierarchy

When making architecture decisions, use this order:

1. Explicit project requirements.
2. Security requirements and threat model.
3. Established standards and authoritative documentation.
4. Official framework capabilities.
5. Proven engineering patterns.
6. Simplicity and maintainability.
7. Experimental ideas.

A reference is an input to a decision, not permission to copy an unsafe pattern.

## 3. Task Contract Is the Boundary

Every executable task must have a normalized Task Contract before tool execution.

Minimum concepts:
- goal
- input
- context
- output
- format
- constraints
- tools allowed/required
- risk level
- approval requirement
- success criteria
- validation rules

User instructions have priority over inferred defaults. Ambiguity may be resolved only when the risk is low and the inference is defensible.

## 4. Least Privilege

Every agent and tool receives only the capabilities required for its current task.

Never:
- expose the host filesystem wholesale
- expose arbitrary environment variables
- expose credentials to the model
- allow unrestricted shell execution
- allow unrestricted network access

## 5. Tool Security

Every tool must define:
- typed input schema
- permission scope
- risk level
- input validation
- output validation
- timeout/resource limits
- audit event
- failure behavior
- tests

Tool calls must be treated as security-sensitive actions, not ordinary function calls.

## 6. Approval Boundary

Human approval is required for consequential external side effects, including:
- deleting or overwriting user data
- sending messages or publishing content
- financial transactions
- production changes
- pushing or releasing code
- privileged system operations
- actions whose impact cannot be safely reversed

The approval decision must occur before the side effect.

## 7. Guardrails

Guardrails operate at multiple boundaries:
- input
- task contract
- tool input
- tool output
- final output

A failed critical guardrail stops execution rather than asking the model to continue around it.

## 8. Sandbox

Untrusted code or file operations must execute inside an isolated workspace.

The sandbox must eventually enforce:
- CPU limit
- memory limit
- timeout
- filesystem isolation
- network policy
- process isolation
- package policy
- cleanup
- audit logging

The host is never considered a sandbox.

## 9. Prompt Injection

External content is data, not authority.

Web pages, files, emails, repositories, tool results, and retrieved documents may contain instructions intended to manipulate the agent. Such instructions must not override the Task Contract, system policy, permissions, or approval boundaries.

## 10. Secrets

Secrets must never be:
- committed
- embedded in prompts
- returned by tools
- printed in logs
- included in traces
- written into generated artifacts

Use environment/configuration mechanisms and secret redaction.

## 11. Validation

The system must validate results against the Task Contract instead of trusting the model's claim that work is complete.

Validation should be deterministic where possible:
- schema validation
- file existence/type checks
- test execution
- calculation checks
- source checks
- format checks
- permission checks

## 12. Observability

Every meaningful execution should be traceable without exposing secrets.

Record:
- task/run ID
- agent
- tool
- timestamps
- status
- bounded metadata
- failures
- approvals
- validation results

Do not log raw credentials or unrestricted sensitive content.

## 13. Simplicity

Prefer a small number of composable primitives over unnecessary agent complexity.

Add an agent only when a separate responsibility, permission boundary, context boundary, or evaluation target justifies it.

## 14. Failure Policy

Failure must be explicit.

Never silently:
- invent tool results
- claim completion
- ignore validation failures
- retry dangerous actions indefinitely
- downgrade security controls to make a task succeed

## 15. Definition of Done

A feature is not done until:
- implementation exists
- unit tests exist
- integration behavior is tested where relevant
- failure cases are tested
- security impact is reviewed
- documentation exists
- acceptance criteria pass
- no known secret is introduced

## 16. Change Rule

If a change increases model authority, network access, filesystem access, process execution, data access, or external side effects, update the threat model and security tests in the same change.

## 17. Target

The long-term target is a hybrid assistant that can understand arbitrary tasks, plan them, choose bounded capabilities, execute safely, verify results, and deliver useful artifacts while keeping humans in control of consequential actions.
