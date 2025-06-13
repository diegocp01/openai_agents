# --- Imports ---
from agents import Agent, Runner
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Agent ---
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant",
    model="gpt-4.1-nano"
)

# --- Main --
# The main function runs the AI agent synchronously with a predefined prompt,
# asking it to write a haiku about recursion, and then prints the generated response.
def main():
    result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)

# --- Run ---
# This ensures that the main() function only runs when this script is executed directly,
# not when it is imported as a module in another file.
if __name__ == "__main__":
    main()