# Reddit Radar
`Spot problems and insights in niche Reddit communities automatically.`

Reddit Radar is a lightweight AI agent that automates research on specific Reddit communities by finding niche pain points, validating them with an LLM, and producing structured outputs for downstream storage (Notion, database, etc.). Perfect for entrepreneurs, developers or community managers looking to discover problems worth solving in highly focused Reddit niches.

[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![Docs](https://img.shields.io/badge/docs-up--to--date-brightgreen?style=flat-square)](#)


# Key Ideas

- Automatically collect posts and comments from configured niche subreddits.
- Use an LLM (Gemini) to validate whether a discovered issue represents a meaningful market problem within the niche.
- Produce structured outputs that can be saved to Notion or a database for later review and prioritization.

# Current Features (Implemented)

- OAuth-based Reddit integration for data ingestion
- Basic Gemini AI integration (validation prompts)
- Modular code structure with agents, services and pipelines
- Sentiment analysis and text processing helpers
- Structured logging</br>
<img width="1832" height="967" alt="image" src="https://github.com/user-attachments/assets/334da5c1-31af-4c92-85b0-3930b28cc464" />


> Planned features are tracked in the roadmap and will be added over time.


# Quick start

### Prerequisites
```bash
Python 3.11+ (tested with 3.13)
A Reddit app (client ID & secret)
Gemini API key (Google LLM)
```

### 1. Clone the repository

```bash
    git clone https://github.com/[your-username]/Market-Scouting-AI-Agent.git
   ```

### 2. Create a virtual environment and install dependencies

```bash
    python -m venv .venv
    .\.venv\Scripts\activate    # Windows
    pip install -r requirements.txt
```

### 3. Copy and edit environment variables

```bash
   cp .env.example .env
```

Open `.env` and set the required keys (see Configuration below).

### 4. Run the ingest agent (example)

```bash
   python engines\ingest_engine.py
```

Depending on the agent/engine you want to run, use the corresponding script under `engines/`.


# Configuration (.env)

The following environment variables are used by the project (add any others required by your integrations):

``` bash
REDDIT_CLIENT_ID       # Reddit API client ID
REDDIT_CLIENT_SECRET   # Reddit API secret
REDDIT_USER_AGENT      # Reddit API user agent string
GEMINI_API_KEY         # Gemini / Google LLM API key
NOTION_API_KEY         # Notion integration key
NOTION_DB_ID           # Notion database id
```

Notes:
```bash
Keep secrets out of version control. Use a secrets manager for production.
```

# Project structure (Overview)

- clients/        thin API clients (Reddit, Gemini)
- engines/        runnable scripts / entrypoints (reddit_ingest, curator)
- services/       business logic and integrations (scrapers, storage)
- pipelines/      data processing pipelines (sentiment, curator)
- database/       SQLAlchemy models and DB initialization
- utils/          shared helpers

# Development status

Branch: MSAA-05-Curator-Agent-Development

- ✅ Project skeleton and core modules
- ✅ Reddit ingestion and basic data collection
- ✅ Gemini integration for evaluation
- 🔄 Ongoing: Problem processing and storage
- 📝 Planned: Notion sync, richer problem-ranking, Email notifications


# Contributing

Contributions and PRs are welcome. Suggested ways to help:
- Implement planned features from the roadmap
- Improve data processing and validation prompts
- Add tests and CI
- Improve documentation and examples

When opening a PR, include tests or a short demo showing the change.

