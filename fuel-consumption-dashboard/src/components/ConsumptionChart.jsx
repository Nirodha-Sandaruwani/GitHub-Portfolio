// src/components/ConsumptionChart.jsx
import React from 'react'
import { useSelector } from 'react-redux'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function ConsumptionChart() {
  const reduxUserId = useSelector(s => s.users?.currentUserId)
  const allRefuels = useSelector(s => s.refuels || [])
  const auth = (() => { try { return JSON.parse(localStorage.getItem('auth') || '{}') } catch { return {} } })()
  const userId = reduxUserId || auth?.id || auth?.email

  if (!userId) return <div className="card">Login to view chart.</div>

  const userRefuels = (allRefuels || []).filter(r => r.userId == userId)
  const data = userRefuels.map((r, i) => {
    const prevKm = userRefuels[i - 1]?.km || 0
    const distance = r.km - prevKm
    const consumption = distance > 0 ? +((r.liters / distance) * 100).toFixed(2) : null
    return { date: r.date, consumption }
  }).filter(d => d.consumption !== null)

  if (data.length === 0) {
    return <div className="card">Add at least two refuels to see the consumption chart.</div>
  }

  return (
    <div className="card">
      <h3 style={{ fontSize: '14px' }}>Consumption (L/100km) Over Time</h3>
      <div style={{ width: '100%', height: 245 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="consumption" stroke="#3b82f6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
