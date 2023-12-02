import { createSlice } from '@reduxjs/toolkit';

export const predictedRouteSlice = createSlice({
  name: 'predictedRoute',
  initialState: {
    predictedRoute : undefined,
  },
  reducers: {
    setPredictedRoute: (state, action) => {
      state.predictedRoute = action.payload;
    },
  },
});

export const { setPredictedRoute } = predictedRouteSlice.actions;
export const predictedRouteReducer = predictedRouteSlice.reducer;