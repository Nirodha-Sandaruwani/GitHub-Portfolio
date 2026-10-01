// src/components/PrivateRoute.jsx
import React from 'react'
import { useSelector } from 'react-redux'
import { Navigate } from 'react-router-dom'

export default function PrivateRoute({ children }) {
  const currentUserId = useSelector(s => s.users.currentUserId)
  return currentUserId ? children : <Navigate to="/login" replace />
}
