import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { message } = await req.json();

    const resp = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message })
    });

    const data = await resp.json();
    return NextResponse.json({ ok: true, data });

  } catch (err: any) {
    return NextResponse.json({
      ok: false,
      error: err.message
    });
  }
}

