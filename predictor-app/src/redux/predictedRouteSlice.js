import { createSlice } from '@reduxjs/toolkit';

export const predictedRouteSlice = createSlice({
  name: 'predictedRoute',
  initialState: {
    predictedRoute : [
      [
        47.4156038,
        9.3325804
      ],
      {
        "date": "Sat, 21 May 2022 00:00:00 GMT",
        "lat": "47.4351834416",
        "level": 0.1217434210526317,
        "lng": "9.3918149135",
        "sensor_id": "107132 | 255E",
        "type": "Glas / Grün,YMATRON"
      },
      {
        "date": "Mon, 10 Oct 2022 00:00:00 GMT",
        "lat": "47.412065012904804",
        "level": 0.6643749999999999,
        "lng": "9.335980774191682",
        "sensor_id": "107026 | 67BE",
        "type": "YMATRON,Glas / Braun"
      },
      {
        "date": "Mon, 10 Oct 2022 00:00:00 GMT",
        "lat": "47.41208",
        "level": 0.4225,
        "lng": "9.33586",
        "sensor_id": "107068 | 4455",
        "type": "YMATRON,Glas / Grün"
      },
      {
        "date": "Mon, 10 Oct 2022 00:00:00 GMT",
        "lat": "47.41209608066285",
        "level": 0.40874999999999995,
        "lng": "9.33591068841119",
        "sensor_id": "107072 | F389",
        "type": "Glas / Weiss,YMATRON"
      },
      {
        "date": "Mon, 10 Oct 2022 00:00:00 GMT",
        "lat": "47.40792974774064",
        "level": 0.67225,
        "lng": "9.33352525794038",
        "sensor_id": "107065 | 4A3D",
        "type": "Glas / Weiss,YMATRON"
      },
      {
        "date": "Mon, 10 Oct 2022 00:00:00 GMT",
        "lat": "47.40798",
        "level": 0.6775,
        "lng": "9.33388",
        "sensor_id": "107077 | 2CC4",
        "type": "YMATRON,Glas / Grün"
      },
      [
        47.4156038,
        9.3325804
      ]
    ],
  },
  reducers: {
    setPredictedRoute: (state, action) => {
      state.predictedRoute = action.payload;
    },
  },
});

export const { setPredictedRoute } = predictedRouteSlice.actions;
export const predictedRouteReducer = predictedRouteSlice.reducer;