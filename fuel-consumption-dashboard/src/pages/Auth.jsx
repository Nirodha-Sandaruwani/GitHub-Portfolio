import React, { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { addUser, setCurrentUser } from '../store/slices/usersSlice'
import '../styles/auth.css'

export default function Auth() {
  const dispatch = useDispatch()
  const usersFromStore = useSelector(s => s.users?.users || [])
  const navigate = useNavigate()
  const location = useLocation()

  const initialSignup = location.pathname.includes('signup') || location.hash.includes('#/signup')
  const [isSignup, setIsSignup] = useState(initialSignup)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    setIsSignup(location.pathname.includes('signup') || location.hash.includes('#/signup'))
  }, [location])

  function getUsersSnapshot() {
    if (usersFromStore && usersFromStore.length) return usersFromStore
    try {
      const raw = localStorage.getItem('users')
      return raw ? JSON.parse(raw) : []
    } catch {
      return []
    }
  }

  const toggleMode = () => {
    setIsSignup(v => !v)
    setError('')
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const users = getUsersSnapshot()

    if (isSignup) {
      if (users.find(u => u.email === email)) {
        setError('Email already exists.')
        return
      }
      const id = Date.now().toString()
      const newUser = { id, username, email, password, records: [] }
      dispatch(addUser(newUser))
      dispatch(setCurrentUser(id))
      localStorage.setItem('auth', JSON.stringify({ id, username, email }))
      localStorage.setItem('users', JSON.stringify([...users, newUser]))
      navigate('/dashboard')
    } else {
      const found = users.find(u => u.email === email && u.password === password)
      if (!found) {
        setError('Invalid email or password.')
        return
      }
      dispatch(setCurrentUser(found.id))
      localStorage.setItem('auth', JSON.stringify({ id: found.id, username: found.username, email: found.email }))
      navigate('/dashboard')
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>{isSignup ? 'Create Account' : 'Welcome Back'}</h2>
        <form onSubmit={handleSubmit}>
          {isSignup && (
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          )}
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
          {error && <p className="error">{error}</p>}
          <button type="submit">{isSignup ? 'Sign Up' : 'Log In'}</button>
        </form>

        {/* added marginTop */}
        <p className="toggle" style={{ marginTop: '1rem' }}>
          {isSignup ? (
            <>
              Already have an account?{' '}
              <span onClick={toggleMode} style={{ cursor: 'pointer', color: '#3b82f6', fontWeight: 'bold' }}>
                Log In
              </span>
            </>
          ) : (
            <>
              Don't have an account?{' '}
              <span onClick={toggleMode} style={{ cursor: 'pointer', color: '#3b82f6', fontWeight: 'bold' }}>
                Sign Up
              </span>
            </>
          )}
        </p>
      </div>
    </div>
  )
}
