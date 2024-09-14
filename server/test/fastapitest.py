from fastapi import FastAPI, Response, Request, Depends
import uvicorn
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://127.0.0.1:4001"], # Allow all origins for testing purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_jwt_from_cookie(request: Request):
    jwt_token = request.cookies.get("session_id")
    return jwt_token

@app.get("/home/{number}")
def home_number(number: int):
    data = {"message": "This is a manually set JSON response"}
    response = Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=200,
        
    )
    response.set_cookie(
        key="session_id", 
        value="123456", 
        max_age=60*60*24,
        samesite="Lax",  # Changed to 'Lax' for local testing
        secure=False,  # Local testing; set to True in production
        #httponly=True
    )
    return response

@app.get("/hello")
def home_target(request: Request):
    print(request.cookies)
    data = {"message": "This is a manually set JSON response"}
    response = Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=200
    )
    response.set_cookie(
        key="session_id", 
        value="123456", 
        max_age=60*60*24,
        samesite="Lax",  # Changed to 'Lax' for local testing
        secure=False,  # Local testing; set to True in production
        httponly=True
    )
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

