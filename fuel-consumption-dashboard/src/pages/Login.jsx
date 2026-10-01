import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/auth.css'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const basePath = window.location.hostname.includes('student.labranet.jamk.fi')
    ? '/~ad9906/e15-consumption-monitoring'
    : ''

  const handleLogin = (e) => {
    e.preventDefault()
    const users = JSON.parse(localStorage.getItem('users') || '[]')
    const user = users.find(u => u.email === email && u.password === password)

    if (user) {
      localStorage.setItem('auth', JSON.stringify({ username: user.username, email: user.email }))
      navigate(`${basePath}/#/dashboard`)
    } else {
      setError('Invalid email or password')
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
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
          <button type="submit">Login</button>
        </form>
        {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        {/* added marginTop */}
        <p className="toggle" style={{ marginTop: '1rem' }}>
          Don't have an account?{' '}
          <span style={{ cursor: 'pointer', color: '#2563eb' }} onClick={() => navigate(`${basePath}/#/signup`)}>
            Sign Up
          </span>
        </p>
      </div>
    </div>
  )
}
