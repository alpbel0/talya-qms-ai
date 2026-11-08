# UI (React + TypeScript + Vite)

İskelet: sol menülü bir layout ve 9 boş sayfa (her biri yalnızca başlık ve
"Geliştirme aşamasında" metni içerir). Arayüz metinleri Türkçedir.

Sayfalar: Panel, Departmanlar, Yeni Uygunsuzluk, Vakalar, Soru-Cevap, Graf Gezgini,
Onay Kuyruğu, Veri Yükle, Risk ve Nedensellik. Hiçbirinde işlev yoktur; API'ye henüz bağlı
değildir.

## Geliştirme (Node 20.19+ veya 22.12+)

```bash
cp .env.example .env     # PowerShell: Copy-Item .env.example .env
npm ci
npm run dev              # http://localhost:5173
npm run lint
npm run build
```

API adresi `VITE_API_URL` ile belirlenir (`src/config.ts`). Docker imajında bu değer
derleme sırasında `--build-arg VITE_API_URL=...` ile gömülür.
