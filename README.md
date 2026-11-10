# StudySense

StudySense is a Streamlit application that helps students understand PDF documents with a locally running language model. Upload a study document, ask questions about its content, and generate study materials grounded in the document.

## Project Overview

StudySense extracts text from an uploaded PDF, divides it into passages, creates embeddings for those passages, and stores them in a ChromaDB collection. When a user requests an answer, the application retrieves relevant passages and sends them as context to the local Ollama model. This retrieval-augmented generation (RAG) flow helps responses stay focused on the uploaded document and provides page references where applicable.

The application also uses the document to generate summaries, quizzes, flashcards, suggested questions, and a glossary of key terms.

## Features

- Upload and process PDF documents.
- Extract text page by page with PyMuPDF.
- Split document text into overlapping chunks.
- Retrieve relevant passages using sentence embeddings and ChromaDB.
- Ask questions about the uploaded document with page references and source passages.
- Choose from detailed, simple, short, or exam-ready answer styles.
- Generate summaries with selectable summary styles and optional page ranges.
- Generate multiple-choice quizzes with selectable difficulty and scoring.
- Generate flashcards with front/back navigation.
- Extract searchable key terms and definitions.
- Suggest questions that can be answered from the document.
- View individual PDF pages in the application.
- Track questions asked, quizzes taken, average score, and best score.
- Download chat history, summaries, and the glossary as text files.

## Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Application programming language |
| Streamlit | Web application interface |
| Ollama | Local model serving |
| Llama 3.1 8B (`llama3.1:8b`) | Text generation |
| PyMuPDF (`fitz`) | PDF reading, text extraction, and page rendering |
| Sentence Transformers | Passage and question embeddings |
| `all-MiniLM-L6-v2` | Embedding model used by the application |
| ChromaDB | In-memory vector collection and similarity search |
| pandas | Quiz progress data and chart preparation |

## Project Structure

```text
StudySense/
├── app.py
├── rag.py
├── requirements.txt
├── sample.pdf
├── README.md
└── .gitignore
```

### Important Files

- `app.py` contains the Streamlit layout, tabs, session state, PDF upload flow, controls, and display logic.
- `rag.py` contains PDF ingestion, chunking, embeddings, ChromaDB retrieval, Ollama generation, prompt construction, and study-material generation.
- `requirements.txt` lists the Python dependencies required by the application.
- `sample.pdf` is a generic sample study document for demonstration and testing.

The local `venv/` directory and Python cache files are development artifacts and are excluded by `.gitignore`.

## Prerequisites

- Python 3.10 or newer.
- Ollama installed and available on the local machine.
- The `llama3.1:8b` Ollama model downloaded locally.
- Windows PowerShell or another terminal suitable for activating a Python virtual environment.

## Installation and Setup

Clone the repository and create a virtual environment:

```powershell
git clone <repository-url>
cd StudySense
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Ollama Setup

Install Ollama using the instructions for your operating system from the official Ollama website, then download the model:

```powershell
ollama pull llama3.1:8b
```

Ollama must be running locally at its default address:

```text
http://localhost:11434
```

The application uses the model name `llama3.1:8b` and does not require an API key.

## Running the Application

With the virtual environment activated and Ollama running:

```powershell
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open that URL in a browser.

## Usage Instructions

1. Open StudySense in your browser.
2. Upload a text-based PDF from the sidebar.
3. Wait for the document to be read and indexed.
4. Use the available tabs:
   - **Ask**: Ask questions, view page references and source passages, review suggestions, or download the chat.
   - **Summary**: Select a summary style and optionally limit the page range.
   - **Quiz**: Choose the number of questions and difficulty, optionally select a page range, and submit answers for scoring.
   - **Flashcards**: Generate cards, move between them, and flip each card to view its answer.
   - **Key Terms**: Extract terms, search the glossary, and download it.
   - **Page Viewer**: Inspect a page from the uploaded PDF.
   - **Progress**: Review question and quiz statistics.

Scanned PDFs without an extractable text layer may not produce usable chunks.

## Configuration

No environment variables, API keys, or secrets are required by the current implementation.

The Ollama server and model are configured in `rag.py`:

```python
MODEL_NAME = "llama3.1:8b"
OLLAMA_HOST = "http://localhost:11434"
```

The embedding model is also loaded by `rag.py`:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

The embedding model may be downloaded by Sentence Transformers on first use, depending on the local environment. The application therefore requires more than just the Ollama model for a fresh installation.

## Future Improvements

The following are planned possibilities, not currently implemented features:

- Add automated tests for PDF ingestion, retrieval, parsing, and UI workflows.
- Add configurable Ollama host and model settings.
- Add support for additional document formats.
- Improve handling of scanned PDFs through optional OCR.
- Persist document indexes between application sessions.
- Add configurable generation and retrieval parameters.
- Add document management for multiple uploaded PDFs.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Create a focused branch for the change.
2. Keep changes limited to the intended feature or fix.
3. Update documentation when behavior or setup changes.
4. Verify the application starts and the relevant functionality works locally.
5. Do not commit virtual environments, uploaded documents containing private information, secrets, or generated files.

## License

No license has been specified for this project yet.
