# StudySense

An AI study partner that turns any PDF into answers, summaries, quizzes, flashcards and a glossary, running entirely on your own machine.

## Table of Contents

- [Contributors](#contributors)
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Ollama Setup](#ollama-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Configuration](#configuration)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [License](#license)

## Contributors

| Name | GitHub |
| --- | --- |
| P Gnanesh | [P-Gnanesh](https://github.com/P-Gnanesh) |
| Mohammed Afshan | [MohdAfshan](https://github.com/MohdAfshan) |
| Ibrahim Sharif | [1brahimSharif](https://github.com/1brahimSharif) |

## Project Overview

StudySense is a Streamlit application that helps students understand PDF documents using a locally running language model. Upload a study document, ask questions about its content, and generate study material grounded in the document.

The application reads an uploaded PDF page by page, splits the text into overlapping chunks, creates embeddings for each chunk and stores them in a ChromaDB collection. When a question is asked, it retrieves the most relevant chunks and sends them as context to a local Ollama model. This retrieval-augmented generation (RAG) flow keeps answers focused on the uploaded document and lets every answer point back to the pages it came from.

The interface is built around the document itself. Each page of the PDF is drawn as a thumbnail split into its chunks, and the chunks that were retrieved for a question light up, numbered by rank. A live pipeline in the sidebar shows the steps behind each answer: embedding the question, searching the chunks, retrieving the best passages and writing the answer.

## Features

- Upload and process PDF documents, with a drop zone and a built-in sample document to try.
- Extract text page by page with PyMuPDF.
- Split document text into overlapping chunks.
- Retrieve relevant passages using sentence embeddings and ChromaDB.
- Ask questions about the document with page tags, source chips and the full source passages.
- See which pages and chunks were used for each answer on an animated document map.
- Choose from detailed, simple, short or exam-ready answer styles.
- Generate summaries with selectable summary styles and an optional page range.
- Generate multiple-choice quizzes with selectable difficulty, optional page range, scoring and per-question explanations.
- Generate flashcards with a 3D flip animation, mouse and keyboard navigation.
- Extract searchable key terms and definitions.
- Suggest questions that can be answered from the document.
- View individual PDF pages in the app and check whether a page was used in the last answer.
- Track questions asked, quizzes taken, average score and best score with a progress chart.
- Download chat history, summaries and the glossary as text files.
- Dark interface with a single teal accent, animated tabs and a layout that adapts to the screen width.

## Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Application language |
| Streamlit | Web application interface |
| Ollama | Local model serving |
| Llama 3.1 8B (`llama3.1:8b`) | Text generation |
| PyMuPDF (`fitz`) | PDF reading, text extraction and page rendering |
| Sentence Transformers | Passage and question embeddings |
| `all-MiniLM-L6-v2` | Embedding model |
| ChromaDB | In-memory vector collection and similarity search |
| pandas | Quiz progress data |

## Project Structure

```
StudySense/
├── app.py                 # Streamlit layout, tabs, session state and the Ask flow
├── rag.py                 # Ingestion, chunking, embeddings, retrieval and generation
├── styles.py              # All CSS: colours, fonts, animations, widget styling
├── components/
│   ├── __init__.py
│   └── ui.py              # HTML builders: document map, pipeline, cards, charts, flashcards
├── .streamlit/
│   └── config.toml        # Streamlit theme
├── requirements.txt
├── sample.pdf
├── README.md
└── .gitignore
```

### Important Files

- `app.py` holds the page layout, tabs, session state, PDF upload flow and the question-answering sequence.
- `rag.py` holds PDF ingestion, chunking, embeddings, ChromaDB retrieval, Ollama generation, prompt construction and study-material generation.
- `styles.py` holds all styling in one place. Colours and fonts are defined once as CSS variables at the top.
- `components/ui.py` builds the custom visual pieces: the document map, pipeline, source cards, quiz results, progress chart and flashcard component.
- `.streamlit/config.toml` sets the Streamlit theme to match the app styling.
- `requirements.txt` lists the Python dependencies.
- `sample.pdf` is a generic sample study document for demonstration and testing.

## Prerequisites

- Python 3.10 or newer.
- [Ollama](https://ollama.com) installed and available on the local machine.
- The `llama3.1:8b` model downloaded locally.
- A terminal such as Windows PowerShell for activating a virtual environment.
- A recent version of Streamlit. If you see errors mentioning `key=` or `vertical_alignment`, run `pip install -U streamlit`.

## Installation and Setup

Clone the repository and create a virtual environment:

```
git clone https://github.com/MohdAfshan/StudySense.git
cd StudySense
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source venv/bin/activate` instead.

## Ollama Setup

Install Ollama from the official website, then download the model:

```
ollama pull llama3.1:8b
```

Ollama must be running locally at its default address:

```
http://localhost:11434
```

The application uses the model name `llama3.1:8b` and does not require an API key.

## Running the Application

With the virtual environment activated and Ollama running:

```
streamlit run app.py
```

Streamlit prints a local URL in the terminal. Open it in your browser.

## Usage

1. Open StudySense in your browser.
2. Drop a text-based PDF onto the upload area, or click **Try sample.pdf**.
3. Wait while the document is read and indexed.
4. Use the tabs:
   - **Ask**: ask questions, watch the document map show which pages were used, review page tags and source passages, get suggested questions, or download the chat.
   - **Summary**: pick a summary style and optionally limit the page range.
   - **Quiz**: choose the number of questions and difficulty, optionally select a page range, then submit your answers for scoring and explanations.
   - **Flashcards**: generate cards, click a card or press Space to flip it, and use the arrow keys or buttons to move between cards.
   - **Key Terms**: extract terms, search the glossary and download it.
   - **Page Viewer**: inspect any page of the uploaded PDF.
   - **Progress**: review question and quiz statistics.
5. Use **Replace document** in the sidebar to load a different PDF.

Scanned PDFs without an extractable text layer may not produce usable chunks.

## Configuration

No environment variables, API keys or secrets are required.

The Ollama server and model are configured in `rag.py`:

```
MODEL_NAME = "llama3.1:8b"
OLLAMA_HOST = "http://localhost:11434"
```

The embedding model is also loaded by `rag.py`:

```
SentenceTransformer("all-MiniLM-L6-v2")
```

Sentence Transformers may download the embedding model on first use, so a fresh installation needs an internet connection once, in addition to the Ollama model download.

To change the look of the app, edit the variables at the top of `styles.py`. The `--accent` variable sets the highlight colour used across the whole interface. Fonts are loaded from Google Fonts and fall back to system fonts when offline.

## Known Limitations

- The pipeline steps in the sidebar are timed for visual effect. The pages that light up on the document map are the ones the retriever actually returned.
- The document map is a display only. To open a page, use the Page Viewer tab.
- The vector index is held in memory and is rebuilt each time a document is uploaded.

## Future Improvements

The following are planned possibilities, not current features:

- Add automated tests for PDF ingestion, retrieval, parsing and UI workflows.
- Add configurable Ollama host and model settings.
- Add support for additional document formats.
- Improve handling of scanned PDFs through optional OCR.
- Persist document indexes between application sessions.
- Add configurable generation and retrieval parameters.
- Add document management for multiple uploaded PDFs.
- Make pages on the document map clickable.
- Add a light theme.

## License

No license has been specified for this project yet.