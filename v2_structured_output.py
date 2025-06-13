
# ==============================================================================
# Now we will tell our Agent how to structure it's response
# Travel Agent
# ==============================================================================

# Imports
import asyncio
from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

model = os.getenv('MODEL_CHOICE', 'gpt-4o-mini')

# --- Models for structured outputs ---
# This is a template for the Agent's response
class TravelPlan(BaseModel):
    destination: str # str -> text
    duration_days: int # int -> whole numbers
    budget: float # float -> decimal numbers
    activities: List[str] = Field(description="List of recommended activities")
    notes: str = Field(description="Additional notes or recommendations")

# --- Main Travel Agent ---

travel_agent = Agent(
    name="Travel Planner",
    instructions="""
    You are a travel assistant that helps users plan their trip.
    
    You can create personalized travel itineraries based on the user's interests and preferences.
    
    Always be helpful, informative, and enthusiastic about travel. Provide specific recommendations
    based on the user's interests and preferences.
    
    When creating travel plans, consider:
    - Local attractions and activities
    - Budget constraints
    - Travel duration
    """,
    model=model,
    output_type=TravelPlan # Here we are telling the agent: use this TravelPlan template 
)

# --- Main Function ---
# Defines the main asynchronous function to run multiple travel agent queries concurrently.
# It uses 'await' to handle agent responses without blocking the program.
async def main():
    # Example queries to test the system
    queries = [
        "I'm planning a trip to Dubai for 5 days with a budget of $5000. What should I do there?",
        "I want to visit London for a week with a budget of $2000. What activities do you recommend?"
    ]
    # Iterates through each query, running the travel agent for each one.
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        # Runs the travel agent with the current query and waits for the result.
        result = await Runner.run(travel_agent, query)
        # Prints the final output of the travel plan.
        print("\nFINAL RESPONSE:")
        travel_plan = result.final_output
        
        # Format the output in a nicer way
        print(f"\n🌍 TRAVEL PLAN FOR {travel_plan.destination.upper()} 🌍")
        print(f"Duration: {travel_plan.duration_days} days")
        print(f"Budget: ${travel_plan.budget}")
        # Loops through each activity and prints it with a number, starting from 1.
        print("\n🎯 RECOMMENDED ACTIVITIES:")
        for i, activity in enumerate(travel_plan.activities, 1):
            print(f"  {i}. {activity}")
        # Prints any additional notes.
        print(f"\n📝 NOTES: {travel_plan.notes}")

if __name__ == "__main__":
    asyncio.run(main())
