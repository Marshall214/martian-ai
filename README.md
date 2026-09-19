# Martian AI 🚀

Martian AI is your ultimate, privacy-focused AI-powered academic companion designed for students, researchers, and professionals. It provides a suite of advanced tools to enhance productivity, reading, writing, and presentation workflows.

## 🌟 Features

*   **Proof AI (Semantic Humanizer)**: Bypasses AI detectors using a locally hosted **Llama 3.1 (8B)** engine with NF4 4-bit quantization. It rewrites text semantically to maximize burstiness and perplexity without losing domain terminology.
*   **Smart Summarizer**: Instantly generates concise summaries from PDFs, documents, or plain text.
*   **Smart Notes**: Converts audio lectures to text summaries and generates audio from notes.
*   **Slide Generator**: Transforms your notes into professional PowerPoint or PDF presentations.
*   **Secure & Private**: All data processing is done in-house. Your data is never shared.

## 🛠️ Tech Stack

*   **Frontend**: Next.js 15, React 19, Tailwind CSS, Framer Motion, Radix UI, Sonner (Toasts)
*   **Backend**: FastAPI, Python 3.11, SQLAlchemy, SQLite
*   **AI Engine**: PyTorch, Transformers, HuggingFace (`meta-llama/Meta-Llama-3.1-8B-Instruct`), BitsAndBytes
*   **Infrastructure**: Docker & Docker Compose

## 🚀 Recent Improvements

1.  **Llama 3.1 8B Integration**: Replaced the outdated regex-based "ZeroGPT destroyer" with a robust local Llama 3.1 model running via `bitsandbytes` `device_map="auto"` to fit inside constrained GPU environments.
2.  **Docker Optimization**: 
    *   Next.js frontend optimized with `output: "standalone"` for a significantly smaller image size.
    *   Non-root user execution (`martian` & `nextjs`) for strict security.
    *   Fixed database persistence bugs mapping directly to persistent volumes.
3.  **Premium UI/UX**: Overhauled the frontend with an Apple-like minimal monochrome aesthetic, glassmorphism, Framer Motion micro-animations, and a global Sonner toast notification system.
4.  **Codebase Cleanup**: Removed dozens of obsolete regex dictionaries, failing tests, and corrupted backup files.

## ⚙️ Getting Started (Docker)

> **IMPORTANT: HuggingFace Token Required**
> Since the backend runs Llama 3.1 locally, you must provide your HuggingFace API token to download the model.

1.  Go to [HuggingFace Llama 3.1](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct) and accept the license.
2.  Create an Access Token in your HuggingFace settings.
3.  Add the token to `backend/.env`:
    ```bash
    HF_TOKEN=hf_your_token_here
    ```
4.  Launch the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

Once the containers are running and the model finishes downloading, the frontend will be available at `http://localhost:3000` and the API at `http://localhost:8000`.
