import React from 'react'
import { useSelector } from 'react-redux'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

export default function PieChartComponent() {
  // --- Auth + user logic (works both local & JAMK) ---
  const reduxUserId = useSelector(s => s.users?.currentUserId)
  const allRefuels  = useSelector(s => s.refuels || [])
  const auth = (() => {
    try { return JSON.parse(localStorage.getItem('auth') || '{}') }
    catch { return {} }
  })()
  const userId = reduxUserId || auth?.id || auth?.email

  if (!userId) {
    return (
      <div style={{ padding: '0.5rem' }}>
        <h2 style={{ marginBottom: '5px', textAlign: 'center', color: '#1e40af', fontSize: '15px' }}>
          Fuel Costs Distribution
        </h2>
        <p style={{ textAlign: 'center', color: '#64748b' }}>
          Please login to view fuel cost distribution.
        </p>
      </div>
    )
  }

  // --- Data ---
  const refuels = (allRefuels || []).filter(r => r.userId == userId)
  const data = refuels.map(r => ({ name: r.date, value: r.liters * r.price }))

  const COLORS = [
    '#4f46e5', '#f97316', '#10b981', '#f43f5e',
    '#3b82f6', '#a855f7', '#14b8a6', '#ef4444'
  ]

  if (!data.length) {
    return (
      <div style={{ padding: '0.5rem' }}>
        <h2 style={{ marginBottom: '5px', textAlign: 'center', color: '#1e40af', fontSize: '15px' }}>
          Fuel Costs Distribution
        </h2>
        <p style={{ textAlign: 'center', color: '#64748b' }}>No refuel data yet.</p>
      </div>
    )
  }

  // --- Percentage labels inside slices ---
  const renderLabelInside = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const RADIAN = Math.PI / 180
    const radius = innerRadius + (outerRadius - innerRadius) / 2
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)
    return (
      <text
        x={x}
        y={y}
        fill="#fff"
        textAnchor="middle"
        dominantBaseline="central"
        fontSize="12px"
        fontWeight="500"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  return (
    <div style={{ padding: '0.5rem' }}>
      <h2
        style={{
          marginBottom: '5px',
          textAlign: 'center',
          color: '#1e40af',
          fontSize: '15px'
        }}
      >
        Fuel Costs Distribution
      </h2>

      {/* Pie chart */}
      <ResponsiveContainer width="100%" height={150}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={70}
            label={renderLabelInside}
            labelLine={false}        // ❌ remove outside label lines
          >
            {data.map((entry, i) => (
              <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(v) => [`$${v.toFixed(2)}`, 'Cost']} />
        </PieChart>
      </ResponsiveContainer>

      {/* Dates legend under the circle */}
      <div
        style={{
          marginTop: '8px',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '6px'
        }}
      >
        {data.map((entry, i) => (
          <div
            key={`legend-${i}`}
            style={{ display: 'flex', alignItems: 'center', fontSize: '12px' }}
          >
            <span
              style={{
                width: '12px',
                height: '12px',
                backgroundColor: COLORS[i % COLORS.length],
                borderRadius: '3px',
                display: 'inline-block',
                marginRight: '4px'
              }}
            />
            {entry.name}
          </div>
        ))}
      </div>
    </div>
  )
}
