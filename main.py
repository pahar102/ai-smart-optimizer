from fastapi import FastAPI, Request
from optimizer import (
    compress_prompt,
    detect_intent,
    fingerprint,
    adapt_for_model,
    generate_report,
    log_usage
)

app = FastAPI()

@app.post("/optimize")
async def optimize_prompt(request: Request):
    data = await request.json()
    raw_prompt = data.get("prompt", "")
    model_name = data.get("model", "gpt")  # optional model name

    optimized = compress_prompt(raw_prompt)
    intent = detect_intent(raw_prompt)
    fingerprint_id = fingerprint(raw_prompt)
    adapted_prompt = adapt_for_model(optimized, model_name)
    report = generate_report(raw_prompt, optimized)

    # Save the usage for future analysis
    log_usage({
        "prompt": raw_prompt,
        "optimized": optimized,
        "intent": intent,
        "fingerprint": fingerprint_id,
        "model": model_name,
        "adapted_prompt": adapted_prompt,
        "report": report
    })

    return {
        "original": raw_prompt,
        "optimized_prompt": optimized,
        "intent": intent,
        "fingerprint": fingerprint_id,
        "adapted_prompt": adapted_prompt,
        "impact_report": report
    }
    
