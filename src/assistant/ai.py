from typing import List, Tuple
from crewai import Agent, Task, Crew
from crewai.memory import LongTermMemory
from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from crewai.tools import BaseTool

from src.assistant._api_keys import AI_API_KEYS
from src.assistant.configs.settings import AgentSettings


class SearchTool(BaseTool):
    name: str = "Search Tool"
    description: str = "Search the web for additional information when needed."

    def _run(self, query: str) -> str:
        return GoogleSerperAPIWrapper(serper_api_key=AI_API_KEYS.serpsearch_api_key).run(query)


class MoMoAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=AI_API_KEYS.openai_api_key,
            model="gpt-4o-mini"
        )
        self.crew = self._create_crew()
        self._results_dict = {
            "prototype": "",
            "results": "",
            "metric": ""
        }

    def _create_crew(self) -> Crew:
        search_tool = [SearchTool()]

        answer_agent, answer_task = self._create_agent_tasks(
            settings_path="src/assistant/configs/settings/answer_agent.yaml",
            llm=self.llm,
            tools=search_tool
        )

        return Crew(
            agents=[answer_agent],
            tasks=answer_task,
            verbose=True,
            memory=True
        )

    def _create_agent_tasks(self, settings_path: str, llm: str, tools: list = []) -> Tuple[Agent, List[Task]]:
        settings = AgentSettings(settings_path)
        agent = Agent(
            name=settings.agent_settings.name,
            role=settings.agent_settings.role,
            goal=settings.agent_settings.goal,
            backstory=settings.agent_settings.backstory,
            verbose=settings.agent_settings.verbose,
            allow_delegation=settings.agent_settings.allow_delegation,
            llm=llm,
            tools=tools,
            max_retry_limit=5
        )
        tasks = [Task(
            name=task.name,
            description=task.description,
            expected_output=task.expected_output,
            agent=agent,
            tools=tools
        ) for task in settings.tasks_settings]
        return agent, tasks

    def set_results(self, prototype: str, results: str, metric: str, systems: str):
        self._results_dict["prototype"] = prototype
        self._results_dict["results"] = results
        self._results_dict["metric"] = metric
        self._results_dict["systems"] = systems

    def ask(self, user_input):
        result = self.crew.kickoff(inputs={
            "input": user_input,
            "prototype": self._results_dict["prototype"],
            "results": self._results_dict["results"],
            "metric": self._results_dict["metric"],
            "systems": self._results_dict["systems"]
        }).raw

        return self._get_html_text(result)

    def _get_html_text(self, result):
        prompt =f"""
        You are an exper for converting markdown to html.
        You have been asked to convert the following markdown to html:

        ```markdown
        {result}
        ```

        Output only the html content.
        """
        import re
        markdown_pattern = re.compile(r"```html\n(.*?)\n```", re.DOTALL)
        content = self.llm.invoke(prompt).content.strip()
        html_text = markdown_pattern.search(content).group(1)
        print(html_text)
        return html_text
