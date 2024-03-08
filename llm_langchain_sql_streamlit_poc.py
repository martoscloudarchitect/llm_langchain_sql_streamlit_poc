# Importing libraries

## Operating system dependent functionality. 
### The functions that the OS module provides allows you to interface with the underlying operating system that Python is running on – be that Windows, Mac or Linux.
import os
### The dotenv module is used to read the key-value pair from the .env file and add them to the environment variable.
from dotenv import load_dotenv
### The pathlib module offers classes representing filesystem paths with semantics appropriate for different operating systems.
from pathlib import Path
### Python Image Loader. The Image module provides a class with the same name which is used to represent a PIL image.
from PIL import Image

## Builing the frontend as web interface
import streamlit as st

## LLM Langchain as an orchestrator and mediator
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
#from langchain.chat_models import ChatOpenAI
from langchain_openai import AzureChatOpenAI


def main():

    # Loading Azure Open AI Resource environment variables from ".env" file outside the code under the same directory
    load_dotenv()

    ## The title() method is used to display the title of the web app top browser tab.
    st.title("AI SQL Assistant")
    ## The header() method is used to display the header of the web app page.
    st.header("Your SQL Database Mediator Assistant - POC Project")
    ## The text_input() method is used to take the input from the user.
    
    user_input = st.text_input("Enter your question")
    ## Create a variable to store the header for two tabs accessible by the user. 

    if user_input:
        # Creating an instance of AzureChatOpenAI
        llm = AzureChatOpenAI(
            deployment_name='gpt-4-deployment',
            openai_api_type="azure",
            temperature = 0
        )

        # Creating an instance of SQLDatabase pointing to a local database on the same resource location where application also exist.
        db = SQLDatabase.from_uri('sqlite:///chinook.db')

        # Creating an instance of SQLDatabaseToolkit
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # Creating an instance of AgentExecutor
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        
        tab_titles = ["Result","DB Schema Diagram"]
        tabs = st.tabs(tab_titles)

        with tabs[0]:
            st.write(agent_executor.invoke(user_input))

        # project root directory
        root_path = [p for p in Path(__file__).parents if p.parts[-1]=='llm_langchain_sql_streamlit_poc'][0]
        # Load image on the second tab
        diagram_ref = Image.open(f"{root_path}/images/sqlite-sample-database-color.jpg")   
        
        with tabs[1]:
            st.image(diagram_ref)

if __name__ == "__main__":
    main()