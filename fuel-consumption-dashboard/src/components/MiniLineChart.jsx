import React from 'react'
import { useSelector } from 'react-redux'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function MiniLineChart() {
  const refuels = useSelector(state => state.refuels)

  // Take last 5 refuels
  const lastRefuels = refuels.slice(-5)

  const data = lastRefuels.map((r, index) => ({
    date: r.date,
    liters: r.liters
  }))

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <h4 style={{ textAlign: 'center', marginBottom: '0.3rem', marginTop: '0.3rem' ,fontSize: '15px', color: '#1e40af' }}>Last 5 Refuels</h4>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="liters" stroke="#2563eb" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
