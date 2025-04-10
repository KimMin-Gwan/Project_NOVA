from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:6000",
        "http://127.0.0.1:4000",
        "http://localhost:6000",
        "http://127.0.0.1:4001",
        "http://127.0.0.1:3000",
        "http://localhost:3000"
        ],  # 원격 호스트의 웹소켓 연결을 허용할 도메인 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse)
def home():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Test</title>
    </head>
    <body>
        <h1>FastAPI Endpoint Test</h1>

        <div>
            <label for="numberInput">Enter a number:</label>
            <input type="number" id="numberInput" value="123">
            <button onclick="testNumberEndpoint()">Test /home/{number}</button>
        </div>

        <div>
            <label for="targetInput">Enter a target:</label>
            <input type="text" id="targetInput" value="example">
            <button onclick="testTargetEndpoint()">Test /home/{target}</button>
        </div>

        <div>
            <label for="targetInput">Enter a target:</label>
            <input type="text" id="targetInput" value="example">
            <button onclick="testThirdEndpoint()">Test /home/{target}</button>
        </div>

        <div>
            <label for="targetInput">Enter a target:</label>
            <input type="text" id="targetInput" value="example">
            <button onclick="testForthEndpoint()">Test /home/{target}</button>
        </div>

        <div>
            <label for="targetInput">Enter a target:</label>
            <input type="text" id="targetInput" value="example">
            <button onclick="testfifthEndpoint()">Test /home/{target}</button>
        </div>

        <div id="response"></div>

        <script>
            async function testNumberEndpoint() {
                const number = document.getElementById('numberInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:4000/user_home/try_login`, {
                        method: 'POST',
                        credentials: 'include', // 쉼표 추가
                        headers: {
                            'Content-Type': 'application/json' // 헤더 추가
                        },
                        body: JSON.stringify({
                            "header" : {
                                "request-type": "default",
                                "client-version": "v1.0.1",
                                "client-ip": "127.0.0.1",
                                "uid": "1234-abcd-5678",
                                "endpoint": "/user_system/",
                                },
                            "body" : {
                                "email" : "randomUser2@naver.com", 
                                "password": "sample122"
                            }
                        })
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    const data = await response.json();
                    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
                } catch (error) {
                    console.error('Fetch error:', error);
                    document.getElementById('response').innerText = 'Error occurred: ' + error.message;
                }
            }

            async function testTargetEndpoint() {
                const target = document.getElementById('targetInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:4000/user_home/try_change_nickname?index=3&custom=운영자`, {
                        mode: 'cors',
                        credentials: 'include'
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    const data = await response.json();
                    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
                } catch (error) {
                    console.error('Fetch error:', error);
                    document.getElementById('response').innerText = 'Error occurred: ' + error.message;
                }
            }

            async function testThirdEndpoint() {
                const target = document.getElementById('targetInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:4000/feed_explore/interaction_feed?fid=2&action=1`, {
                        mode: 'cors',
                        credentials: 'include'
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    const data = await response.json();
                    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
                } catch (error) {
                    console.error('Fetch error:', error);
                    document.getElementById('response').innerText = 'Error occurred: ' + error.message;
                }
            }

            async function testForthEndpoint() {
                const number = document.getElementById('numberInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:4000/user_home/try_change_password`, {
                        method: 'POST',
                        credentials: 'include', // 쉼표 추가
                        headers: {
                            'Content-Type': 'application/json' // 헤더 추가
                        },
                        body: JSON.stringify({
                            "header" : {
                                "request-type": "default",
                                "client-version": "v1.0.1",
                                "client-ip": "127.0.0.1",
                                "uid": "1234-abcd-5678",
                                "endpoint": "/user_system/",
                                },
                            "body" : {
                                "password": "sample122",
                                "new_password" : "sample123"
                            }
                        })
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    const data = await response.json();
                    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
                } catch (error) {
                    console.error('Fetch error:', error);
                    document.getElementById('response').innerText = 'Error occurred: ' + error.message;
                }
            }

            async function testfifthEndpoint() {
                const number = document.getElementById('numberInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:4000/user_home/try_send_email`, {
                        method: 'POST',
                        credentials: 'include', // 쉼표 추가
                        headers: {
                            'Content-Type': 'application/json' // 헤더 추가
                        },
                        body: JSON.stringify({
                            "header" : {
                                "request-type": "default",
                                "client-version": "v1.0.1",
                                "client-ip": "127.0.0.1",
                                "uid": "1234-abcd-5678",
                                "endpoint": "/user_system/",
                                },
                            "body" : {
                                "email": "alsrhks2508@naver.com",
                            }
                        })
                    });
                    if (!response.ok) {
                        throw new Error('Network response was not ok.');
                    }
                    const data = await response.json();
                    document.getElementById('response').innerText = JSON.stringify(data, null, 2);
                } catch (error) {
                    console.error('Fetch error:', error);
                    document.getElementById('response').innerText = 'Error occurred: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """
    return html

@app.get('/upload', response_class=HTMLResponse)
def home():
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Upload with JSON</title>
        </head>
        <body>

        <h1>Image Upload</h1>

        <!-- 이미지 업로드 폼 -->
        <form id="uploadForm">
            <input type="file" id="imageInput" accept="image/*" multiple><br><br> <!-- multiple 속성 추가 -->
            <input type="text" id="titleInput" placeholder="Title"><br><br>
            <input type="text" id="descriptionInput" placeholder="Description"><br><br>
            <button type="submit">Upload Image</button>
        </form>

        <!-- 응답 메시지 출력 -->
        <p id="message"></p>

        <script>
        document.getElementById("uploadForm").addEventListener("submit", async function(event) {
            event.preventDefault();  // 폼의 기본 동작을 막음

            const imageInput = document.getElementById("imageInput");
            const titleInput = document.getElementById("titleInput");
            const descriptionInput = document.getElementById("descriptionInput");
            const messageElement = document.getElementById("message");

            // FormData 객체에 파일과 JSON 데이터를 추가
            const formData = new FormData();

            // 여러 파일을 선택했을 때 각각의 파일을 FormData에 추가
            if (imageInput.files.length > 0) {
                for (const file of imageInput.files) {
                    formData.append("images", file); // "images" 키로 여러 파일 추가
                }
            } else {
                messageElement.textContent = "No image selected.";
                return;
            }

            // JSON 데이터 추가
            formData.append("jsonData", JSON.stringify({
                header : {
                    "request-type": "default",
                    "client-version": "v1.0.1",
                    "client-ip": "127.0.0.1",
                    "uid": "1234-abcd-5678",
                    "endpoint": "/user_system/",
                },
                body: {
                    body : titleInput.value,
                    fid: "",
                    fclass: "card",
                    choice: [],
                    hashtag : ["임시", "해시태그", "노바"]
                }
            })); 

            try {
                // 서버에 POST 요청 보내기
                const response = await fetch("http://127.0.0.1:4000/feed_explore/try_edit_feed", {
                    method: "POST",
                    credentials: 'include',
                    body: formData
                });

                const result = await response.json();

                if (response.ok) {
                    messageElement.textContent = result.message + " Images saved at: " + result.image_paths.join(", ");
                } else {
                    messageElement.textContent = "Error: " + result.detail;
                }
            } catch (error) {
                messageElement.textContent = "Upload failed: " + error.message;
            }
        });
        </script>

        </body>
        </html>

    """
    return html

uvicorn.run(app=app, host="127.0.0.1", port =4001)


