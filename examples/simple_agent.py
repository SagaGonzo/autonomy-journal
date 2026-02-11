"""Simple agent simulation example demonstrating autonomy-journal usage."""

from autonomy_journal import Journal, create_event_schema


def main():
    """Run a simple toy agent simulation."""
    
    # Define schemas for different event types
    agent_action_schema = create_event_schema(
        "agent.action",
        properties={
            "event_type": {"type": "string", "const": "agent.action"},
            "agent_id": {"type": "string"},
            "action": {"type": "string"},
            "timestamp": {"type": "number"}
        },
        required=["agent_id", "action", "timestamp"]
    )
    
    agent_observation_schema = create_event_schema(
        "agent.observation",
        properties={
            "event_type": {"type": "string", "const": "agent.observation"},
            "agent_id": {"type": "string"},
            "observation": {"type": "string"},
            "timestamp": {"type": "number"}
        },
        required=["agent_id", "observation", "timestamp"]
    )
    
    # Create journals for different event types
    with Journal(path="/tmp/agent_actions.jsonl", schema=agent_action_schema) as action_journal:
        with Journal(path="/tmp/agent_observations.jsonl", schema=agent_observation_schema) as obs_journal:
            
            # Simulate agent interactions
            print("Starting toy agent simulation...")
            
            # Agent observes environment
            obs_journal.log({
                "event_type": "agent.observation",
                "agent_id": "agent_001",
                "observation": "Room temperature is 72°F",
                "timestamp": 1000
            })
            
            # Agent takes action
            action_journal.log({
                "event_type": "agent.action",
                "agent_id": "agent_001",
                "action": "adjust_thermostat",
                "timestamp": 1001
            })
            
            # Agent observes result
            obs_journal.log({
                "event_type": "agent.observation",
                "agent_id": "agent_001",
                "observation": "Room temperature is 70°F",
                "timestamp": 1002
            })
            
            print(f"Logged {len(action_journal.get_events())} actions")
            print(f"Logged {len(obs_journal.get_events())} observations")
    
    # Read back and verify
    print("\nReading back logged events:")
    print("\nActions:")
    for event in Journal.read("/tmp/agent_actions.jsonl"):
        print(f"  - Agent {event['agent_id']} performed '{event['action']}' at t={event['timestamp']}")
    
    print("\nObservations:")
    for event in Journal.read("/tmp/agent_observations.jsonl"):
        print(f"  - Agent {event['agent_id']} observed '{event['observation']}' at t={event['timestamp']}")


if __name__ == "__main__":
    main()
