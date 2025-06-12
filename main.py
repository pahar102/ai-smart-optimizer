from fastapi import FastAPI, Request
from optimizer import compress_prompt, detect_intent, fingerprint

app = FastAPI()

@app.post("/optimize")
async def optimize_prompt(request: Request):
    data = await request.json()
    raw_prompt = data.get("prompt", "")
    optimized = compress_prompt(raw_prompt)
    intent = detect_intent(raw_prompt)
    fingerprint_id = fingerprint(raw_prompt)

    return {
        "original": raw_prompt,
        "optimized_prompt": optimized,
        "intent": intent,
        "fingerprint": fingerprint_id
    }
  
