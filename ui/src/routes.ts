export interface AppRoute {
  path: string
  label: string
}

// Sol menü ve yönlendirme tek kaynaktan beslenir.
export const ROUTES: AppRoute[] = [
  { path: '/', label: 'Panel' },
  { path: '/departmanlar', label: 'Departmanlar' },
  { path: '/yeni-uygunsuzluk', label: 'Yeni Uygunsuzluk' },
  { path: '/vakalar', label: 'Vakalar' },
  { path: '/soru-cevap', label: 'Soru-Cevap' },
  { path: '/graf-gezgini', label: 'Graf Gezgini' },
  { path: '/onay-kuyrugu', label: 'Onay Kuyruğu' },
  { path: '/veri-yukle', label: 'Veri Yükle' },
  { path: '/risk-nedensellik', label: 'Risk ve Nedensellik' },
]
