from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model = "gpt-5")

response = model.invoke("what is langchain?")

print(response.content)