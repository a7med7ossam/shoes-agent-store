ollama pull llama3.1:8b
ollama serve

git clone <https://github.com/a7med7ossam/shoes-agent-store.git>
cd shoes-agent-store

docker compose up --build -d



# You will not need those anymore!!!
# python database.py
# uvicorn main:app --reload
# streamlit run app.py