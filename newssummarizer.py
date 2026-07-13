from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool = TavilySearchResults(max_results=5)

llm = ChatOpenAI(model="gpt-5")

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant .
                                          
Summarize the following news into clear bullet points

{news}                                          
""")



chain = prompt | llm | StrOutputParser()

news_results = search_tool.run("Latest AI news of 2026")

result = chain.invoke({"news" : news_results})

print(result)