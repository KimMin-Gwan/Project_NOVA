from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/home/{number}/{name}")
def home_number(number:int, name:str):
    print(number)
    return name

uvicorn.run(app=app, host="127.0.0.1", port=5000)

