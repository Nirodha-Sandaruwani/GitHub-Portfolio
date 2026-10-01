// src/store/slices/refuelsSlice.js
import { createSlice } from '@reduxjs/toolkit'

// Initialize refuels from localStorage
const initialState = JSON.parse(localStorage.getItem('refuels') || '[]')

const refuelsSlice = createSlice({
  name: 'refuels',
  initialState,
  reducers: {
    addRefuel(state, action) {
      state.push(action.payload)
      localStorage.setItem('refuels', JSON.stringify(state))
    },
    removeRefuel(state, action) {
      const newState = state.filter(r => r.id !== action.payload)
      localStorage.setItem('refuels', JSON.stringify(newState))
      return newState
    },
    clearAllForUser(state, action) {
      const userId = action.payload
      const newState = state.filter(r => r.userId !== userId)
      localStorage.setItem('refuels', JSON.stringify(newState))
      return newState
    }
  }
})

export const { addRefuel, removeRefuel, clearAllForUser } = refuelsSlice.actions
export default refuelsSlice.reducer
