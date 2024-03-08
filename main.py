import os
from dotenv import load_dotenv

# LLM Langchain as an orchestrator and mediator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureOpenAI
from langchain_core.output_parsers import StrOutputParser

## Interacting with structured data
import sqlite3
import pandas as pd
import json

load_dotenv()

# Accessing environment variables
os.environ["OPENAI_API_TYPE"] 
os.environ["OPENAI_API_VERSION"] 
os.environ["AZURE_OPENAI_ENDPOINT"] 
os.environ["OPENAI_API_KEY"] 
os.environ["AZURE_COGS_KEY"] 
os.environ["AZURE_COGS_ENDPOINT"] 
os.environ["AZURE_COGS_REGION"]


# Creating the main components of the chain

# Component #1 - Connection to the Database and read the schema
## Defines the name of the database as a variable
database = 'chinook.db'
## Database Connector to SQLlite
dbconn = sqlite3.connect(database)

## Reads the schema of SQLLite database
c = dbconn.cursor()

# Get the list of all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

# Initialize an empty dictionary to hold the schema
dbschema = {}

# For each table, get the schema
for table in tables:
    table = table[0]
    c.execute(f"PRAGMA table_info({table})")
    # Get the schema of the table
    table_info = c.fetchall()
    # Format the schema as a dictionary where the keys are the column names and the values are the types
    dbschema[table] = {column[1]: column[2] for column in table_info}

# Save the schema as a JSON file
with open('schema.json', 'w') as f:
    json.dump(dbschema, f)

# Component #2 - Create a prompt template
prompt_template = """
Based on the table schema below, write a SQL Query that would answer the user's questions.
{schema}

Question: {question}
SQL Query:
"""
prompt = ChatPromptTemplate.from_template(prompt_template)
prompt.format(schema="my schema", question="how many tables are in the database?")

# Component #3 - Create a chain that uses this prompt
llm = AzureOpenAI(
    deployment_name='gpt-4-deployment',
    #openai_api_type=os.environ["OPENAI_API_TYPE"],
    openai_api_type='azure',
    temperature=0
)

sql_chain = (
    RunnablePassthrough.assign(schema=dbschema)
    | prompt
    | llm.blind(stop="\nSQL_Result:")
    | StrOutputParser()
)

sql_chain.invoke({"question": "What are the names of the tables in the database?"})