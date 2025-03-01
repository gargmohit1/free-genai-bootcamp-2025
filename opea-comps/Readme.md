## How to run the LLM Service

We are using Ollma which will be deilvered by docker-compose.

We have set docker compose port as 8008, which will provide service for ollma server

Value are mentioned in .env variables

```sh
docker compose up -d
```

When you start the Ollama it doesn't have the model downloade.
So we'll need to download the model via the API for ollama.

### Download (Pull) a model

```sh
curl http://localhost:8008/api/pull -d '{
  "model": "llama3.2:1b"
}'
```

## How to Run the mega service Example

```sh
python app.py
```
### Request
```sh
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"prompt": "Hello, how are you?"}'
```
### Response
```json
{
  "response": {
    "content": "I'm doing well, thanks for asking. Is there anything I can help you with or would you like to talk about what's on your mind?",
    "role": "assistant"
  }
}

```