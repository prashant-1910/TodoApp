from fastapi import FastAPI
from database import engine
from router import auth,todo,admin,user

app = FastAPI()

#this will create todos.db when we run app 1st time , if we make any db chnages we need to delete todos.db file and rerun the app this will recreate db with updated colums changes
#if you are using sqlalchemy then only keep this file other wise no use of below
#models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)
