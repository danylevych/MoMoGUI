from PyQt5.QtCore import QThread, pyqtSignal


class ChatbotWorker(QThread):
    """
    A worker thread that sends a user input to the agent and emits a signal with the response.
    """
    finished = pyqtSignal(str)

    def __init__(self, agent, user_input):
        """
        Initializes the ChatbotWorker.

        Parameters:
            agent (MoMoAgent): The agent to ask.
            user_input (str): The user input to send.
        """
        super().__init__()
        self.agent = agent
        self.user_input = user_input

    def run(self):
        """
        Runs the worker thread.
        """
        response = self.agent.ask(self.user_input)
        self.finished.emit(response)

