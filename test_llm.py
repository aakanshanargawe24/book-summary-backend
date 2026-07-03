from app.clients.llm import LLM

llm = LLM()

response = llm.generate("Say hello in one sentence.")

print(response)