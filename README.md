# Flask Lab Project

A Flask-based web application with CI/CD pipelines and Docker support.

## Project Structure

- `main/` - Main Flask application
  - `app.py` - Flask application entry point
  - `requirements.txt` - Python dependencies
  - `Dockerfile` - Docker container configuration
  - `tests/` - Unit tests
  - `templates/` - HTML templates
  - `static/` - CSS and static files
- `.github/workflows/` - CI/CD workflows
  - `ci-cd.yml` - Main CI/CD pipeline for testing and building
  - `vite-pages.yml` - Frontend deployment (currently disabled)

## Recent Fixes (October 21, 2025)

### 1. Fixed Werkzeug Compatibility Issue
**Problem:** Tests were failing with `AttributeError: module 'werkzeug' has no attribute '__version__'`

**Solution:** Pinned Werkzeug to version 2.2.3 in `requirements.txt` to ensure compatibility with Flask 2.2.5

```
Flask==2.2.5
Werkzeug==2.2.3
pytest==7.4.0
```

### 2. Updated CI/CD Workflows
- CI/CD pipeline now triggers on both `main` and `frontend` branches
- All tests pass successfully ✅
- Docker build configured correctly

### 3. Disabled Frontend Workflow
- Temporarily disabled auto-trigger for `vite-pages.yml` workflow until frontend project is created
- Workflow only runs on manual dispatch (`workflow_dispatch`)

## Setup Instructions

### Local Development

1. **Install dependencies:**
   ```bash
   cd main
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at http://localhost:5000

3. **Run tests:**
   ```bash
   pytest -v
   ```

### Docker Setup

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Visit http://localhost:5000

## CI/CD Pipeline

The project uses GitHub Actions for automated testing and building:

- **Trigger:** Push or PR to `main` or `frontend` branches
- **Steps:**
  1. Checkout code
  2. Set up Python 3.11
  3. Install dependencies
  4. Run pytest tests
  5. Build Docker image

## API Endpoints

- `GET /` - Home page
- `GET /health` - Health check endpoint
- `POST /data` - JSON data endpoint

## Requirements

- Python 3.11+
- Flask 2.2.5
- Werkzeug 2.2.3
- pytest 7.4.0
- Docker & Docker Compose (optional)

## Testing

All unit tests are located in `main/tests/test_app.py` and include:
- Home page test
- Health check test
- JSON POST data test
- Non-JSON POST data validation test

**Test Results:** ✅ 4 passed

## Notes

- The `github-pages` environment error in `vite-pages.yml` requires GitHub Pages to be enabled in repository settings
- Python 3.13 compatibility: Some deprecation warnings appear but don't affect functionality
- Session data is stored in `main/data/sessions/`