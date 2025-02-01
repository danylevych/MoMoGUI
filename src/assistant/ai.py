
from langchain_ollama import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory

from .llm_type import LLMType
from .utils import load_prompt
from ._api_keys import AI_API_KEYS



class MoMoAgent:
    """
    The agent that will be used to interact with the user.
    """
    def __init__(self, llm_type: LLMType = LLMType.OPENAI):

        self._set_llm(llm_type)
        self._create_chain()

        self.results_dict = dict(prototype="", results="", metric="")

    def _set_llm(self, llm_type: LLMType):
        if llm_type == LLMType.OLLAMA:
            self.llm = OllamaLLM(model="llama3.2:1b")
        elif llm_type == LLMType.GEMINI:
            self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=AI_API_KEYS.google_api_key)
        elif llm_type == LLMType.OPENAI:
            self.llm = ChatOpenAI(api_key=AI_API_KEYS.openai_api_key, model="gpt-4o")
        else:
            raise ValueError("Invalid LLMType")


    def _create_chain(self):
        self.prompt = PromptTemplate(
            template=load_prompt(),
            input_keys=["history", "prototype", "results", "input"]
        )

        self.memory = ConversationBufferWindowMemory(
                k=13,
                input_key="input",
            )

        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )


    def results(self, prototype:str, results:str, metric:str):
        self.results_dict["prototype"] = prototype
        self.results_dict["results"] = results
        self.results_dict["metric"] = metric


    def ask(self, input: str):
        ask_query_dict = self.results_dict.copy()
        ask_query_dict["input"] = input

        response = self.chain.invoke(ask_query_dict)

        return response
