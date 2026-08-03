# TodoApp

Python version -> Python 3.14.6
create env -> python -m venv fastapienv 
Enable Env -> fastapienv\Scripts\activate.bat
Disbale Env -> deactivate
 #Install below pip commands in env
  pip list
  pip install fastapi
  pip install "fastapi[standard]"
  pip install "uvicorn[standard]"
  pip install sqlalchemy (For db)
  pip install passlib (to encrypt the password)
  pip install bcrypt==4.0.1 (to encrypt the password)
  pip install python-multipart (to use form in fastapi like authform) 
  pip install "python-jose[cryptography]"  (JWT)
  pip install psycopg2-binary (for postgres)
  pip install pymysql (for mysql)
  python -m pip install streamlit requests (streamlit)
=====
Installing and setting up sqlit3 in Window
go to -> https://sqlite.org/download.html
look for "sqlite-tools-win-x64-3530400.zip" - Command-line tools for Windows x64, including (1) the command-line shell, (2) sqldiff.exe, (3) sqlite3_analyzer.exe, and (4) sqlite3_rsync.exe.
download the zip and extract in "C" drive and rename directory to sqlit3
add this directory location in enviourment variable System variable Path 
now check the version in cmd -> sqlite3
==================
Connect your local application db todos.db to run the queries 
go to db directory location type in cmd -> sqlite3 todos.db
it will connect to sqlite>
to check the table structure -> .schema 
sqlite> insert into todos (title,description,priority,completed) values('Book','des1',1,False);
to change table mode ui 
.mode table or .mode box or .mode column

====
Course github link -> https://github.com/codingwithroby/fastapi-the-complete-course 

Run the application -> uvicorn books:app --reload
                       fastapi run books.py (another way to run the app)
OpenAPI link -> http://127.0.0.1:8000/docs

Git Repo -> https://github.com/prashant-1910/FastAPI.git


====

====================================================
Quick options and commands:
• Simple (pip) Working solution: (pip3 freeze > requirements.txt)
 python -m pip freeze > requirements.txt  (commit this). 
 Teammates run: python -m pip install -r requirements.txt
 To uninstall: python -m pip uninstall -r requirements.txt -y
• Better (pinning): use pip-tools: pip-compile requirements.in -> requirements.txt
• Modern (Poetry): commit pyproject.toml + poetry.lock; teammates run: poetry install
• Conda: conda env export > environment.yml; conda env create -f environment.yml
==========================================================
uvicorn main:app --host 0.0.0.0 --port 10004
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=10005

===
.\todoenv\Scripts\Activate.ps1
python -m uvicorn main:app --reload

.\todoenv\Scripts\Activate.ps1
streamlit run streamlit_app.py

==
https://todoapp-cvit.onrender.com/