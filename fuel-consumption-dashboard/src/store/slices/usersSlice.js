// src/store/slices/usersSlice.js
import { createSlice } from '@reduxjs/toolkit'

const initialState = JSON.parse(
  localStorage.getItem('usersState') || 
  JSON.stringify({ users: [], currentUserId: null })
)

const usersSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    addUser(state, action) {
      state.users.push(action.payload)
      localStorage.setItem('usersState', JSON.stringify(state))
    },
    setCurrentUser(state, action) {
      state.currentUserId = action.payload
      localStorage.setItem('usersState', JSON.stringify(state))
    },
    logout(state) {
      state.currentUserId = null
      localStorage.setItem('usersState', JSON.stringify(state))
    },
    updateUser(state, action) {
      const { id, ...rest } = action.payload
      const u = state.users.find(x => x.id === id)
      if (u) Object.assign(u, rest)
      localStorage.setItem('usersState', JSON.stringify(state))
    }
  }
})

export const { addUser, setCurrentUser, logout, updateUser } = usersSlice.actions
export default usersSlice.reducer
