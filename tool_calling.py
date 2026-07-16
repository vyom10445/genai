from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from rich import print
from langchain_core.messages import HumanMessage

#step 1 :tool creation

@tool
def get_text_length(text : str) -> int :
    """returns the number of characters in a given text"""
    return len(text)

llm = ChatOpenAI(model= "gpt-4o")



# step 2 : tool binding
llm_with_tool = llm.bind_tools([get_text_length])


message = []

query  = HumanMessage("Return the number of characters in the given text : 'Hello how are you' ")
message.append(query)

result = llm_with_tool.invoke(message)
message.append(result)


if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]



