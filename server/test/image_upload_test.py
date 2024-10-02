from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import uvicorn

app = FastAPI()

# CORS 설정 (필요시 수정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 원하는 도메인으로 변경
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_image_with_json(
    image: UploadFile = File(...), 
    jsonData: str = Form(...)
):
    try:
        # 이미지 처리
        image_name = image.filename
        contents = await image.read()

        # JSON 데이터 파싱
        data = json.loads(jsonData)
        title = data.get("title")
        description = data.get("description")

        print(title)
        print(description)

        # 이미지 저장 (예시)
        with open(f"uploaded_{image_name}", "wb") as f:
            f.write(contents)



        return JSONResponse(content={"message": f"Image '{image_name}' with title '{title}' uploaded successfully"})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to upload. Error: {str(e)}"}, status_code=500)


uvicorn.run(app=app, port=4000)