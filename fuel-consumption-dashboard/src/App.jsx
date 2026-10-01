// src/App.jsx
import React from 'react'
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom'
import Auth from './pages/Auth'
import Dashboard from './pages/Dashboard'

/**
 * Simple client-side protection: we use localStorage 'auth' as the source of truth.
 * HashRouter keeps everything working in a sub-folder (JAMK) without server rewrites.
 */
function PrivateRoute({ children }) {
  const auth = JSON.parse(localStorage.getItem('auth') || 'null')
  return auth && (auth.email || auth.username) ? children : <Navigate to="/login" replace />
}

export default function App() {
  const auth = JSON.parse(localStorage.getItem('auth') || 'null')

  return (
    <HashRouter>
      <Routes>
        {/* Auth page (login + signup handled inside the same component) */}
        <Route path="/login" element={<Auth />} />
        <Route path="/signup" element={<Auth />} />

        {/* Protected dashboard */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />

        {/* Root -> redirect based on auth */}
        <Route
          path="/"
          element={
            auth && (auth.username || auth.email)
              ? <Navigate to="/dashboard" replace />
              : <Navigate to="/login" replace />
          }
        />

        {/* Fallback: send unknown routes to root */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  )
}
