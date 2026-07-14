from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from rich import print

#step 1 :tool creation

@tool
def get_text_length(text : str) -> int :
    """returns the number of characters in a given text"""
    return len(text)

llm = ChatOpenAI(model= "gpt-4o")



# step 2 : tool binding
llm_with_tool = llm.bind_tools([get_text_length])





