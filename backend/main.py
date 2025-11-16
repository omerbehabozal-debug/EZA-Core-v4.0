# -*- coding: utf-8 -*-
"""
EZA-Core v4.0
Ana FastAPI Uygulaması
"""

from typing import Optional, Dict, Any, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from backend.api.input_analyzer import analyze_input
from backend.api.output_analyzer import analyze_output, evaluate_output
from backend.api.alignment_engine import compute_alignment
from backend.api.advisor import generate_advice
from backend.api.utils.model_runner import (
    call_single_model,
    call_multi_models,
    rewrite_with_ethics,
)

from backend.api.pipeline import router as pipeline_router


from data_store.event_logger import log_event

from backend.api.utils.exceptions import EZAException, RateLimitExceeded


from backend.middleware.request_logger import RequestLoggerMiddleware
from backend.middleware.normalize_middleware import NormalizeMiddleware
from backend.middleware.rate_limit_middleware import RateLimitMiddleware
from backend.middleware.circuit_breaker import CircuitBreakerMiddleware
from backend.middleware.error_handler import (
    eza_exception_handler,
    rate_limit_handler,
    generic_exception_handler
)




app = FastAPI(title="EZA-Core v4.0")

# --- Middleware Katmanı ---
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(NormalizeMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(CircuitBreakerMiddleware)

# --- Exception Handler Katmanı ---
app.add_exception_handler(EZAException, eza_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(Exception, generic_exception_handler)



templates = Jinja2Templates(directory="frontend/templates")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# --- API Route Katmanı ---
app.include_router(pipeline_router)



# -------------------------------------------------
# Pydantic Modelleri
# -------------------------------------------------

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    query: Optional[str] = None
    model: Optional[str] = "chatgpt"


class PairRequest(BaseModel):
    input_text: str
    output_text: str


# -------------------------------------------------
# Sağlık kontrolü
# -------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/health/deep", tags=["system"])
async def deep_health_check():
    try:
        from backend.api.input_analyzer import analyze_input
        from backend.api.output_analyzer import analyze_output
        from backend.api.alignment_engine import compute_alignment
        from backend.api.advisor import generate_advice

        test_in = "Test input"
        test_out = "Test output"

        input_scores = analyze_input(test_in)
        output_scores = analyze_output(test_out)
        alignment = compute_alignment(input_scores, output_scores)
        advice = generate_advice(input_scores, output_scores, alignment)

        return {
            "status": "ok",
            "input_scores": input_scores,
            "output_scores": output_scores,
            "alignment": alignment,
            "advice": advice,
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/test/pipeline", tags=["test"])
async def test_pipeline():
    try:
        from backend.api.input_analyzer import analyze_input
        from backend.api.output_analyzer import analyze_output
        from backend.api.alignment_engine import compute_alignment
        from backend.api.advisor import generate_advice

        sample_input = "How can I protect my digital privacy?"
        sample_output = "Use strong passwords and avoid clicking unknown links."

        input_scores = analyze_input(sample_input)
        output_scores = analyze_output(sample_output)
        alignment = compute_alignment(input_scores, output_scores)
        advice = generate_advice(input_scores, output_scores, alignment)

        return {
            "input_text": sample_input,
            "output_text": sample_output,
            "input_scores": input_scores,
            "output_scores": output_scores,
            "alignment": alignment,
            "advice": advice,
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------------------------
# Ana UI (chat arayüzü)
# -------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# -------------------------------------------------
# /analyze – Tam E2E etik analiz
#  - chat.js burayı kullanır
#  - api_test.py de burayı test eder
# -------------------------------------------------

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    text = req.text or req.query or ""
    model = (req.model or "chatgpt").lower()

    # 1) Input analizi
    input_scores: Dict[str, Any] = analyze_input(text)

    # 2) Model cevabını al
    if model == "multi":
        models = ["chatgpt", "claude", "gemini", "llama"]
        model_outputs = call_multi_models(text, models)
    else:
        out = call_single_model(text, model_name=model)
        model_outputs = {model: out}

    # 3) Output analizi (çoklu model ortalaması)
    # Her model çıktısı için ayrı ayrı analiz yap
    output_analyses = {}
    for model_name, output_text in model_outputs.items():
        output_analyses[model_name] = analyze_output(output_text, model=model_name)
    
    # İlk modelin analizini ana output_scores olarak kullan (veya birleştirilmiş analiz)
    output_scores = output_analyses[list(model_outputs.keys())[0]]

    # 4) Alignment hesabı
    alignment_result = compute_alignment(
        input_analysis=input_scores,
        output_analysis=output_scores,
    )
    alignment_score = alignment_result.get("alignment_score", 0)
    alignment_label = alignment_result.get("verdict", "unknown")

    # 5) EZA tavsiyesi
    advice = generate_advice(
        input_analysis=input_scores,
        output_analysis=output_scores,
        alignment_result=alignment_result,
    )

    # 6) Etik olarak güçlendirilmiş cevap
    #   (multi durumda baz modeli chatgpt alıyoruz, yoksa ilk modeli)
    base_model_key = "chatgpt"
    if base_model_key not in model_outputs:
        base_model_key = list(model_outputs.keys())[0]
    
    # advice dict'inden string çıkar
    advice_text = ""
    if isinstance(advice, dict) and advice.get("ok"):
        advice_dict = advice.get("advice", {})
        if isinstance(advice_dict, dict):
            advice_text = advice_dict.get("user_message", "") or str(advice_dict)
        else:
            advice_text = str(advice_dict)
    else:
        advice_text = str(advice)
    
    rewritten = rewrite_with_ethics(
        text=model_outputs[base_model_key],
        advice=advice_text,
        model_name=base_model_key,
    )

    # 7) Log kaydı
    log_event(
        {
            "query": text,
            "models_used": list(model_outputs.keys()),
            "input_scores": input_scores,
            "model_outputs": model_outputs,
            "output_scores": output_scores,
            "alignment_score": alignment_score,
            "alignment_label": alignment_label,
            "alignment_result": alignment_result,
            "advice": advice,
            "rewritten_text": rewritten,
        }
    )

    # 8) Response
    #    - testler için: language, intents, risk_level top-level
    #    - frontend için: input_scores, model_outputs, output_scores...
    input_analysis = input_scores.get("analysis", {})
    return {
        "language": input_analysis.get("language"),  # analysis içinden
        "intents": input_analysis.get("intent"),  # "intent" tek, "intents" değil
        "risk_level": "high" if input_analysis.get("risk_flags") else "low",  # risk_flags'den türet
        "input_scores": input_scores,
        "model_outputs": model_outputs,
        "output_scores": output_scores,
        "alignment_score": alignment_score,
        "alignment_label": alignment_label,
        "alignment_result": alignment_result,
        "advice": advice,
        "rewritten_text": rewritten,
    }


# -------------------------------------------------
# /pair – Sadece soru + cevap uyumu testi
#  - pair_trainer_test.py burayı değil, core fonksiyonları test ediyor
#  - Ama API olarak da sunuyoruz
# -------------------------------------------------

@app.post("/pair")
async def pair(req: PairRequest):
    input_scores = analyze_input(req.input_text)
    output_scores = evaluate_output(req.output_text)

    alignment_result = compute_alignment(
        input_analysis=input_scores,
        output_analysis=output_scores,
    )

    return {
        "alignment_score": alignment_result.get("alignment_score", 0),
        "alignment_label": alignment_result.get("verdict", "unknown"),
    }


# -------------------------------------------------
# /dashboard – Şimdilik basit HTML placeholder
#  - api_test sadece HTML döndüğünü kontrol ediyor
# -------------------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # İleride burada gerçek grafikler olacak (Supabase verisiyle).
    html = """
    <html>
      <head><title>EZA Dashboard</title></head>
      <body>
        <h1>EZA-Core v4.0 – Dashboard (Placeholder)</h1>
        <p>Burada ileride alignment trendleri, risk dağılımı ve model kıyas grafikleri gösterilecek.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
