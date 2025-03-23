import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOpenAI(model="gpt-4o-mini")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools. 
            Wrap the output in this format and provide no other text
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentEx    ecutor(agent=agent, tools=tools, verbose=True)

st.title("AI Research Assistant")
query = st.text_input("What can I help you research?")
if st.button("Search") and query:
    with st.spinner("Fetching research..."):
        raw_response = agent_executor.invoke({"query": query})
        
        try:
            structured_response = parser.parse(raw_response.get("output"))
            st.subheader("Topic:")
            st.write(structured_response.topic)
            st.subheader("Summary:")
            st.write(structured_response.summary)
            st.subheader("Sources:")
            st.write("\n".join(structured_response.sources))
            st.subheader("Tools Used:")
            st.write(", ".join(structured_response.tools_used))
        except Exception as e:
            # st.error(f"Error parsing response: {e}")
            st.write("Raw Response:", raw_response)