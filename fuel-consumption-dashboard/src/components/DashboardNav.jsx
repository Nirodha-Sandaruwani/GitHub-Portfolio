// src/components/DashboardNav.jsx
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { setCurrentUser, logout as usersLogout } from '../store/slices/usersSlice'

export default function DashboardNav({ username }) {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  const handleLogout = () => {
    // Clear persisted auth and redux user
    localStorage.removeItem('auth')
    // If you have another persisted store item, you may want to clear that too:
    // localStorage.removeItem('fuel_app_state')
    dispatch(usersLogout())
    dispatch(setCurrentUser(null))
    // navigate to login (HashRouter handles path)
    navigate('/login')
    // Force a reload to reset any in-memory caches if you prefer:
    // window.location.href = window.location.origin + window.location.pathname + '#/login'
  }

  return (
    <nav style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      padding: '1rem', backgroundColor: '#2563eb', color: '#fff'
    }}>
      <div style={{ fontWeight: 700, fontSize: '1.15rem' }}>FuelTrack</div>
      <div style={{ fontSize: '0.95rem' }}>Welcome {username}</div>
      <div>
        <button onClick={handleLogout} style={{
          background: '#ef4444', color: '#fff', border: 'none', padding: '0.45rem 0.85rem',
          borderRadius: '6px', cursor: 'pointer'
        }}>Logout</button>
      </div>
    </nav>
  )
}
