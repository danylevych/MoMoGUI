import yaml
from typing import List, Tuple
from pydantic import BaseModel

class AgentConfig(BaseModel):
    name             : str
    role             : str
    goal            : str
    verbose          : bool
    allow_delegation : bool
    backstory        : str


class TaskConfig(BaseModel):
    name             : str
    description      : str
    expected_output  : str


class AgentSettings:
    def __init__(self, setings_yaml_path: str):
        (self.agent_settings, self.tasks_settings) = self._load_settings(setings_yaml_path)

    def _load_settings(self, setings_yaml_path: str) -> Tuple[AgentConfig, List[TaskConfig]]:
        with open(setings_yaml_path, 'r') as file:
            settings = yaml.safe_load(file)

            agent_data = list(settings['agents'])[0]
            agent = AgentConfig(**agent_data)
            tasks = [TaskConfig(**task) for task in settings['tasks']]
        return agent, tasks

