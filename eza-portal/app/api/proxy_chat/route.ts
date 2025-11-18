import { NextRequest, NextResponse } from "next/server";

async function callEzaAnalyze(text: string, mode: "fast" | "deep") {
  const resp = await fetch("http://localhost:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, mode })
  });

  const data = await resp.json();
  return data;
}

async function callOpenAiLLM(message: string): Promise<string> {
  const apiKey = process.env.OPENAI_API_KEY;

  if (!apiKey) {
    return "LLM hatası: OPENAI_API_KEY tanımlı değil. .env dosyasına ekleyin.";
  }

  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content:
            "You are an assistant behind an ethical proxy (EZA). Answer clearly and concisely."
        },
        { role: "user", content: message }
      ]
    })
  });

  const data = await resp.json();
  const content =
    data?.choices?.[0]?.message?.content ??
    "LLM cevabı alınamadı (OpenAI response parsing error).";
  return content;
}

export async function POST(req: NextRequest) {
  try {
    const { message, mode = "fast", provider = "openai" } = await req.json();

    if (!message || typeof message !== "string") {
      return NextResponse.json(
        { ok: false, error: "Geçersiz mesaj." },
        { status: 400 }
      );
    }

    // 1) Input EZA analizi (basit versiyon - sadece input analizi için)
    // Full analysis için backend /proxy_chat endpoint'ini kullan
    const input_analysis_resp = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message, mode: "fast" })
    });
    const input_analysis = await input_analysis_resp.json();

    // 2) Backend /proxy_chat endpoint'ini kullan (tüm analizleri backend yapar)
    const proxy_resp = await fetch("http://localhost:8000/proxy_chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        text: message,
        mode: "proxy"  // Normal proxy mode
      })
    });

    if (!proxy_resp.ok) {
      return NextResponse.json({
        ok: false,
        error: `Backend error: ${proxy_resp.status} ${proxy_resp.statusText}`
      });
    }

    const backendData = await proxy_resp.json();

    // 3) Backend'den gelen veriyi frontend formatına dönüştür
    const transformedData = {
      ok: true,
      mode,
      provider,
      llm_output: backendData.text || backendData.analysis?.output?.output_text || "",
      input_analysis: backendData.analysis?.input || input_analysis,
      output_analysis: backendData.analysis?.output || null,
      alignment: backendData.analysis?.alignment || null,
      final_verdict: backendData.analysis?.final || null,
      eza_score: backendData.analysis?.eza_score || null,
      reasoning_shield: backendData.analysis?.reasoning_shield || null,
      // Frontend UI compatibility
      cleaned_output: backendData.text || "",
      output: backendData.text || "",
      eza_score_value: backendData.analysis?.eza_score?.eza_score || null,
      intent: backendData.intent ? {
        level: backendData.intent,
        summary: backendData.intent,
        score: backendData.intent_score || 0.0
      } : null,
      bias: backendData.bias || "low",
      safety: backendData.safety || "low",
      risk_level: backendData.risk_level || "none",
      reasons: backendData.analysis?.final?.reason ? [backendData.analysis.final.reason] : null,
      // Raw backend data
      _raw: backendData
    };

    return NextResponse.json({
      ok: true,
      data: transformedData
    });
  } catch (err: any) {
    return NextResponse.json({
      ok: false,
      error: err?.message ?? "Proxy Chat hatası"
    });
  }
}

