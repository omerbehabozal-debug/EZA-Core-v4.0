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

    // 1) Input EZA analizi
    const input_analysis = await callEzaAnalyze(message, mode);

    // 2) LLM cevabı
    let llm_output = "";
    if (provider === "openai") {
      llm_output = await callOpenAiLLM(message);
    } else {
      llm_output = `[${provider}] henüz entegre edilmedi. Örnek cevap: Bu bir placeholder LLM cevabıdır.`;
    }

    // 3) Deep Mode ise output için de EZA analizi
    let output_analysis: any = null;
    if (mode === "deep") {
      output_analysis = await callEzaAnalyze(
        `USER:\n${message}\n\nMODEL:\n${llm_output}`,
        mode
      );
    }

    return NextResponse.json({
      ok: true,
      data: {
        mode,
        provider,
        llm_output,
        input_analysis,
        output_analysis
      }
    });
  } catch (err: any) {
    return NextResponse.json({
      ok: false,
      error: err?.message ?? "Proxy Chat hatası"
    });
  }
}

