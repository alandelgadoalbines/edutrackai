# EduTrackAI Backend

Base Flask application configured for cPanel Passenger deployments.

## Running locally
1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Optionally define environment variables in a `.env` file at the project root.
3. Start the app:
   ```bash
   python - <<'PY'
   from app import create_app
   app = create_app()
   app.run(debug=True)
   PY
   ```

The health endpoint will be available at `/api/health` (e.g., `http://localhost:5000/api/health`).
