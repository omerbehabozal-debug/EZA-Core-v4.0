# EZA PORTAL v1.0

Bu proje, EZA-Core backend'ine bağlanan etik analizli chat portalıdır.

## Çalıştırma

1) Backend (FastAPI):
   ```bash
   uvicorn backend.main:app --reload
   ```

2) Portal:
   ```bash
   npm install
   npm run dev
   ```

Portal `http://localhost:3000/chat` adresinde çalışacaktır.

## Özellikler

- ChatGPT benzeri arayüz
- Sağda gerçek zamanlı etik panel
- EZA-Core Level 1–10 bağlantısı
- Zustand ile state yönetimi
- TailwindCSS ile modern UI

## Proje Yapısı

```
eza-portal/
 ├── app/
 │   ├── api/analyze/route.ts    # Backend API proxy
 │   ├── chat/page.tsx            # Ana chat sayfası
 │   ├── layout.tsx               # Root layout
 │   └── globals.css              # Global stiller
 ├── components/
 │   ├── ChatInput.tsx            # Mesaj girişi
 │   ├── ChatMessage.tsx          # Mesaj gösterimi
 │   ├── AnalysisPanel.tsx        # Etik analiz paneli
 │   └── ScoreBar.tsx             # Skor göstergesi
 ├── stores/
 │   └── chatStore.ts             # Zustand store
 └── lib/
     └── types.ts                 # TypeScript tipleri
```

## Notlar

- Backend'in `http://localhost:8000` adresinde çalıştığından emin olun
- Proxy Mode Aşama 3'te eklenecek

