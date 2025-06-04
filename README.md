# Memexor

> Bring any data stream into your LLM's memory.

**Memexor** is an open-source ingestion and retrieval layer that makes it easy to feed **text, audio, video, or binary streams** into a **vector store**, and expose that content to your agent via the [Model Context Protocol (MCP)](https://smith.langchain.com/hub/openai/mcp-docs).

## Project Structure

The project follows a clean architecture pattern with distinct layers:

```
memexor/
├── src/
│   ├── domain/           # Core business logic & entities
│   ├── application/      # Use-cases & interfaces
│   ├── infrastructure/   # Concrete implementations
│   ├── presentation/     # API endpoints
│   ├── config/          # Settings & constants
│   └── tests/           # Unit/integration tests
├── pyproject.toml       # Project metadata & dependencies
├── .pre-commit-config.yaml  # Code quality hooks
└── README.md
```

## Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Set up pre-commit hooks:
```bash
pre-commit install
```

4. Create a `.env` file:
```bash
OPENAI_API_KEY=your-api-key
WEAVIATE_URL=http://localhost:8080
```

5. Start Weaviate:
```bash
docker-compose up -d weaviate
```

## Development Guidelines

1. **Code Style**
   - Follow PEP 8
   - Use Black for formatting
   - Sort imports with isort
   - Type-hint all functions
   - Document public APIs

2. **Testing**
   - Write tests for all new features
   - Maintain test coverage
   - Run `pytest` before committing

3. **Git Workflow**
   - Create feature branches
   - Write descriptive commit messages
   - Submit PRs for review

## API Usage

### Upload Text
```bash
curl -F 'file=@sample.txt' localhost:8000/upload/text
```

### Search Documents
```bash
curl -X POST localhost:8000/tools/search \
  -H "Content-Type: application/json" \
  -d '{"text": "query text", "top_k": 5}'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

## ⚡️ Why Memexor?

LLMs are powerful—but forgetful.

Memexor helps you:

- 🎙 Ingest **any stream**: audio, video, PDFs, binary logs, even EEG
- 🧠 Convert into embeddings and store in your **vector DB of choice**
- 🔁 Expose a `/tools/search` endpoint via MCP for agent queries
- 🧭 Build contextual, memory-enabled AI systems in minutes

---

## 🔧 Quickstart (dev preview)

```bash
git clone https://github.com/yourname/memexor.git
cd memexor
cp .env.example .env
docker-compose up --build
```
Then:
```bash
curl -F 'file=@sample.txt' localhost:8000/upload/text
```
##🧱 Architecture
```text
[ text/audio/video stream ]
          ↓
   [ Ingestion API (FastAPI) ]
          ↓
[ Embedding layer (OpenAI or local) ]
          ↓
[ Vector DB (Weaviate, Pinecone, etc.) ]
          ↓
[ MCP-compatible /tools/search endpoint ]
```

---

## 🗺 Roadmap

- [x] Text ingestion + OpenAI embedding
- [ ] Audio and video file ingestion
- [ ] Plug-ins for CLIP, Whisper, ImageBind
- [ ] Live stream support (RTSP/WebSocket)
- [ ] MCP server with hybrid search
- [ ] Hosted control plane (auth, RBAC, metrics)

---

## 🌍 Use Cases

- 🧠 Give your agent a memory of everything it's seen/heard
- 🔍 Index and search your meeting recordings, notes, files
- 🧪 Experiment with new modalities (EEG, IMU, sensors)
- 💼 Build powerful internal tools with long-term knowledge

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) for the ingestion server
- [Weaviate](https://weaviate.io/) for vector storage
- [OpenAI](https://platform.openai.com/docs) or BYO embedding model
- [Docker Compose](https://docs.docker.com/compose/) for local orchestration

---

## 🤝 Contributing

Want to help build the open memory layer for multimodal AI agents?  
Open issues, file PRs, or join the conversation in [GitHub Discussions](https://github.com/yourname/memexor/discussions).

---

## 🧾 License

MIT (for now). We may introduce a dual-license or BSL model as Memexor evolves. All feedback welcome.

---

## 👋 Stay in touch

Follow [@yourhandle](https://twitter.com/yourhandle) or star the repo to stay in the loop.  
We're in early validation—your feedback can shape Memexor's future.
