import yaml
from typing import List, Tuple
from ..models.agent_config import AgentConfig, TaskConfig

class AgentSettingsLoader:
    """Loads agent and task configurations from YAML files"""

    @staticmethod
    def load_settings(settings_yaml_path: str) -> Tuple[AgentConfig, List[TaskConfig]]:
        """
        Load agent and task settings from a YAML file

        Args:
            settings_yaml_path: Path to the YAML configuration file

        Returns:
            Tuple of (agent_config, task_configs)
        """
        with open(settings_yaml_path, 'r') as file:
            settings = yaml.safe_load(file)

            agent_data = list(settings['agents'])[0]
            agent = AgentConfig(**agent_data)
            tasks = [TaskConfig(**task) for task in settings['tasks']]

        return agent, tasks
