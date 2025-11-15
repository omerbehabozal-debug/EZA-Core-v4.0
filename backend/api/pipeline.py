from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# --- Modüller ---
from backend.api.input_analyzer import analyze_input
from backend.api.output_analyzer import analyze_output
from backend.api.alignment_engine import compute_alignment
from backend.api.advisor import generate_advice

# Event logging (isteğe bağlı)
try:
    from data_store.event_logger import log_event
except Exception:
    log_event = None  # Event sistemi çökmesin diye fallback


# --- İstek Modeli ---
class PipelineRequest(BaseModel):
    text: str
    query: str | None = None
    model: str = "chatgpt"


# --- Router ---
router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


# ---------------------------------------------------
#   ANA PIPELINE ENDPOINT
# ---------------------------------------------------
@router.post("/run")
async def run_pipeline(request: PipelineRequest):
    """
    Tek endpoint üzerinden:
      1) Girdi analizi
      2) Çıktı üretimi (LLM)
      3) Alignment ve risk analizi
      4) Tavsiye oluşturma
    işlemlerini gerçekleştirir.
    """

    try:
        # 1) INPUT ANALYSIS -----------------------------------------
        input_info = analyze_input(request.text)

        # 2) OUTPUT ANALYSIS ----------------------------------------
        output_info = analyze_output(
            text=request.text,
            model=request.model,
            query=request.query
        )

        # 3) ALIGNMENT ENGINE ---------------------------------------
        alignment = compute_alignment(
            output_info=output_info,
            input_info=input_info
        )

        # 4) ADVISOR -------------------------------------------------
        final_advice = generate_advice(
            alignment=alignment,
            input_info=input_info,
            output_info=output_info
        )

        # 5) EVENT LOGGING (opsiyonel)
        if log_event:
            log_event(
                "pipeline_run",
                {
                    "input": request.text,
                    "output": output_info,
                    "alignment": alignment
                }
            )

        # 6) RESPONSE ------------------------------------------------
        return {
            "success": True,
            "input": input_info,
            "output": output_info,
            "alignment": alignment,
            "advice": final_advice
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
