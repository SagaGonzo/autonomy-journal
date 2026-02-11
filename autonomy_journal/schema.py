"""Schema management for event validation."""

from typing import Any, Dict, Optional
from jsonschema import validate, ValidationError


class EventSchema:
    """Schema definition for event validation."""
    
    def __init__(self, schema: Dict[str, Any]):
        """Initialize event schema.
        
        Args:
            schema: JSON Schema definition for events
        """
        self.schema = schema
    
    def validate(self, event: Dict[str, Any]) -> None:
        """Validate an event against the schema.
        
        Args:
            event: Event data to validate
            
        Raises:
            ValidationError: If event doesn't match schema
        """
        validate(instance=event, schema=self.schema)
    
    def is_valid(self, event: Dict[str, Any]) -> bool:
        """Check if event is valid without raising exception.
        
        Args:
            event: Event data to check
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.validate(event)
            return True
        except ValidationError:
            return False


def create_event_schema(
    event_type: str,
    properties: Optional[Dict[str, Any]] = None,
    required: Optional[list] = None,
    additional_properties: bool = False
) -> EventSchema:
    """Create a simple event schema.
    
    Args:
        event_type: Type identifier for the event
        properties: Schema properties for event fields
        required: List of required field names
        additional_properties: Whether to allow additional properties
        
    Returns:
        EventSchema instance
    """
    if properties is None:
        properties = {}
    
    if required is None:
        required = []
    
    # Ensure event_type is always required
    if "event_type" not in properties:
        properties["event_type"] = {"type": "string", "const": event_type}
    
    if "event_type" not in required:
        required = ["event_type"] + required
    
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": additional_properties
    }
    
    return EventSchema(schema)
