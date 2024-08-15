from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_item(name: str, price: int):
    return {"name": name, "price": price}
