from langchain.tools import tool

@tool #decorator for creating tool
def get_greetings(name : str) -> str : #type hints
    """generate a greeting message for user"""  #docstring
    return f"Hello {name} ! Welcome to the AI world"


result = get_greetings.invoke({"name" : "Vyom"})

print(result)