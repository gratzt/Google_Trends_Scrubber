REM paths will need to be adjusted to reflect the users set up
call C:\Users\Public\Anaconda3\envs\google_trends\Lib\venv\scripts\nt\activate.bat
C:\Users\Public\Anaconda3\envs\google_trends\python.exe "%~dp0\Google_trends_scrubber.py"
REM "C:\Program Files\PostgreSQL\12\bin\psql" -U postgres -d MYDB -a -f %~dp0\update_search_data.sql
PAUSE

