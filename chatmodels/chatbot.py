from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage , AIMessage , HumanMessage

from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    model="mistral-small-2506"
)



print("chosse your AI mode")
print("press 1 for Angry mode")
print("press 2 for funny mode ")
print("press 3 for sad mode")

choice = int(input("tell your response :- "))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are a very sad AI agent. You respond in a depressed and emotional tone."

messages = [
    SystemMessage(content=mode)
]

print("Welcome! Press 0 to exit")
while True:

    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt=="0":
        break

    response = llm.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Bot: ",response.content)


print(messages)