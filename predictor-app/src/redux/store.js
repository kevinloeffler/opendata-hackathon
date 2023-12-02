import {configureStore} from "@reduxjs/toolkit";
import {sensorReducer} from "./sensorSlice";

const store = configureStore({
    reducer: {
        sensor: sensorReducer,
    },
});

export default store;

