def load_prompt():
    """
    Return the prompt of the assistant.
    """
    with open('src/assistant/prompt.prm', 'r') as file:
        return file.read()
