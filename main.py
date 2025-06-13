from fastapi import FastAPI, Request
from optimizer import compress_prompt, detect_intent, fingerprint

app = FastAPI()

@app.post("/optimize")
async def optimize_prompt(request: Request):
    try:
        data = await request.json()
        raw_prompt = data.get("prompt", "")
        print("📥 Raw Prompt Received:", raw_prompt)

        optimized = compress_prompt(raw_prompt)
        intent = detect_intent(raw_prompt)
        fingerprint_id = fingerprint(raw_prompt)

        print("✅ Optimization Done")

        return {
            "original": raw_prompt,
            "optimized_prompt": optimized,
            "intent": intent,
            "fingerprint": fingerprint_id
        }
    except Exception as e:
        print("❌ Error occurred:", str(e))
        return {"error": "Internal Server Error", "detail": str(e)}
        
