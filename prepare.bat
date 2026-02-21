python -m venv venv
.\venv\Scripts\pip.exe install -r .\requirements.txt
# check if .env file exists, if not copy modelo.env to .env
if not exist .env (
    copy modelo.env .env
)