from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo 
import openai
from dotenv import load_dotenv
import os

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = os.getenv("GROQ_API_KEY")

model = OpenAIChat(id="gpt-4o-mini")

financial_agent = Agent(
    name= "Financial Analyst",
    model=model,
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True,
         ), 
    ],
    instructions="Use tables to display data",
    show_tool_calls=True,
    markdown=True,
   )    

web_Search_agent= Agent(
    name  = "Web Search Agent",
    role  = "You are a web search agent that can search the web for information using DuckDuckGo.",
    model = model,
    tools=[DuckDuckGo() ],
    instructions="Always include sources in your answers" ,
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent = Agent(
    team = [financial_agent, web_Search_agent],
    instructions = ["Always include sources in your answers", "Use tables to display data"],
    show_tool_calls = True,
    markdown = True,        
)

def run_chat():
    print("💬 Financial Analyst Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break

        try:
            response = multi_ai_agent.run(user_input)
            print(f"\nAI: {response.content}\n")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    run_chat()
