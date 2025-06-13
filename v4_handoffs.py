
# ==============================================================================
# Now we have a main agent and 2 specialized agents
# Entertainment Agents
# ==============================================================================

import asyncio
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

model = os.getenv('MODEL_CHOICE', 'gpt-4.1-nano')

# --- Models for structured outputs ---

class BookRecommendation(BaseModel):
    title: str
    author: str
    genre: str
    reading_time_hours: int
    reason: str = Field(description="Why this book is recommended")

class MovieRecommendation(BaseModel):
    title: str
    director: str
    genre: str
    duration_minutes: int
    reason: str = Field(description="Why this movie is recommended")

class EntertainmentPlan(BaseModel):
    activity_type: str
    recommendation: str
    time_needed: str
    why_chosen: str

# --- Tools ---

@function_tool
def get_book_info(genre: str) -> str:
    """Get information about popular books in a specific genre."""
    book_database = {
        "mystery": [
            {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "hours": 15},
            {"title": "Gone Girl", "author": "Gillian Flynn", "hours": 12}
        ],
        "romance": [
            {"title": "Pride and Prejudice", "author": "Jane Austen", "hours": 10},
            {"title": "The Notebook", "author": "Nicholas Sparks", "hours": 8}
        ],
        "fantasy": [
            {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "hours": 9},
            {"title": "The Hobbit", "author": "J.R.R. Tolkien", "hours": 11}
        ]
    }
    
    if genre.lower() in book_database:
        books = book_database[genre.lower()]
        return json.dumps(books)
    else:
        return "Genre not found in our database."

@function_tool
def get_movie_info(genre: str) -> str:
    """Get information about popular movies in a specific genre."""
    movie_database = {
        "comedy": [
            {"title": "The Grand Budapest Hotel", "director": "Wes Anderson", "minutes": 99},
            {"title": "Superbad", "director": "Greg Mottola", "minutes": 113}
        ],
        "action": [
            {"title": "Mad Max: Fury Road", "director": "George Miller", "minutes": 120},
            {"title": "John Wick", "director": "Chad Stahelski", "minutes": 101}
        ],
        "drama": [
            {"title": "The Shawshank Redemption", "director": "Frank Darabont", "minutes": 142},
            {"title": "Forrest Gump", "director": "Robert Zemeckis", "minutes": 142}
        ]
    }
    
    if genre.lower() in movie_database:
        movies = movie_database[genre.lower()]
        return json.dumps(movies)
    else:
        return "Genre not found in our database."

# --- Specialized Agents ---

book_agent = Agent(
    name="Book Specialist",
    handoff_description="Expert who recommends books based on your preferences",
    instructions="""
    You are a friendly book specialist who loves helping people find their next great read!
    
    Use the get_book_info tool to find books in the genre the user wants.
    Pick the best option and explain why it's perfect for them.
    
    Be enthusiastic about reading and make the person excited to start their book!
    """,
    model=model,
    tools=[get_book_info],
    output_type=BookRecommendation
)

movie_agent = Agent(
    name="Movie Specialist", 
    handoff_description="Expert who recommends movies based on your preferences",
    instructions="""
    You are a movie buff who loves helping people find the perfect film to watch!
    
    Use the get_movie_info tool to find movies in the genre the user wants.
    Pick the best option and explain why they'll love it.
    
    Be exciting about movies and make them want to grab popcorn and start watching!
    """,
    model=model,
    tools=[get_movie_info],
    output_type=MovieRecommendation
)

# --- Main Entertainment Agent ---

entertainment_agent = Agent(
    name="Entertainment Helper",
    instructions="""
    You are a friendly entertainment assistant who helps people decide what to do in their free time!
    
    You can help with:
    1. General entertainment advice
    2. Hand off to book specialist for book recommendations
    3. Hand off to movie specialist for movie recommendations
    
    Be enthusiastic and helpful! When someone asks specifically about books or movies, 
    hand them off to the right specialist.
    
    For general questions, give friendly advice about entertainment options.
    """,
    model=model,
    tools=[],
    handoffs=[book_agent, movie_agent],
    output_type=EntertainmentPlan
)


# --- Main Function ---

async def main():
    # Example queries to test the system
    queries = [
        "I want to read a good mystery book",
        "Recommend me a funny movie to watch tonight"
    ]
    
    for query in queries:
        print("\n" + "="*50)
        print(f"QUERY: {query}")
        
        result = await Runner.run(entertainment_agent, query)
        
        # Print handoff information if available
        if hasattr(result, 'messages') and result.messages:
            for message in result.messages:
                if hasattr(message, 'role') and message.role == 'assistant':
                    if 'handoff' in str(message).lower() or any(agent_name in str(message) for agent_name in ['Book Specialist', 'Movie Specialist']):
                        print(f"\n🔄 HANDED OFF TO: {message.sender if hasattr(message, 'sender') else 'Specialist Agent'}")
        
        # Check if we can detect handoff from the result structure
        if hasattr(result.final_output, "title") and hasattr(result.final_output, "author"):
            print("\n🔄 HANDED OFF TO: Book Specialist")
        elif hasattr(result.final_output, "title") and hasattr(result.final_output, "director"):
            print("\n🔄 HANDED OFF TO: Movie Specialist")
        
        print("\nFINAL RESPONSE:")
        
        # Format output based on response type
        if hasattr(result.final_output, "title") and hasattr(result.final_output, "author"):  # Book
            book = result.final_output
            print("\n📚 BOOK RECOMMENDATION 📚")
            print(f"Title: {book.title}")
            print(f"Author: {book.author}")
            print(f"Genre: {book.genre}")
            print(f"Reading Time: {book.reading_time_hours} hours")
            print(f"\n💡 Why this book: {book.reason}")
            
        elif hasattr(result.final_output, "title") and hasattr(result.final_output, "director"):  # Movie
            movie = result.final_output
            print("\n🎬 MOVIE RECOMMENDATION 🎬")
            print(f"Title: {movie.title}")
            print(f"Director: {movie.director}")
            print(f"Genre: {movie.genre}")
            print(f"Duration: {movie.duration_minutes} minutes")
            print(f"\n💡 Why this movie: {movie.reason}")
            
        else:  # General entertainment plan
            plan = result.final_output
            print("\n🎯 ENTERTAINMENT SUGGESTION 🎯")
            print(f"Activity: {plan.activity_type}")
            print(f"Recommendation: {plan.recommendation}")
            print(f"Time Needed: {plan.time_needed}")
            print(f"\n💡 Why this choice: {plan.why_chosen}")

if __name__ == "__main__":
    asyncio.run(main())