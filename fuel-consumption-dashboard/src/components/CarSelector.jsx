import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { selectCar } from '../store/slices/carsSlice'

export default function CarSelector() {
  const cars = useSelector(state => state.cars.cars)
  const selectedCarId = useSelector(state => state.cars.selectedCarId)
  const dispatch = useDispatch()

  return (
    <div className="card">
      <h2>Select Car</h2>
      <select
        value={selectedCarId}
        onChange={e => dispatch(selectCar(Number(e.target.value)))}
      >
        {cars.map(car => (
          <option key={car.id} value={car.id}>
            {car.name}
          </option>
        ))}
      </select>
    </div>
  )
}
