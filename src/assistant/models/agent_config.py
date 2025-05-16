from dataclasses import dataclass
from typing import List


@dataclass
class AgentConfig:
    """Configuration for an AI agent"""
    name: str
    role: str
    goal: str
    verbose: bool
    allow_delegation: bool
    backstory: str

@dataclass
class TaskConfig:
    """Configuration for a task"""
    name: str
    description: str
    expected_output: str
