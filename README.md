# Autonomy Journal

Deterministic, schema-first JSONL logs for toy agent simulations (verification-first).

## Overview

Autonomy Journal is a lightweight Python library for creating deterministic, schema-validated JSONL logs for agent simulations. It emphasizes:

- **Schema-first**: Define and validate event schemas using JSON Schema
- **Deterministic**: Consistent output with sorted keys for reproducibility
- **Verification-first**: Built-in validation ensures data integrity
- **Simple**: Minimal API for logging and reading events

## Installation

```bash
pip install autonomy-journal
```

Or install from source:

```bash
git clone https://github.com/SagaGonzo/autonomy-journal.git
cd autonomy-journal
pip install -e .
```

## Quick Start

### Basic Usage

```python
from autonomy_journal import Journal

# Create a journal
with Journal(path="simulation.jsonl") as journal:
    journal.log({"event_type": "agent.action", "action": "move", "value": 10})
    journal.log({"event_type": "agent.observation", "observation": "wall detected"})

# Read events back
events = Journal.read("simulation.jsonl")
for event in events:
    print(event)
```

### With Schema Validation

```python
from autonomy_journal import Journal, create_event_schema

# Define a schema
schema = create_event_schema(
    "agent.action",
    properties={
        "event_type": {"type": "string", "const": "agent.action"},
        "agent_id": {"type": "string"},
        "action": {"type": "string"},
        "timestamp": {"type": "number"}
    },
    required=["agent_id", "action", "timestamp"]
)

# Create journal with schema validation
with Journal(path="actions.jsonl", schema=schema, strict=True) as journal:
    # This will succeed
    journal.log({
        "event_type": "agent.action",
        "agent_id": "agent_001",
        "action": "move",
        "timestamp": 1000
    })
    
    # This will raise ValidationError (missing required fields)
    # journal.log({"event_type": "agent.action"})
```

## Features

### Deterministic Output

All events are serialized with sorted keys, ensuring consistent output:

```python
journal.log({"z": 1, "a": 2, "m": 3})
# Output: {"a": 2, "m": 3, "z": 1}
```

### In-Memory Logging

Log events without writing to disk:

```python
journal = Journal()  # No path specified
journal.log({"event_type": "test", "value": 42})
events = journal.get_events()  # Retrieve from memory
```

### Strict and Non-Strict Modes

Control validation behavior:

```python
# Strict mode: raises exceptions on validation errors
journal = Journal(schema=schema, strict=True)

# Non-strict mode: silently ignores invalid events
journal = Journal(schema=schema, strict=False)
```

## Example

See `examples/simple_agent.py` for a complete example of a toy agent simulation.

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### Running Example

```bash
python examples/simple_agent.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
