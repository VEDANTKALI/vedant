import { configureStore } from '@reduxjs/toolkit';
import complaintReducer from './complaintSlice';
import dashboardReducer from './dashboardSlice';

export const store = configureStore({
  reducer: {
    complaints: complaintReducer,
    dashboard: dashboardReducer,
  },
});
