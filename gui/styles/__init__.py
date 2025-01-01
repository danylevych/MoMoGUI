def load_window_style():
    with open("gui/styles/window_styles.qss", "r") as file:
        return file.read()

def load_ask_ai_style():
    with open("gui/styles/ask_ai_style.qss", "r") as file:
        return file.read()

def load_momo_agent_style():
    with open("gui/styles/momo_agent.qss", "r") as file:
        return file.read()
