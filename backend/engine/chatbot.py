import pandas as pd
from langchain_openai import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Load your CSV
df = pd.read_csv("financial_data.csv")

# Initialize LLM
llm = OpenAI(api_key="AIzaSyCY2kE80M4xDZ9d2WN7zsDzaVAU-aCrTi8", temperature=0)

# Create agent
agent = create_pandas_dataframe_agent(llm, df, verbose=True)

# Ask financial questions
print(agent.run("Who has the highest debt?"))
print(agent.run("What is the average spending?"))
print(agent.run("If income increases by 10%, how much will John save?"))