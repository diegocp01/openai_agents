# Intro

This repository is a basic guide on how to build AI Agents using pyhton and OpenAI Agents SDK

# Requirements

- OpenAI API Key (This has a cost attached to it, you will need a credit card, the good news is that is very cheap, model: GPT 4.1 mini. Input price: $0.40 / 1M tokens (like 'words') and $1.60 for 1M output) Get your key here -> https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://platform.openai.com/api-keys&ved=2ahUKEwi3m7vSg--NAxUzTTABHY5LJRcQFnoECCkQAQ&usg=AOvVaw1YhcGDWJXhiKSfmL59Pnfn


# Beginner friendly step by step

-Download Cursor, VS Code or Windsurf to your computer (Google it)
-Open your IDE (Cursor, Windsurf, VSCode) and then click on Open Folder (create a folder for this project)
-Go to the top left and chose Terminal -> New Terminal
- In the Terminal: copy and paste this:
```bash
git clone https://github.com/diegocp01/openai_agents.git
```

Make sure your folder name on the left is the same as the terminal. (if not, take a screenshoot and ask chatgpt. Is a quick cd command)

- Create a new file inside of the openai-sdk-agent folder, called '.env'
-Inside of the .env file copy this:

```bash
# Copy and paste your openai api key below instead of the 'sk-12....'
OPENAI_API_KEY=sk-12232432

# The LLM to use find more llm names here
#https://platform.openai.com/docs/models
MODEL_CHOICE=gpt-4.1-nano
```

1. In the Terminal: Install the required dependencies:

```bash
python -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
export OPENAI_API_KEY=sk-...
```

2. Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
MODEL_CHOICE=gpt-4o-mini  # or another model of your choice
```

## Files

- `v1_basic_agent.py` - Basic Agent
- `v2_structured_output.py` - Agent with organized outputs
- `v3_tool_calls.py` - Agent with access to tools
- `v4_handoffs.py` - Orchestrator Agents with Specialized agents


## Streamlit

```bash
streamlit run v1_basic_agent_streamlit.py
```
## Running the Examples

### Basic Agent (v1)

Run the basic agent example:

```bash
python v1_basic_agent.py
```

This will execute a simple agent that generates a haiku about recursion.

### Structured Output Agent (v2)

Run the structured output travel agent example:

```bash
python v2_structured_output.py
```

This demonstrates using Pydantic models to create structured travel plans with destinations, activities, and budget information.

### Tool Calls Agent (v3)

Run the tool calls travel agent example:

```bash
python v3_tool_calls.py
```

This version adds a weather forecasting tool to provide weather information for travel destinations.

### Handoffs Agent (v4)

Run the handoffs travel agent example:

```bash
python v4_handoffs.py
```

This version introduces specialized sub-agents for flight and hotel recommendations, demonstrating agent handoffs.

### Guardrails and Context Agent (v5)

Run the guardrails and context travel agent example:

```bash
python v5_guardrails_and_context.py
```

This version adds:
- Budget analysis guardrails to validate if a travel budget is realistic
- User context to store and use preferences like preferred airlines and hotel amenities

[Optional] Follow the [Logfire setup intructions](https://logfire.pydantic.dev/docs/#logfire) (free to get started) for tracing in this version and version 6. This example will still work with Logfire configured but you won't get tracing.

### Streamlit Chat Interface (v6)

Launch the Streamlit web interface:

```bash
streamlit run v6_streamlit_agent.py
```

This will start a web server and open a browser window with the travel agent chat interface. Features include:

- Persistent chat history within a session
- User preference management in the sidebar
- Beautifully formatted responses for different types of travel information
- Support for conversation memory across multiple turns

## Environment Variables

The following environment variables can be configured in your `.env` file:

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `MODEL_CHOICE` (optional): The OpenAI model to use (default: gpt-4o-mini)

## Features Demonstrated

1. **Basic Agent Configuration (v1)**
   - Instructions and model settings
   - Simple agent execution

2. **Structured Output (v2)**
   - Using Pydantic models for structured responses
   - Travel planning with organized information

3. **Tool Calls (v3)**
   - Custom tools for retrieving external data
   - Weather forecasting integration

4. **Agent Handoffs (v4)**
   - Specialized agents for flights and hotels
   - Delegation to domain-specific experts

5. **Guardrails and Context (v5)**
   - Input validation with budget guardrails
   - User context for personalized recommendations
   - Preference-based sorting of results

6. **Chat Interface (v6)**
   - Conversation history and context
   - User preference management
   - Formatted responses for different output types
   - Thread management for persistent conversations

## Notes

This is a demonstration project and uses simulated data for weather, flights, and hotels. In a production environment, you would integrate with real APIs for this information.
