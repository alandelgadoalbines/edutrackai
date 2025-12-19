# Flask Backend

A minimal Flask backend configured via a `.env` file, with SQLAlchemy integration and a simple health-check endpoint.

## Prerequisites
- Python 3.9+ recommended
- `pip` for managing Python packages

## Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root to configure the app. You can start from the example below:
   ```env
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   SECRET_KEY=change-me
   DATABASE_URL=sqlite:///app.db
   ```

## Running the server
With your virtual environment active and `.env` populated:
```bash
flask run
```
By default the app will be available at `http://127.0.0.1:5000`.

## Health check
Use the health endpoint to verify the service is up:
```bash
curl http://127.0.0.1:5000/health
```
A successful response returns:
```json
{"status": "healthy"}
```
