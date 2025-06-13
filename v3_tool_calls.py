
# ==============================================================================
# Now we will give our agent some TOOLS! (This is when it gets fun!)
# Recipe Agent
# ==============================================================================

import asyncio
import json
from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

model = os.getenv('MODEL_CHOICE', 'gpt-4.1-nano')

# --- Models for structured outputs ---

class RecipeRecommendation(BaseModel):
    recipe_name: str
    cooking_time_minutes: int
    difficulty_level: str = Field(description="Easy, Medium, or Hard")
    ingredients: List[str] = Field(description="List of ingredients needed")
    instructions: str = Field(description="Simple cooking instructions")

# --- Tools ---
# Here is a simple python function called get_ingredient_info, you can experiment with chatgpt
@function_tool
def get_ingredient_info(ingredient: str) -> str:
    """Get basic information about a cooking ingredient including tips."""
    # Simple ingredient database
    ingredient_info = {
        "chicken": "High in protein, cook to 165°F internal temperature. Great for beginners!",
        "pasta": "Quick cooking staple, usually takes 8-12 minutes to boil. Very beginner-friendly!",
        "rice": "Versatile grain, use 2:1 water to rice ratio. Perfect for meal prep!",
        "eggs": "Protein-rich and versatile. Can be scrambled, fried, or boiled. Great for any skill level!",
        "tomatoes": "Rich in vitamins, great fresh or cooked. Add to almost any dish!",
        "cheese": "Adds flavor and richness. Melt easily, store in refrigerator.",
        "bread": "Carb base for many meals. Toast for extra flavor and texture.",
        "potatoes": "Filling and versatile. Can be baked, fried, or boiled. Very budget-friendly!"
    }
    
    ingredient_lower = ingredient.lower()
    if ingredient_lower in ingredient_info:
        return f"{ingredient.title()}: {ingredient_info[ingredient_lower]}"
    else:
        return f"{ingredient.title()}: This is a great ingredient to experiment with in cooking!"

# --- Main Recipe Agent ---

recipe_agent = Agent(
    name="Recipe Helper",
    instructions="""
    You are a friendly cooking assistant that helps beginners find simple, delicious recipes.
    
    You can:
    1. Recommend easy recipes based on what ingredients someone has
    2. Provide helpful information about ingredients
    
    Always be encouraging and supportive! Keep recipes simple and beginner-friendly.
    Focus on recipes that:
    - Use common ingredients
    - Have clear, simple steps
    - Take 30 minutes or less
    - Are hard to mess up
    
    Be enthusiastic about cooking and help build confidence in the kitchen!
    """,
    model=model,
    tools=[get_ingredient_info],
    output_type=RecipeRecommendation
)

# --- Main Function ---

async def main():
    # Example queries to test the system
    queries = [
        "I have chicken and rice at home. What's an easy recipe I can make?",
        "I'm a complete beginner and only have eggs and bread. Help me make something simple!"
    ]
    
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        
        result = await Runner.run(recipe_agent, query)
        
        print("\nFINAL RESPONSE:")
        recipe = result.final_output
        
        # Format the output in a nice way
        print(f"\n🍳 RECIPE RECOMMENDATION: {recipe.recipe_name.upper()} 🍳")
        print(f"⏰ Cooking Time: {recipe.cooking_time_minutes} minutes")
        print(f"📊 Difficulty: {recipe.difficulty_level}")
        
        print("\n🛒 INGREDIENTS:")
        for i, ingredient in enumerate(recipe.ingredients, 1):
            print(f"  {i}. {ingredient}")
        
        print(f"\n👨‍🍳 INSTRUCTIONS:\n{recipe.instructions}")

if __name__ == "__main__":
    asyncio.run(main())
