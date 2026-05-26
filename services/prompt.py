from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are smart document analyzer.

RULES:
- Use the provided context to answer.
- Only answer from the given context.
- If the context is not relevant, say context is not relevant.
- keep the answer short and focused.
"""
    ),
    MessagesPlaceholder(variable_name = "chat_history"),
    (
        "human",
        """
Context:
{context}

Question:
{question}
"""
)])