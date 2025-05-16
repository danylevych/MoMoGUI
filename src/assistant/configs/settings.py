from typing import List, Tuple
from ..core.config_loader import AgentSettingsLoader
from ..models.agent_config import AgentConfig, TaskConfig


class AgentSettings:
    """Manages loading of agent settings from YAML files"""

    def __init__(self, settings_yaml_path: str):
        """
        Initialize settings from a YAML file

        Args:
            settings_yaml_path: Path to the settings YAML file
        """
        self.agent_settings, self.tasks_settings = self._load_settings(settings_yaml_path)

    def _load_settings(self, settings_yaml_path: str) -> Tuple[AgentConfig, List[TaskConfig]]:
        """
        Load settings using the AgentSettingsLoader

        Args:
            settings_yaml_path: Path to the settings YAML file

        Returns:
            Tuple of (agent_config, task_configs)
        """
        return AgentSettingsLoader.load_settings(settings_yaml_path)

