# Model-assisted task understanding

The model may enrich task understanding, but it is never an authority over execution.

## Boundary

1. User task text enters the deterministic TaskContract projection.
2. A bounded ModelRequest is created from that projection.
3. The model must return a strict JSON analysis document.
4. Pydantic rejects unknown fields and malformed values.
5. The resulting TaskAnalysis is passed to the existing deterministic planner.
6. Tools, permissions, approvals, filesystem access, browser actions, and secrets remain outside model output.

Model output is untrusted data. A model cannot grant itself capabilities by returning fields such as `tools_allowed`, `approval_required`, credentials, or executable code.

## Failure behavior

Invalid JSON or schema violations fail the model-assisted analysis rather than silently converting model text into execution instructions. Deployments may omit model assistance and use the deterministic analyzer.

## Configuration

Model assistance is opt-in through the runtime composition. The provider boundary owns credentials and network access; task input never supplies an endpoint, API key, or model identifier.
