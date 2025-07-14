# main.py

from fastapi import Body, Depends, FastAPI, Request
from dependencies import get_urls_content
from schemas import TextModelResponse, TextModelRequest
from models import generate_text, load_text_model

models = {}

app = FastAPI()

@app.get("/")
def root_controller():
    return {"status": "healthy"}

@app.post("/generate/text", response_model_exclude_defaults=True) 
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content) 
) -> TextModelResponse:
    ... # rest of controller logic
    prompt = f"{body.prompt}\n\nExtracted content:\n{urls_content}" if urls_content else body.prompt
    pipe = load_text_model()
    output = generate_text(pipe, prompt, temperature=body.temperature)
    return TextModelResponse(
        content=output,
        ip=request.client.host,
        tokens=len(output.split())
    )