from typing import List, Any
from crewai import Agent, Task, Crew
from crewai.llm import LLM

from .core.config_loader import AgentSettingsLoader
from .models.data_model import AssistantData
from ._api_keys import CONFIGS
from crewai_tools import SerperDevTool


class MoMoAgent:
    """
    MoMo AI Assistant using CrewAI

    This class manages the AI assistant that can answer questions about
    morphological modeling and analyze system data.
    """
    def __init__(self):
        """Initialize the MoMo AI assistant"""
        # Select the LLM model based on available API keys
        self.llm = self._create_llm()

        # Data storage for context information
        self.context_data = AssistantData()

        # Create the crew of AI agents
        self.crew = self._create_crew()

    def _create_llm(self) -> Any:
        """
        Create the language model based on available API keys

        Returns:
            An LLM instance from CrewAI
        """
        # Prefer OpenAI if available, fallback to Anthropic
        if CONFIGS.openai_api_key:
            return LLM(
                api_key=CONFIGS.openai_api_key,
                model=CONFIGS.model_to_use,
            )
        elif CONFIGS.anthropic_api_key:
            return LLM(
                api_key=CONFIGS.anthropic_api_key,
                model=CONFIGS.model_to_use,
            )
        else:
            raise ValueError("No API keys available for language models")

    def _create_crew(self) -> Crew:
        """
        Create the AI crew with agents and tasks

        Returns:
            Configured Crew instance
        """
        # Create tools
        tools = []
        if CONFIGS.serper_api_key:
            import os
            os.environ["SERPER_API_KEY"] = CONFIGS.serper_api_key
            tools.append(SerperDevTool())

        # Create agent and tasks
        agent, tasks = self._create_agent_and_tasks(tools)

        # Create and return the crew
        return Crew(
            agents=[agent],
            tasks=tasks,
            verbose=True,
            memory=True
        )

    def _create_agent_and_tasks(self, tools: List) -> tuple:
        """
        Create an agent and its tasks based on config

        Args:
            tools: List of tools to provide to the agent

        Returns:
            Tuple of (agent, tasks)
        """
        # Load agent settings
        agent_config, task_configs = AgentSettingsLoader.load_settings(
            "src/assistant/configs/settings/answer_agent.yaml"
        )

        # Create the agent
        agent = Agent(
            name=agent_config.name,
            role=agent_config.role,
            goal=agent_config.goal,
            backstory=agent_config.backstory,
            verbose=agent_config.verbose,
            allow_delegation=agent_config.allow_delegation,
            llm=self.llm,
            tools=tools,
            max_retry_limit=3
        )

        # Create tasks
        tasks = []
        for task_config in task_configs:
            tasks.append(Task(
                name=task_config.name,
                description=task_config.description,
                expected_output=task_config.expected_output,
                agent=agent,
                tools=tools
            ))

        return agent, tasks

    def set_results(self, prototype: str, results: str, metric: str, systems: str):
        """
        Set results data for context in conversations

        Args:
            prototype: The system prototype
            results: The similarity results
            metric: The similarity metric used
            systems: The system descriptions
        """
        self.context_data.prototype = prototype
        self.context_data.results = results
        self.context_data.metric = metric
        self.context_data.systems = systems

    def ask(self, user_input: str) -> str:
        """
        Ask a question to the AI assistant

        Args:
            user_input: The user's question or request

        Returns:
            The assistant's response in HTML format
        """
        # Execute the crew's tasks with inputs
        response = self.crew.kickoff(inputs={
            "input": user_input,
            "prototype": self.context_data.prototype,
            "results": self.context_data.results,
            "metric": self.context_data.metric,
            "systems": self.context_data.systems
        })

        # Return the response as is (already in HTML format from the YAML prompt)
        return response.raw
