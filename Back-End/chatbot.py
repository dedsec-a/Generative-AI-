from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import BaseTool
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(temperature=0.7, model="gpt-4")

# 🛫 Dummy tool: Simulates a flight search
def search_flights(destination, days):
    return f"Found flights to {destination} on May 10, return after {days} days. Price: ₹5,200."

# 🏨 Dummy tool: Simulates a hotel search
def search_hotels(destination, days):
    return f"Found hotel 'Snow Valley Resort' in {destination} for {days} nights. ₹1,800/night."

# 🗓️ Dummy itinerary planner
def generate_itinerary(destination, days):
    return "\n".join([f"Day {i+1}: Explore {destination} sightseeing" for i in range(days)])

# Wrapping the tools
tools = [
    Tool(name="Flight Search",
         func=lambda x: search_flights(x.split(',')[0], int(x.split(',')[1])),
         description="Use this to find flights. Input format: 'Destination,Days'"),
    
    Tool(name="Hotel Search",
         func=lambda x: search_hotels(x.split(',')[0], int(x.split(',')[1])),
         description="Use this to find hotels. Input format: 'Destination,Days'"),

    Tool(name="Itinerary Planner",
         func=lambda x: generate_itinerary(x.split(',')[0], int(x.split(',')[1])),
         description="Creates a travel itinerary. Input format: 'Destination,Days'")
]

# Create the agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 🎯 Sample task
response = agent.run("Plan a 5-day budget trip to Manali in May")
print(response)
