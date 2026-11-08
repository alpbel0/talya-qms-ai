// API adresi .env dosyasından (VITE_API_URL) okunur; yoksa yerel varsayılan kullanılır.
export const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
