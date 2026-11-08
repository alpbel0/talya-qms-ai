import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Departmanlar from './pages/Departmanlar'
import GrafGezgini from './pages/GrafGezgini'
import OnayKuyrugu from './pages/OnayKuyrugu'
import Panel from './pages/Panel'
import RiskNedensellik from './pages/RiskNedensellik'
import SoruCevap from './pages/SoruCevap'
import Vakalar from './pages/Vakalar'
import VeriYukle from './pages/VeriYukle'
import YeniUygunsuzluk from './pages/YeniUygunsuzluk'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Panel />} />
        <Route path="departmanlar" element={<Departmanlar />} />
        <Route path="yeni-uygunsuzluk" element={<YeniUygunsuzluk />} />
        <Route path="vakalar" element={<Vakalar />} />
        <Route path="soru-cevap" element={<SoruCevap />} />
        <Route path="graf-gezgini" element={<GrafGezgini />} />
        <Route path="onay-kuyrugu" element={<OnayKuyrugu />} />
        <Route path="veri-yukle" element={<VeriYukle />} />
        <Route path="risk-nedensellik" element={<RiskNedensellik />} />
      </Route>
    </Routes>
  )
}
