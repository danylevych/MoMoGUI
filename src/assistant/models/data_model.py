from dataclasses import dataclass
from typing import Optional


@dataclass
class AssistantData:
    """Data model for storing context information for the AI assistant"""
    prototype: str = ""
    results: str = ""
    metric: str = ""
    systems: str = ""

    def is_empty(self) -> bool:
        """Check if all fields are empty"""
        return not any([self.prototype, self.results, self.metric, self.systems])
