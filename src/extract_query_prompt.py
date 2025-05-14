from langchain_core.prompts import ChatPromptTemplate

extract_query_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Pokémon search assistant. Extract structured info from user queries."),
    ("human", "User query: {query}\n\nReturn a JSON object with these keys:\n- game\n- pokemon\n- intent (e.g., how to catch, where to find, stats, moves, etc.)")
])
