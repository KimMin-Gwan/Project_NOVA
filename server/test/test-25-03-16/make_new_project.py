from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://127.0.0.1:4001", "http://localhost:4000"], # Allow all origins for testing purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML 파일 저장 경로
SAVE_DIRECTORY = "./"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)  # 디렉토리가 없으면 생성

@app.post("/save-html")
def save_html(request: dict):
    # 요청 본문 데이터 파싱
    html_content = request.get("body_data", "")
    
    if not html_content:
        return JSONResponse(status_code=400, content={"message": "No body_data provided"})
    
    # 파일 이름 생성 (e.g., saved_file.html)
    file_name = "saved_file.html"
    file_path = os.path.join(SAVE_DIRECTORY, file_name)
    
    # HTML 파일로 저장
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    # 0. fid 만들기 fid.html
    # 1. boto3에 저 파일을 저장함
    # 2. 경로 url을 만들기
    # 3. 만들어낸 경로 url을 포함한 새로운 Feed 데이터를 만들어
    # 4. 만들어낸 Feed 데이터를 DB에 저장함
    # 5. 임시 html파일을 지움
    # 6. 새로운 Feed 데이터를 알고리즘에 등록함
    # 7. 위 동작들이 정상적으로 동작했음을 리턴


    return {"message": "File saved successfully", "file_path": file_path}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
