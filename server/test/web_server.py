from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

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

        <div id="response"></div>

        <script>
            async function testNumberEndpoint() {
                const number = document.getElementById('numberInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:5000/home/${number}`, {
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

            async function testTargetEndpoint() {
                const target = document.getElementById('targetInput').value;
                try {
                    const response = await fetch(`http://127.0.0.1:5000/hello`, {
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
        </script>
    </body>
    </html>
    """
    return html

uvicorn.run(app=app, host="127.0.0.1", port =4001)


