// src/store/slices/carsSlice.js
import { createSlice } from '@reduxjs/toolkit'

// Load initial state from localStorage
const initialState = JSON.parse(
  localStorage.getItem('carsState') ||
  JSON.stringify({ cars: [{ id: 1, name: 'My Car' }], selectedCarId: 1 })
)

const carsSlice = createSlice({
  name: 'cars',
  initialState,
  reducers: {
    addCar: (state, action) => {
      state.cars.push(action.payload)
      localStorage.setItem('carsState', JSON.stringify(state))
    },
    selectCar: (state, action) => {
      state.selectedCarId = action.payload
      localStorage.setItem('carsState', JSON.stringify(state))
    }
  }
})

export const { addCar, selectCar } = carsSlice.actions
export default carsSlice.reducer
