// src/components/RefuelForm.jsx
import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { addRefuel } from '../store/slices/refuelsSlice'
import { useNavigate } from 'react-router-dom'

export default function RefuelForm() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const reduxUserId = useSelector(s => s.users?.currentUserId)
  const auth = (() => { try { return JSON.parse(localStorage.getItem('auth') || '{}') } catch { return {} } })()
  const userId = reduxUserId || auth?.id || auth?.email

  const [date, setDate] = useState('')
  const [km, setKm] = useState('')
  const [liters, setLiters] = useState('')
  const [price, setPrice] = useState('')

  if (!userId) {
    return (
      <div className="card">
        <p>Please <button onClick={() => navigate('/login')}>login</button> to add refuels.</p>
      </div>
    )
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!date || !km || !liters || !price) return alert('Fill all fields')
    const id = Date.now().toString() + Math.floor(Math.random() * 1000).toString()
    dispatch(addRefuel({
      id,
      userId,
      date,
      km: Number(km),
      liters: Number(liters),
      price: Number(price)
    }))
    setDate('')
    setKm('')
    setLiters('')
    setPrice('')
  }

  return (
    <div className="card">
      <h2>Add Refuel</h2>
      <form
        onSubmit={handleSubmit}
        className="refuel-form"
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0.5rem',
          alignItems: 'center'
        }}
      >
        <input
          type="date"
          value={date}
          onChange={e => setDate(e.target.value)}
          style={{ flex: '1 1 160px' }}
        />
        <input
          type="number"
          placeholder="Kilometers"
          value={km}
          onChange={e => setKm(e.target.value)}
          style={{ flex: '1 1 120px' }}
        />
        <input
          type="number"
          placeholder="Liters"
          value={liters}
          onChange={e => setLiters(e.target.value)}
          style={{ flex: '1 1 100px' }}
        />
        {/* Price + Button share the same row */}
        <div
          style={{
            display: 'flex',
            flex: '1 1 auto',
            gap: '0.5rem',
            alignItems: 'center'
          }}
        >
          <input
            type="number"
            placeholder="Price per Liter"
            value={price}
            onChange={e => setPrice(e.target.value)}
            style={{ flex: '1 1 120px' }}
          />
          <button
            type="submit"
            style={{
              flex: '0 0 auto',
              padding: '0.6rem 1rem',
              backgroundColor: '#2563eb',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer'
            }}
          >
            Add Refuel
          </button>
        </div>
      </form>
    </div>
  )
}
