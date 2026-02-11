"""
Schema validation module.
"""
import json
from pathlib import Path
from typing import Dict, Any

def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema file.
    
    Args:
        schema_name: Name of the schema file
        
    Returns:
        Schema dictionary
    """
    schema_path = Path(__file__).parent.parent.parent / 'schemas' / schema_name
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_event(event: Dict[str, Any], strict: bool = True) -> bool:
    """Validate an event against the autonomy schema.
    
    Args:
        event: Event dictionary to validate
        strict: Whether to use strict validation
        
    Returns:
        True if valid, raises exception otherwise
    """
    try:
        # Basic validation - check required fields
        required_fields = ['timestamp', 'event_type', 'agent_id', 'data']
        for field in required_fields:
            if field not in event:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate event_type
        valid_types = ['agent_init', 'agent_action', 'agent_observation', 
                      'agent_termination', 'system_state']
        if event['event_type'] not in valid_types:
            raise ValueError(f"Invalid event_type: {event['event_type']}")
        
        return True
    except Exception as e:
        if strict:
            raise
        return False
