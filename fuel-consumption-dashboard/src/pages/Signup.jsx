import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/auth.css'

export default function Signup() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const basePath = window.location.hostname.includes('student.labranet.jamk.fi')
    ? '/~ad9906/e15-consumption-monitoring'
    : ''

  const handleSignup = (e) => {
    e.preventDefault()
    const users = JSON.parse(localStorage.getItem('users') || '[]')

    if (users.find(u => u.email === email)) {
      alert('Email already exists.')
      return
    }

    const newUser = { id: Date.now(), username, email, password, records: [] }
    users.push(newUser)
    localStorage.setItem('users', JSON.stringify(users))
    localStorage.setItem('auth', JSON.stringify({ username, email }))

    navigate(`${basePath}/#/dashboard`)
  }

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>Sign Up</h2>
        <form onSubmit={handleSignup}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
        {/* added marginTop */}
        <p className="toggle" style={{ marginTop: '1rem' }}>
          Already have an account?{' '}
          <span style={{ cursor: 'pointer', color: '#2563eb' }} onClick={() => navigate(`${basePath}/#/login`)}>
            Login
          </span>
        </p>
      </div>
    </div>
  )
}
