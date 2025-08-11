from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

class LLMService:
    def __init__(self, api_key: str):
        # Initialize the ChatGroq model with the provided API key
        # We use a popular and capable model like Llama 3
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama3-70b-8192",
            temperature=0.7
        )

        # Define the system prompt and human message template
        system_prompt = "You are a helpful and witty assistant. Answer the user's question concisely."
        human_template = "{user_input}"

        # Create the prompt template from the messages
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_template)
        ])

        # Create the conversational chain by piping the components together
        self.chain = self.prompt | self.llm | StrOutputParser()

    def invoke(self, user_input: str) -> str:
        """
        Invokes the LLM chain with the user's input.
        """
        return self.chain.invoke({"user_input": user_input})