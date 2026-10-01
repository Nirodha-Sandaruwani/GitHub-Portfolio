// src/store/index.js
import { configureStore, combineReducers } from '@reduxjs/toolkit'
import usersReducer from './slices/usersSlice'
import refuelsReducer from './slices/refuelsSlice'
import carsReducer from './slices/carsSlice'

// Combine all slices
const rootReducer = combineReducers({
  users: usersReducer,
  refuels: refuelsReducer,
  cars: carsReducer
})

// Load persisted state
function loadState() {
  try {
    const raw = localStorage.getItem('fuel_app_state')
    if (!raw) return undefined
    return JSON.parse(raw)
  } catch (err) {
    console.warn('Failed to load persisted state', err)
    return undefined
  }
}

// Save state
function saveState(state) {
  try {
    localStorage.setItem('fuel_app_state', JSON.stringify(state))
  } catch (err) {
    console.warn('Failed to save state', err)
  }
}

const preloadedState = loadState()

export const store = configureStore({
  reducer: rootReducer,
  preloadedState
})

store.subscribe(() => {
  saveState(store.getState())
})

export default store
