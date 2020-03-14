CALL venv\Scripts\activate.bat
set FLASK_ENV=development
start flask run
timeout 2
start "CSIA" "http://localhost:5000"
