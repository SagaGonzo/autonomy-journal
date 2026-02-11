"""Core journal for logging agent events."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO
from .schema import EventSchema


class Journal:
    """Deterministic JSONL logger for agent simulations."""
    
    def __init__(
        self,
        path: Optional[str] = None,
        schema: Optional[EventSchema] = None,
        strict: bool = True
    ):
        """Initialize journal.
        
        Args:
            path: Path to JSONL file. If None, logs to memory only.
            schema: Optional schema for event validation
            strict: If True, validation errors raise exceptions
        """
        self.path = Path(path) if path else None
        self.schema = schema
        self.strict = strict
        self._file: Optional[TextIO] = None
        self._events: List[Dict[str, Any]] = []
        
        if self.path:
            self._file = open(self.path, 'a')
    
    def log(self, event: Dict[str, Any]) -> None:
        """Log an event.
        
        Args:
            event: Event data to log
            
        Raises:
            ValidationError: If schema validation fails in strict mode
        """
        if self.schema:
            if self.strict:
                self.schema.validate(event)
            elif not self.schema.is_valid(event):
                return
        
        self._events.append(event)
        
        if self._file:
            json_line = json.dumps(event, sort_keys=True)
            self._file.write(json_line + '\n')
            self._file.flush()
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Get all logged events from memory.
        
        Returns:
            List of logged events
        """
        return self._events.copy()
    
    def close(self) -> None:
        """Close the journal file."""
        if self._file:
            self._file.close()
            self._file = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False
    
    @staticmethod
    def read(path: str) -> List[Dict[str, Any]]:
        """Read events from a JSONL file.
        
        Args:
            path: Path to JSONL file
            
        Returns:
            List of events
        """
        events = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events
