# SoleAgent Setup Guide

## Step 1: Install the Prerequisites
On the new laptop, download and install:

* **Git:** To download your code from GitHub.
* **Docker Desktop:** To run your containers.
* **Ollama:** To run your local LLM.

Install Docker:

- Git for Windows (Git Bash)
- Docker Desktop
- kubectl
- kind

Quick install with PowerShell (Admin):

```powershell
winget install --id Git.Git -e
winget install --id Docker.DockerDesktop -e
winget install --id Kubernetes.kubectl -e
winget install --id Kubernetes.kind -e
```

Verify in Git Bash:

```bash
git --version
docker --version
kubectl version --client
kind version
```

Install Ollama:
On the new laptop, Insert the USB Flash Drive:

1. Copy `Ollama_Local_Models` folder into a drive that has 5GB free.
2. Copy `OllamaSetup.exe` into your disk and install it in any directory (C: D: E:).
3. While opening `OllamaSetup.exe` configure model location under settings, click browse and choose the path to your `Ollama_Local_Models` folder.

## Step 2: Start Ollama
Open a terminal on the new laptop and download the "brain" for your agent:

```bash
ollama pull llama3.1:8b
#ollama serve
#because it's always running 
```


## Step 3: Download Your Code
Open a new terminal window and download your project from GitHub:

```bash
git clone https://github.com/a7med7ossam/shoes-agent-store.git
cd shoes-agent-store
```

## Step 4: The Magic Command
Find Docker app icon and run it then
Run the single command that reads your `docker-compose.yml` and builds everything from scratch:

```bash
docker compose up --build -d
```

### What happens next is entirely automated by Docker:

1. It downloads Python 3.12.
2. It reads `requirements.txt` and installs FastAPI, Streamlit, LangGraph, etc.
3. It downloads PostgreSQL 16 and Qdrant.
4. It boots up the database.
5. It runs `database.py`, reads your `shoes_inventory.csv`, and injects all 370 shoes into the fresh database.
6. It starts FastAPI and Streamlit.

Once your terminal says the containers are "Started", you just open your browser to http://localhost:8501 on the new laptop, and your SoleAgent is ready to take orders!
