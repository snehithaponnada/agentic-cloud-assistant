# Agentic Cloud Operations Assistant

An AI-powered cloud operations assistant that inspects AWS resources, analyzes application logs, identifies cloud issues, and retrieves relevant troubleshooting knowledge to recommend solutions.

The project combines **Agentic AI, AWS, RAG, and cloud troubleshooting** into an end-to-end application.

---

## Features

- Inspect AWS S3 resources
- Discover S3 buckets and objects
- Read application logs directly from S3
- Detect and analyze cloud errors
- Diagnose IAM permission issues
- Retrieve relevant troubleshooting knowledge using RAG
- Generate recommended fixes using an LLM
- Agentic tool selection using LangGraph
- REST API built with FastAPI
- Interactive React frontend

---

## System Workflow

```text
User
  |
  v
React Frontend
  |
  v
FastAPI API
  |
  v
LangGraph Agent
  |
  +--------------------+
  |                    |
  v                    v
AWS Inspection       Log Analysis
  |                    |
  v                    v
Amazon S3          Error Detection
  |                    |
  +---------+----------+
            |
            v
     Knowledge Retrieval
            |
            v
   ChromaDB Vector Store
            |
            v
   HuggingFace Embeddings
            |
            v
        Gemini LLM
            |
            v
Troubleshooting Recommendation
            |
            v
      React Frontend
```

---

## Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- LangGraph
- Boto3

### AI / RAG
- Google Gemini
- HuggingFace Sentence Transformers
- ChromaDB
- `all-MiniLM-L6-v2` embeddings

### Cloud
- Amazon Web Services (AWS)
- Amazon S3
- AWS IAM
- AWS CLI

### Frontend
- React
- Vite
- JavaScript
- CSS

---

## Project Structure

```text
agentic-cloud-assistant/
|
|-- app/
|   |-- agent/
|   |   `-- graph.py
|   |
|   |-- api/
|   |   `-- routes.py
|   |
|   |-- rag/
|   |   |-- ingest.py
|   |   `-- retriever.py
|   |
|   |-- services/
|   |
|   |-- tools/
|   |   |-- aws_tool.py
|   |   |-- s3_tools.py
|   |   |-- log_analyzer.py
|   |   `-- knowledge_tool.py
|   |
|   `-- main.py
|
|-- knowledge/
|   |-- s3_troubleshooting.txt
|   |-- iam_troubleshooting.txt
|   |-- lambda_troubleshooting.txt
|   `-- cloudwatch_troubleshooting.txt
|
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   |-- App.css
|   |   |-- index.css
|   |   `-- main.jsx
|   |
|   |-- package.json
|   `-- vite.config.js
|
|-- chroma_db/
|-- requirements.txt
|-- .env
|-- .gitignore
`-- README.md
```

---

## Agent Components

The LangGraph agent decides which tools are required based on the user's request.

### AWS Inspection

Uses Boto3 to communicate with AWS and inspect S3 resources.

The agent can:

- List S3 buckets
- List objects inside a bucket
- Read S3 objects

### Log Analysis

Application logs retrieved from S3 are analyzed to identify cloud-related errors such as:

```text
AccessDenied
User is not authorized to perform s3:GetObject
```

### Knowledge Retrieval

Troubleshooting documents are converted into embeddings and stored in ChromaDB.

When an error is detected, the agent performs semantic retrieval to find relevant AWS troubleshooting information.

### LLM Reasoning

Google Gemini uses information collected by the agent and retrieved knowledge to generate:

- Error analysis
- Likely root cause
- Relevant AWS/IAM explanation
- Recommended troubleshooting steps

---

## Example Agent Workflow

Example request:

```text
Inspect my AWS S3 environment.

Find my application log and analyze any errors you find.

Search the troubleshooting knowledge base and recommend a solution.
```

The agent autonomously performs:

```text
1. Inspect S3 buckets
        |
2. Find objects in the bucket
        |
3. Locate application.log
        |
4. Read the log from S3
        |
5. Analyze the log
        |
6. Detect AccessDenied / IAM issue
        |
7. Search troubleshooting knowledge using RAG
        |
8. Determine likely root cause
        |
9. Generate recommended solution
```

---

# Running the Project Locally

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd agentic-cloud-assistant
```

---

## 2. Create a Python Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_google_api_key
```

Do not commit API keys, AWS credentials, or other secrets to GitHub.

---

## 5. Configure AWS Authentication

Install and configure the AWS CLI before running AWS inspection locally.

Verify the CLI:

```bash
aws --version
```

Authenticate using your configured AWS authentication method and verify the active identity:

```bash
aws sts get-caller-identity
```

The AWS identity used by the application must have the permissions required for the resources being inspected.

---

## 6. Build the RAG Knowledge Base

Run the ingestion script if the ChromaDB knowledge base has not been created yet:

```bash
python -m app.rag.ingest
```

---

## 7. Start the FastAPI Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

## 8. Start the React Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

## API

### Chat Endpoint

```text
POST /api/chat
```

Example request:

```json
{
  "message": "Inspect my AWS S3 environment and analyze my application logs."
}
```

The request is passed to the LangGraph agent, which determines which cloud inspection and troubleshooting tools should be executed.

---

## Example Troubleshooting Scenario

An application log stored in Amazon S3 contains:

```text
ERROR AccessDenied while calling GetObject
ERROR User is not authorized to perform s3:GetObject
```

The assistant:

1. Discovers the S3 bucket.
2. Finds the application log.
3. Reads the log from AWS.
4. Detects the `AccessDenied` error.
5. Identifies it as an IAM permission issue.
6. Searches the RAG troubleshooting knowledge base.
7. Recommends checking `s3:GetObject`, IAM policies, resource ARNs, and S3 bucket policies.

---

## Security

Sensitive credentials should never be committed to source control.

The following should remain excluded using `.gitignore`:

```text
.env
venv/
frontend/node_modules/
__pycache__/
*.pyc
```

AWS permissions should follow the principle of least privilege.

---

## Future Improvements

- Support additional AWS services such as Lambda and CloudWatch
- IAM policy inspection
- Multi-cloud troubleshooting
- Conversation history
- Streaming agent responses
- Additional troubleshooting knowledge sources

---

## Project Status

The current implementation supports an end-to-end agentic troubleshooting workflow:

**AWS Inspection → Log Retrieval → Error Analysis → RAG Retrieval → LLM Reasoning → Recommended Solution**
