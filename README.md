# ReviewMate

### AI-Powered GitHub Pull Request Review Platform

ReviewMate is a full-stack application that automatically analyzes GitHub pull requests using AI and provides actionable code-review feedback. It combines GitHub integration, FastAPI, PostgreSQL, Redis/RQ, Gemini AI, and React into a complete local development workflow.

---

## Overview

Code reviews can be time-consuming, especially when developers need to manually inspect every pull request for potential issues, risks, and missing tests.

ReviewMate automates the first level of review by:

- Connecting GitHub repositories
- Receiving pull request events through GitHub Webhooks
- Fetching changed files from pull requests
- Sending code changes to Gemini AI for analysis
- Generating a structured review
- Assigning a risk level
- Providing recommendations
- Identifying whether tests may be missing
- Automatically posting the review back to the GitHub pull request

The project also uses Redis and RQ for background processing so that AI analysis can run asynchronously instead of blocking the API request.
