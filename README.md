# Memexor

> Bring any data stream into your LLM’s memory.

**Memexor** is an open-source ingestion and retrieval layer that makes it easy to feed **text, audio, video, or binary streams** into a **vector store**, and expose that content to your agent via the [Model Context Protocol (MCP)](https://smith.langchain.com/hub/openai/mcp-docs).

Inspired by Vannevar Bush’s vision of the “Memex”—a device to augment human memory—**Memexor** is built to give your LLM agents a persistent, multimodal, searchable memory layer.

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

- 🧠 Give your agent a memory of everything it’s seen/heard
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
We’re in early validation—your feedback can shape Memexor’s future.
