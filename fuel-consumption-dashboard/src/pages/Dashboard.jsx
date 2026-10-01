// src/pages/Dashboard.jsx
import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { setCurrentUser } from '../store/slices/usersSlice'
import DashboardNav from '../components/DashboardNav'
import RefuelForm from '../components/RefuelForm'
import RefuelList from '../components/RefuelList'
import ConsumptionChart from '../components/ConsumptionChart'
import PieChartComponent from '../components/PieChartComponent'
import MiniLineChart from '../components/MiniLineChart'

export default function Dashboard() {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const currentUserId = useSelector(s => s.users?.currentUserId)
  // If Redux users are persisted you don't need the below, but we add a robust fallback:
  useEffect(() => {
    try {
      const auth = JSON.parse(localStorage.getItem('auth') || '{}')
      if (auth?.id && !currentUserId) {
        // restore current user into Redux after full page reload
        dispatch(setCurrentUser(auth.id))
      } else if (!auth?.id && !auth?.email) {
        // nothing in localStorage: force login
        navigate('/login')
      }
    } catch (err) {
      console.warn('Failed to read auth from localStorage', err)
      navigate('/login')
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const auth = (() => { try { return JSON.parse(localStorage.getItem('auth') || '{}') } catch { return {} } })()

  // If still not authenticated, do not render and redirect
  if (!auth?.id && !auth?.email && !currentUserId) {
    navigate('/login')
    return null
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <DashboardNav username={auth?.username || auth?.email || 'User'} />

      <main style={{ display: 'flex', flex: 1, padding: '1rem', gap: '1rem', overflow: 'hidden', background: '#f3f4f6' }}>
        {/* Left column */}
        <div style={{ flex: '1', display: 'flex', flexDirection: 'column', gap: '1rem', minWidth: '220px', maxWidth: '320px' }}>
          <div style={{ flex: 1, background: '#fff', borderRadius: '8px', padding: '0.5rem', boxShadow: '0 2px 6px rgba(0,0,0,0.08)' }}>
            <PieChartComponent />
          </div>
          <div style={{ flex: 1, background: '#fff', borderRadius: '8px', padding: '0.5rem', boxShadow: '0 2px 6px rgba(0,0,0,0.08)' }}>
            <MiniLineChart />
          </div>
        </div>

        {/* Center column */}
        <div style={{ flex: '2.5', display: 'flex', flexDirection: 'column', gap: '1rem', minWidth: '420px', overflowY: 'auto' }}>
          <div style={{ background: '#fff', borderRadius: '8px', padding: '1rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
            <RefuelForm />
          </div>

          <div style={{ background: '#fff', borderRadius: '8px', padding: '1rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}>
            <ConsumptionChart />
          </div>
        </div>

        {/* Right column */}
        <div style={{ flex: '1', minWidth: '260px', maxHeight: '100%', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <RefuelList />
        </div>
      </main>
    </div>
  )
}
