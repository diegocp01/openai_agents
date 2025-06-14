# Intro

This repository is a basic guide on how to build AI Agents using pyhton and OpenAI Agents SDK



*Optional:* Talk to an AI that knows this repository: https://huggingface.co/spaces/diegocp01/GPT-4.1

# Requirements

- OpenAI API Key (This has a cost attached to it, you will need a credit card, the good news is that is very cheap, model: GPT 4.1 mini. Input price: $0.40 / 1M tokens (like 'words') and $1.60 for 1M output) Get your key here -> https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://platform.openai.com/api-keys&ved=2ahUKEwi3m7vSg--NAxUzTTABHY5LJRcQFnoECCkQAQ&usg=AOvVaw1YhcGDWJXhiKSfmL59Pnfn


# Beginner friendly step by step

-Download Cursor, VS Code or Windsurf to your computer (Google it)
-Open your IDE (Cursor, Windsurf, VSCode) and then click on Open Folder (create a folder for this project)
-Go to the top left and chose Terminal -> New Terminal
- In the Terminal: copy and paste this + enter:
```bash
git clone https://github.com/diegocp01/openai_agents.git
```

Make sure your folder name on the left is the same as the terminal. (if not, take a screenshoot and ask chatgpt. Is a quick cd command)

-Create a new file inside of the openai-sdk-agent folder, called '.env'
-Inside of the .env file copy this:

```bash
# Copy and paste your openai api key below instead of the 'sk-12....'
OPENAI_API_KEY=sk-12232432

# The LLM to use find more llm names here
#https://platform.openai.com/docs/models
MODEL_CHOICE=gpt-4.1-nano
```

-In the Terminal: Install the required dependencies:
Create a virtual enviroment like this ->
```bash
python -m venv .venv
```
If your IDE asks you to create a python ENV click YES

-Then in the terminal paste this (This activates the enviroment): 
```bash
source .venv/bin/activate
```

-Now you will install the openai agents sdk and other frameworks needed
-(The frameworks are listed in the requirements file)
```bash
pip install -r requirements.txt
```

Then paste this in the terminal (with your openai key from .env file)
```bash
export OPENAI_API_KEY=sk-122
```


## Files

- `v1_basic_agent.py` - Basic Agent
- `v2_structured_output.py` - Agent with organized outputs
- `v3_tool_calls.py` - Agent with access to tools
- `v4_handoffs.py` - Orchestrator Agents with Specialized agents

# Running the Agents
## Basic Agent (v1)

Run the basic agent example:

```bash
python v1_basic_agent.py
```

## Structured Output Agent (v2)

Run the Agent with organized outputs:

```bash
python v2_structured_output.py
```

## Tool Calls Agent (v3)

Run the tool calls travel agent example:

```bash
python v3_tool_calls.py
```

Now we will give our agent some TOOLS! (This is when it gets fun!)
Recipe Agent

## Handoffs Agent (v4)

Run the Orchestrator Agents with Specialized agents

```bash
python v4_handoffs.py
```

## Run the interactive user interface app

```bash
streamlit run app.py
```


Youtube Video: https://youtu.be/w0D1R69LOjk
