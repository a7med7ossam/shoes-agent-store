# SoleAgent Setup Guide

## Step 1: Install the Prerequisites
On the new laptop, download and install:

* **Git:** To download your code from GitHub.
* **Docker Desktop:** To run your containers.
* **Ollama:** To run your local LLM.

## Step 2: Start Ollama
Open a terminal on the new laptop and download the "brain" for your agent:

` ` `bash
ollama pull llama3.1:8b
ollama serve
` ` `

## Step 3: Download Your Code
Open a new terminal window and download your project from GitHub:

` ` `bash
git clone <https://github.com/a7med7ossam/shoes-agent-store.git>
cd shoes-agent-store
` ` `

## Step 4: The Magic Command
Now, run the single command that reads your `docker-compose.yml` and builds everything from scratch:

` ` `bash
docker compose up --build -d
` ` `

### What happens next is entirely automated by Docker:

1. It downloads Python 3.12.
2. It reads `requirements.txt` and installs FastAPI, Streamlit, LangGraph, etc.
3. It downloads PostgreSQL 16 and Qdrant.
4. It boots up the database.
5. It runs `database.py`, reads your `shoes_inventory.csv`, and injects all 370 shoes into the fresh database.
6. It starts FastAPI and Streamlit.

Once your terminal says the containers are "Started", you just open your browser to http://localhost:8501 on the new laptop, and your SoleAgent is ready to take orders!
