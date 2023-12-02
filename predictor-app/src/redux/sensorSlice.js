import { createSlice } from '@reduxjs/toolkit';

export const sensorSlice = createSlice({
  name: 'sensor',
  initialState: {
    sensors: undefined,
    isLoading: false,
    hasError: false,
    errorMessage: null,
  },
  reducers: {
    setSensors: (state, action) => {
      console.log(state, action);
      state.sensors = action.payload;
    },
  },
});

export const { setSensors } = sensorSlice.actions;
export const sensorReducer = sensorSlice.reducer;