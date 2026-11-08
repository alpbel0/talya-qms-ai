import { NavLink, Outlet } from 'react-router-dom'
import { ROUTES } from '../routes'

export default function Layout() {
  return (
    <div className="layout">
      <nav className="sidebar" aria-label="Ana menü">
        <div className="brand">Talya QMS-AI</div>
        <ul>
          {ROUTES.map((r) => (
            <li key={r.path}>
              <NavLink to={r.path} end className={({ isActive }) => (isActive ? 'active' : '')}>
                {r.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
