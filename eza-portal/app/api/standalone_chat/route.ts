import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { message, mode = "standalone" } = await req.json();

    if (!message || typeof message !== "string") {
      return NextResponse.json(
        { ok: false, error: "Geçersiz mesaj." },
        { status: 400 }
      );
    }

    // Call backend /standalone_chat endpoint
    const backendResp = await fetch("http://localhost:8000/standalone_chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message, mode })
    });

    if (!backendResp.ok) {
      return NextResponse.json({
        ok: false,
        error: `Backend error: ${backendResp.status} ${backendResp.statusText}`
      });
    }

    const backendData = await backendResp.json();

    // Transform backend response to frontend format
    const transformedData = {
      ok: true,
      mode: backendData.mode || "standalone",
      text: backendData.text || "",
      analysis: backendData.analysis || {},
      risk_level: backendData.risk_level || "low",
      intent: backendData.intent || "information",
      intent_score: backendData.intent_score || 0.0,
      bias: backendData.bias || "low",
      safety: backendData.safety || "low",
      eza_score: backendData.analysis?.eza_score?.eza_score || null,
      _raw: backendData
    };

    return NextResponse.json({
      ok: true,
      ...transformedData
    });
  } catch (err: any) {
    return NextResponse.json({
      ok: false,
      error: err?.message ?? "Standalone Chat hatası"
    });
  }
}

