import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { 
  Building2, 
  LayoutDashboard, 
  Users, 
  ShoppingCart, 
  Package, 
  Headphones, 
  Archive, 
  CreditCard, 
  LogOut,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/usuarios', label: 'Usuários', icon: Users },
  { path: '/compras', label: 'Compras', icon: ShoppingCart },
  { path: '/ativos', label: 'Ativos', icon: Package },
  { path: '/chamados', label: 'Chamados', icon: Headphones },
  { path: '/inventario', label: 'Inventário', icon: Archive },
  { path: '/contas-mensais', label: 'Contas Mensais', icon: CreditCard },
]

export function Sidebar({ usuario, onLogout }) {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  return (
    <div className={`bg-white border-r border-gray-200 transition-all duration-300 ${collapsed ? 'w-16' : 'w-64'}`}>
      <div className="flex flex-col h-full">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            {!collapsed && (
              <div className="flex items-center space-x-2">
                <Building2 className="h-8 w-8 text-primary" />
                <div>
                  <h1 className="text-lg font-semibold">Gestão TI</h1>
                  <p className="text-xs text-gray-500">Sistema Integrado</p>
                </div>
              </div>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setCollapsed(!collapsed)}
              className="p-1"
            >
              {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
            </Button>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="h-5 w-5 flex-shrink-0" />
                    {!collapsed && <span className="font-medium">{item.label}</span>}
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        {/* User Info & Logout */}
        <div className="p-4 border-t border-gray-200">
          {!collapsed && (
            <div className="mb-3">
              <p className="text-sm font-medium text-gray-900">{usuario.nome}</p>
              <p className="text-xs text-gray-500">{usuario.email}</p>
              <p className="text-xs text-gray-500 capitalize">{usuario.perfil}</p>
            </div>
          )}
          <Button
            variant="ghost"
            onClick={onLogout}
            className={`w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 ${
              collapsed ? 'px-2' : ''
            }`}
          >
            <LogOut className="h-4 w-4" />
            {!collapsed && <span className="ml-2">Sair</span>}
          </Button>
        </div>
      </div>
    </div>
  )
}

