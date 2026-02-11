"""Tests for autonomy_journal.journal module."""

import json
import tempfile
from pathlib import Path
import pytest
from autonomy_journal.journal import Journal
from autonomy_journal.schema import create_event_schema
from jsonschema import ValidationError


def test_journal_log_to_memory():
    """Test logging events to memory only."""
    journal = Journal()
    
    journal.log({"event_type": "test", "value": 1})
    journal.log({"event_type": "test", "value": 2})
    
    events = journal.get_events()
    assert len(events) == 2
    assert events[0]["value"] == 1
    assert events[1]["value"] == 2


def test_journal_log_to_file():
    """Test logging events to file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_path = f.name
    
    try:
        with Journal(path=temp_path) as journal:
            journal.log({"event_type": "test", "value": 1})
            journal.log({"event_type": "test", "value": 2})
        
        events = Journal.read(temp_path)
        assert len(events) == 2
        assert events[0]["value"] == 1
        assert events[1]["value"] == 2
    finally:
        Path(temp_path).unlink()


def test_journal_with_schema_strict():
    """Test journal with schema in strict mode."""
    schema = create_event_schema(
        "agent.action",
        properties={
            "event_type": {"type": "string", "const": "agent.action"},
            "action": {"type": "string"}
        },
        required=["action"]
    )
    
    journal = Journal(schema=schema, strict=True)
    
    journal.log({"event_type": "agent.action", "action": "move"})
    
    with pytest.raises(ValidationError):
        journal.log({"event_type": "agent.action"})


def test_journal_with_schema_non_strict():
    """Test journal with schema in non-strict mode."""
    schema = create_event_schema(
        "agent.action",
        properties={
            "event_type": {"type": "string", "const": "agent.action"},
            "action": {"type": "string"}
        },
        required=["action"]
    )
    
    journal = Journal(schema=schema, strict=False)
    
    journal.log({"event_type": "agent.action", "action": "move"})
    journal.log({"event_type": "agent.action"})
    
    events = journal.get_events()
    assert len(events) == 1


def test_journal_context_manager():
    """Test journal as context manager."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_path = f.name
    
    try:
        with Journal(path=temp_path) as journal:
            journal.log({"event_type": "test", "value": 1})
        
        assert journal._file is None
        
        events = Journal.read(temp_path)
        assert len(events) == 1
    finally:
        Path(temp_path).unlink()


def test_journal_read_empty_lines():
    """Test reading JSONL file with empty lines."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        f.write('{"event_type": "test", "value": 1}\n')
        f.write('\n')
        f.write('{"event_type": "test", "value": 2}\n')
        temp_path = f.name
    
    try:
        events = Journal.read(temp_path)
        assert len(events) == 2
    finally:
        Path(temp_path).unlink()


def test_journal_deterministic_output():
    """Test that journal produces deterministic output (sorted keys)."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_path = f.name
    
    try:
        with Journal(path=temp_path) as journal:
            journal.log({"z": 1, "a": 2, "m": 3})
        
        with open(temp_path, 'r') as f:
            line = f.read().strip()
        
        parsed = json.loads(line)
        keys = list(parsed.keys())
        assert keys == ["a", "m", "z"]
    finally:
        Path(temp_path).unlink()
