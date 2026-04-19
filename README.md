# AI Text Processing Pipeline

**Learning Project**: Demonstrating AsyncIO, Pydantic, and FastAPI for AI Engineering

---

## Purpose

This project demonstrates modern Python skills required for AI Engineering:
- **AsyncIO**: Concurrent API calls for high-performance I/O
- **Pydantic**: Type-safe data validation and structured outputs
- **FastAPI**: Production-ready REST API architecture
- **Real-world application**: Batch document analysis at scale

Built without abstraction frameworks (no LangChain) to demonstrate core async Python competency.

---

## What It Does

Takes a directory of text files and:
1. Reads all files concurrently from the input directory
2. Sends content to LLM API (OpenAI/Azure) in parallel using AsyncIO
3. Analyzes each document for sentiment, category, and key points
4. Validates all responses using Pydantic models
5. Saves structured JSON results with timestamps
6. Exposes results via REST API endpoints

**Real-world use case**: Processing customer feedback, support tickets, or product reviews at scale.

---

## Project Structure

```
ai-document-processor/
├── data/
│   ├── input/              # Place your .txt files here
│   └── output/             # Processed results saved as JSON
├── models.py               # Pydantic models for validation
├── read_files.py           # FastAPI app + async processing logic
├── llm_config.py           # LLM client configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.11 or higher
- OpenAI API access (standard OpenAI or Azure OpenAI/custom gateway)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-document-processor

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API credentials (see Configuration below)
```

### Configuration

Copy `.env.example` to `.env` and choose ONE configuration option:

**Option A: Standard OpenAI** (Easiest for getting started)
```bash
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Option B: Azure OpenAI or Custom Gateway** (Enterprise/Organization setup)
```bash
MY_LLM_API_KEY=your-api-key
MY_LLM_ENDPOINT=https://your-endpoint.openai.azure.com/
MY_LLM_API_VERSION=2024-10-21
```

The application automatically detects which configuration you provide.

---

## Running the Application

### Start the FastAPI Server

```bash
uvicorn read_files:app --reload
```

The server will start at `http://localhost:8000`

### Interactive API Documentation

Visit `http://localhost:8000/docs` for auto-generated Swagger UI documentation where you can test all endpoints.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information and available endpoints |
| `/health` | GET | Health check with configuration details |
| `/getFiles` | GET | Process all files concurrently (main endpoint) |
| `/getFiles/nonconcurrent` | GET | Process files sequentially (for comparison) |
| `/results/list` | GET | List all saved result files |
| `/results/{filename}` | GET | Download specific result file |

### Example Usage

**1. Check service health:**
```bash
curl http://localhost:8000/health
```

**2. Process all files:**
```bash
curl http://localhost:8000/getFiles
```

**3. List all results:**
```bash
curl http://localhost:8000/results/list
```

---

## Adding Input Files

1. Place your text files (`.txt`) in the `data/input/` directory
2. Call the `/getFiles` endpoint
3. Results are automatically saved to `data/output/` as timestamped JSON files

Example input files included:
- Customer feedback documents
- Product reviews
- Support tickets

---

## Key Learning Outcomes

**Technical Skills Demonstrated:**

- **Async/Await Patterns**: Using `asyncio.gather()` for concurrent API calls
- **Pydantic Validation**: Type-safe models with field validation (regex patterns, ranges)
- **FastAPI Architecture**: RESTful API design with proper error handling
- **Type Hints**: Modern Python typing throughout
- **Error Handling**: Graceful handling of API failures in async contexts
- **File I/O**: Path operations and JSON serialization
- **LLM Integration**: Direct API usage without abstraction frameworks

**Architectural Patterns:**

- Separation of concerns (models, client config, API logic)
- Structured logging and output
- Environment-based configuration
- Validation of external API responses

---

## Technical Architecture

### Design Decisions

**Direct API Integration vs. Abstraction Frameworks**

This project intentionally uses direct LLM API integration rather than frameworks like LangChain to:
- Maintain fine-grained control over API calls and error handling
- Minimize dependencies and reduce complexity
- Demonstrate deep understanding of async patterns and concurrent programming
- Optimize for specific batch processing requirements
- Reduce latency by eliminating unnecessary abstraction layers

**Async-First Architecture**

The system is built around Python's AsyncIO to:
- Maximize throughput with concurrent API calls
- Efficiently handle I/O-bound operations
- Scale to hundreds of documents without threading complexity
- Maintain responsive API endpoints during processing

### Performance

The concurrent endpoint (`/getFiles`) processes multiple files simultaneously, significantly reducing total processing time compared to sequential processing.

Example: 5 files × 2 seconds each = 2 seconds concurrent vs 10 seconds sequential

---

## Testing

```bash
# Start the server
uvicorn read_files:app --reload

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/getFiles
```

Or use the interactive docs at `http://localhost:8000/docs`

---

## Requirements

Main dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `openai` - LLM API client
- `python-dotenv` - Environment variable management

See `requirements.txt` for full list.

---

## Future Enhancements

Potential improvements for production use:
- Rate limiting for API calls
- Caching layer for repeated content
- Text preprocessing/cleaning
- Batch size configuration
- Progress tracking for large datasets
- Database integration for results storage
- Authentication/authorization

---

## License

This is a learning/portfolio project. Feel free to use as reference.

---

## About

This project demonstrates production-grade AI engineering capabilities: async Python patterns, type-safe data validation, and scalable API architecture. Built for high-performance batch document processing with modern LLM APIs.

**Technical Stack**: Python 3.11+, FastAPI, AsyncIO, Pydantic, OpenAI API

---

## Contributing

This is a portfolio/demonstration project. Feel free to fork and adapt for your use cases.

