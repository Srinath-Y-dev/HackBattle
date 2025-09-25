import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent


api_key = "YOUR_OPENAI_API_KEY" 

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Load data and create the LangChain agent (this runs only once when the server starts)
try:
    df = pd.read_csv("financial_data.csv")
    llm = OpenAI(api_key=api_key, temperature=0)
    # The agent is now initialized globally for the app
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, handle_parsing_errors=True)
    print("Agent initialized successfully.")
except Exception as e:
    print(f"Error initializing agent: {e}")
    agent = None

# Define an API endpoint for asking questions
@app.route('/ask', methods=['POST'])
def ask_agent():
    if agent is None:
        return jsonify({"error": "Agent not initialized"}), 500

    # Get the question from the incoming JSON request
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Run the agent with the user's question
        print(f"Received question: {question}")
        answer = agent.run(question)
        print(f"Agent's answer: {answer}")
        return jsonify({'answer': str(answer)}) # Convert answer to string to ensure it's JSON serializable
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)