"""
Main journal module for deterministic event logging.
"""
import json
from datetime import datetime
from typing import Any, Dict, Optional

class AutonomyJournal:
    """Deterministic JSONL journal for agent events."""
    
    def __init__(self, filepath: str, agent_id: str):
        """Initialize journal.
        
        Args:
            filepath: Path to JSONL output file
            agent_id: Unique identifier for the agent
        """
        self.filepath = filepath
        self.agent_id = agent_id
        self.file_handle = None
    
    def __enter__(self):
        """Context manager entry."""
        self.file_handle = open(self.filepath, 'a')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.file_handle:
            self.file_handle.close()
    
    def log_event(self, event_type: str, data: Dict[str, Any], 
                  metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log an event to the journal.
        
        Args:
            event_type: Type of event (agent_init, agent_action, etc.)
            data: Event-specific data payload
            metadata: Optional metadata (version, repro_hash, etc.)
        """
        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event_type': event_type,
            'agent_id': self.agent_id,
            'data': data
        }
        
        if metadata:
            event['metadata'] = metadata
        
        # Write with sorted keys for determinism
        json_line = json.dumps(event, sort_keys=True)
        self.file_handle.write(json_line + '\n')
        self.file_handle.flush()
