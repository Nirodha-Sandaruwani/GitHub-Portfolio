// src/components/RefuelList.jsx
import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { removeRefuel } from '../store/slices/refuelsSlice'

export default function RefuelList() {
  const dispatch = useDispatch()
  const reduxUserId = useSelector(s => s.users?.currentUserId)
  const allRefuels = useSelector(s => s.refuels || [])
  const auth = (() => { try { return JSON.parse(localStorage.getItem('auth') || '{}') } catch { return {} } })()
  const userId = reduxUserId || auth?.id || auth?.email

  if (!userId) {
    return <div className="card">Please login to see refuels.</div>
  }

  const refuels = (allRefuels || []).filter(r => r.userId == userId) // loose check so id/email work

  const totalKm = refuels.reduce((acc, r, i) => (i === 0 ? acc : acc + Math.max(0, r.km - refuels[i - 1].km)), 0)
  const totalCost = refuels.reduce((acc, r) => acc + r.liters * r.price, 0)
  const avgConsumption = refuels.length > 1
    ? refuels.reduce((acc, r, i) => {
      if (i === 0) return acc
      const d = r.km - refuels[i - 1].km
      if (d > 0) return acc + (r.liters / d) * 100
      return acc
    }, 0) / (refuels.length - 1)
    : 0

  return (
    <div className="card" style={{ padding: '1rem' }}>
      <h2 style={{ marginBottom: '1rem', textAlign: 'center', color: '#1e40af', fontSize: '15px' }}>
        Refuel Events
      </h2>

      {refuels.length === 0 ? (
        <p style={{ textAlign: 'center' }}>No refuels yet.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {refuels.map((r, i) => {
            const prev = refuels[i - 1]
            const distance = prev ? Math.max(0, r.km - prev.km) : 0
            const cost = r.liters * r.price
            const consumption = distance > 0 ? ((r.liters / distance) * 100).toFixed(2) : '-'
            return (
              <div key={r.id} style={{
                background: '#f8fafc', padding: '1rem', borderRadius: '8px', boxShadow: '0 2px 6px rgba(0,0,0,0.06)',
                display: 'flex', flexDirection: 'column', gap: '0.5rem'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <strong style={{ color: '#1f3b8a', fontSize: '14px' }}>Date: {r.date}</strong>
                  <button onClick={() => dispatch(removeRefuel(r.id))} style={{
                    background: '#ef4444', color: '#fff', border: 'none', padding: '0.3rem 0.6rem', borderRadius: '6px', cursor: 'pointer'
                  }}>Remove</button>
                </div>

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', fontSize: '14px' }}>
                  <div style={{ flex: '1 1 45%' }}><strong>Km:</strong> {r.km}</div>
                  <div style={{ flex: '1 1 45%' }}><strong>Δ km:</strong> {distance || '-'}</div>
                  <div style={{ flex: '1 1 45%' }}><strong>Liters:</strong> {r.liters}</div>
                  <div style={{ flex: '1 1 45%' }}><strong>Price/L:</strong> {r.price}</div>
                  <div style={{ flex: '1 1 45%' }}><strong>Cost:</strong> {cost.toFixed(2)}</div>
                  <div style={{ flex: '1 1 45%' }}><strong>Cons L/100km:</strong> {consumption}</div>
                </div>
              </div>
            )
          })}

          <div style={{
            marginTop: '1rem', padding: '1rem', background: '#e0f2fe', borderRadius: '8px', textAlign: 'center', fontWeight: '600'
          }}>
            <p>Total km: {totalKm}</p>
            <p>Total cost: {totalCost.toFixed(2)}</p>
            <p>Avg L/100km: {avgConsumption ? avgConsumption.toFixed(2) : '-'}</p>
          </div>
        </div>
      )}
    </div>
  )
}
