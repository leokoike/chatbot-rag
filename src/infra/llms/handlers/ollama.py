from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from src.domain.llm import LLM


class BasicChatOllama(LLM):
    def __init__(self):
        self.template = "Você é um assistente virtual que responde perguntas em geral."
        self.prompt = ChatPromptTemplate(
            [
                (
                    "system",
                    "Você é um assistente virtual chamado AINokode. Responda as perguntas fornecidas de modo direto e usando no máximo 3 frases.",
                ),
                ("user", "{input}"),
            ]
        )
        self.llm = ChatOllama(
            base_url="http://127.0.0.1:11434",
            model="llama3.2",
        )
        self.chain = self.prompt | self.llm

    async def invoke(self, query):
        message = await self.chain.ainvoke({"input": query})
        print(f"{__file__}: {message}")

        return message.content
