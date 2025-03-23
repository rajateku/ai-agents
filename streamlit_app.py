import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import pandas as pd
import re

# Load environment variables
load_dotenv()

# Initialize the web agent
web_agent = Agent(
    name="Web Agent",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources and format the response as a numbered list"],
    show_tool_calls=True,
    markdown=True,
)

# Set up the Streamlit page
st.set_page_config(
    page_title="AI Web Search Agent",
    page_icon="🔍",
    layout="wide"
)

# Add a title and description
st.title("🔍 AI Web Search Agent")
st.markdown("""
This app uses an AI agent to search the web and provide detailed answers to your questions.
The agent will always include sources for its information.
""")

# Create a text input for the user's query
user_query = st.text_input("Enter your question:", placeholder="e.g., Give 10 AI companies that I can apply for jobs in Munich")

# Add a search button
if st.button("Search"):
    if user_query:
        # Create a placeholder for the response
        response_placeholder = st.empty()
        
        # Get the response from the agent and convert to string
        response = str(web_agent.run(user_query))
        
        # Display the raw response in an expander
        with st.expander("Raw Response"):
            st.markdown(response)
        
        # Try to extract numbered items from the response
        items = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', response, re.DOTALL)
        
        if items:
            # Create a DataFrame for the table
            df = pd.DataFrame({
                'Item': [item.strip() for item in items]
            })
            
            # Display the table
            st.subheader("Structured Results")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No structured data found in the response. Showing raw response only.")
            
    else:
        st.warning("Please enter a question to search.") 