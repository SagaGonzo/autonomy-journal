"""Tests for autonomy_journal.schema module."""

import pytest
from jsonschema import ValidationError
from autonomy_journal.schema import EventSchema, create_event_schema


def test_event_schema_validate_success():
    """Test successful event validation."""
    schema = EventSchema({
        "type": "object",
        "properties": {
            "event_type": {"type": "string"},
            "value": {"type": "number"}
        },
        "required": ["event_type", "value"]
    })
    
    event = {"event_type": "test", "value": 42}
    schema.validate(event)


def test_event_schema_validate_failure():
    """Test failed event validation."""
    schema = EventSchema({
        "type": "object",
        "properties": {
            "event_type": {"type": "string"},
            "value": {"type": "number"}
        },
        "required": ["event_type", "value"]
    })
    
    event = {"event_type": "test"}
    
    with pytest.raises(ValidationError):
        schema.validate(event)


def test_event_schema_is_valid():
    """Test is_valid method."""
    schema = EventSchema({
        "type": "object",
        "properties": {
            "event_type": {"type": "string"}
        },
        "required": ["event_type"]
    })
    
    assert schema.is_valid({"event_type": "test"}) is True
    assert schema.is_valid({"wrong_field": "test"}) is False


def test_create_event_schema_basic():
    """Test basic event schema creation."""
    schema = create_event_schema("agent.action")
    
    assert schema.is_valid({"event_type": "agent.action"}) is True
    assert schema.is_valid({"event_type": "wrong.type"}) is False


def test_create_event_schema_with_properties():
    """Test event schema creation with properties."""
    schema = create_event_schema(
        "agent.action",
        properties={
            "event_type": {"type": "string", "const": "agent.action"},
            "action": {"type": "string"},
            "value": {"type": "number"}
        },
        required=["action", "value"]
    )
    
    valid_event = {
        "event_type": "agent.action",
        "action": "move",
        "value": 10
    }
    assert schema.is_valid(valid_event) is True
    
    invalid_event = {
        "event_type": "agent.action",
        "action": "move"
    }
    assert schema.is_valid(invalid_event) is False


def test_create_event_schema_additional_properties():
    """Test schema with additional properties control."""
    strict_schema = create_event_schema("test", additional_properties=False)
    loose_schema = create_event_schema("test", additional_properties=True)
    
    event_with_extra = {"event_type": "test", "extra_field": "value"}
    
    assert strict_schema.is_valid(event_with_extra) is False
    assert loose_schema.is_valid(event_with_extra) is True
