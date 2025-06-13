
# ==============================================================================
# This Agent is only a regular talk to ChatGPT, you send a prompt and get a response
# ==============================================================================


# --- Imports ---
from agents import Agent, Runner
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Agent ---
agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant", # This is the system prompt that tells the AI how to behave, change it if you want
    model="gpt-4.1-nano" # Change the model here
)

# --- Main --
# The main function runs the AI agent synchronously with a predefined prompt,
# asking it to write a haiku about recursion, and then prints the generated response.
def main():
    result = Runner.run_sync(agent, """
    Say: Hello my name is ChatGPT, this is a test. Now add something you will 
    like to tell the user. Your whole output is max 30 words.
    """) # This is the PROMPT
    print(result.final_output)

# --- Run ---
# This ensures that the main() function only runs when this script is executed directly,
# not when it is imported as a module in another file.
if __name__ == "__main__":
    main()