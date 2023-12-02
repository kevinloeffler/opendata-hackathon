import {configureStore} from "@reduxjs/toolkit";
import {sensorReducer} from "./sensorSlice";
import {predictedRouteReducer} from "./predictedRouteSlice";

const store = configureStore({
    reducer: {
        sensor: sensorReducer,
        predictedRoute: predictedRouteReducer,
    },
});

export default store;

