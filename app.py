# ==============================================================================
# Simple Streamlit Entertainment Agent App - Perfect for YouTube Tutorial!
# ==============================================================================

import streamlit as st
import asyncio
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Entertainment Helper",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for beautiful gradient background and styling
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 25%, #74b9ff 50%, #0984e3 75%, #6c5ce7 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    /* Gradient animation */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle styling */
    .stApp > div > div > div > div > div:nth-child(2) p {
        color: rgba(255, 255, 255, 0.9) !important;
        text-align: center;
        font-size: 1.2rem !important;
        margin-bottom: 2rem !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: black !important;
        font-size: 1.1rem !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.6) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #00b894, #00cec9) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px 0 rgba(31, 38, 135, 0.6) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .sidebar .sidebar-content {
        background: transparent !important;
    }
    
    /* Sidebar text - Multiple selectors to ensure it works */
    .css-1d391kg h1, 
    .css-1d391kg h2, 
    .css-1d391kg h3, 
    .css-1d391kg h4,
    .css-1d391kg p,
    .css-1d391kg div,
    .css-1d391kg span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stSuccess > div, .stInfo > div, .stWarning > div {
        color: white !important;
    }
    
    /* Column content */
    .element-container h3, .element-container p, .element-container div {
        color: white !important;
    }
    
    /* Markdown text */
    .stMarkdown p, .stMarkdown li {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Footer */
    .stMarkdown em {
        color: rgba(255, 255, 255, 0.7) !important;
        text-align: center;
    }
    
    /* Spinner */
    .stSpinner {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

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

# --- Initialize Agents (only once) ---

@st.cache_resource
def initialize_agents():
    """Initialize agents once and cache them."""
    
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
    
    return entertainment_agent

# --- Helper Functions ---

async def get_recommendation(query: str):
    """Get recommendation from the entertainment agent."""
    entertainment_agent = initialize_agents()
    result = await Runner.run(entertainment_agent, query)
    return result

def display_book_recommendation(book):
    """Display book recommendation in a nice format."""
    st.success("📚 Book Recommendation Found!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📖 Book Details")
        st.write(f"**Title:** {book.title}")
        st.write(f"**Author:** {book.author}")
        st.write(f"**Genre:** {book.genre}")
        st.write(f"**Reading Time:** {book.reading_time_hours} hours")
    
    with col2:
        st.subheader("💡 Why This Book?")
        st.write(book.reason)

def display_movie_recommendation(movie):
    """Display movie recommendation in a nice format."""
    st.success("🎬 Movie Recommendation Found!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎭 Movie Details")
        st.write(f"**Title:** {movie.title}")
        st.write(f"**Director:** {movie.director}")
        st.write(f"**Genre:** {movie.genre}")
        st.write(f"**Duration:** {movie.duration_minutes} minutes")
    
    with col2:
        st.subheader("💡 Why This Movie?")
        st.write(movie.reason)

def display_general_plan(plan):
    """Display general entertainment plan."""
    st.info("🎯 Entertainment Suggestion")
    st.write(f"**Activity:** {plan.activity_type}")
    st.write(f"**Recommendation:** {plan.recommendation}")
    st.write(f"**Time Needed:** {plan.time_needed}")
    st.write(f"**Why This Choice:** {plan.why_chosen}")

# --- Main Streamlit App ---

def main():
    # Title and header
    st.title("🎬 Entertainment Helper")
    st.write("Get personalized book and movie recommendations!")
    
    # Sidebar with examples
    st.sidebar.header("💡 Try These Examples:")
    st.sidebar.write("• I want to read a mystery book")
    st.sidebar.write("• Recommend a funny movie")
    st.sidebar.write("• What should I watch tonight?")
    st.sidebar.write("• I need a good fantasy book")
    
    # Main input
    user_query = st.text_input(
        "What kind of entertainment are you looking for?",
        placeholder="e.g., I want to read a good mystery book"
    )
    
    # Submit button
    if st.button("Get Recommendation", type="primary"):
        if user_query:
            with st.spinner("Finding the perfect recommendation for you..."):
                try:
                    # Get recommendation
                    result = asyncio.run(get_recommendation(user_query))
                    
                    # Show handoff information
                    if hasattr(result.final_output, "title") and hasattr(result.final_output, "author"):
                        st.info("🔄 Handed off to: Book Specialist")
                        display_book_recommendation(result.final_output)
                    elif hasattr(result.final_output, "title") and hasattr(result.final_output, "director"):
                        st.info("🔄 Handed off to: Movie Specialist")
                        display_movie_recommendation(result.final_output)
                    else:
                        st.info("🔄 Handled by: Main Entertainment Agent")
                        display_general_plan(result.final_output)
                        
                except Exception as e:
                    st.error(f"Sorry, something went wrong: {str(e)}")
        else:
            st.warning("Please enter a question or request!")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit and Open AI Agents* 🤖")

if __name__ == "__main__":
    main()