import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchDashboardSummary } from '../services/api';

export const getDashboardSummary = createAsyncThunk(
  'dashboard/getDashboardSummary',
  async (_, { rejectWithValue }) => {
    try {
      return await fetchDashboardSummary();
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState: {
    summary: null,
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getDashboardSummary.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getDashboardSummary.fulfilled, (state, action) => {
        state.loading = false;
        state.summary = action.payload;
      })
      .addCase(getDashboardSummary.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

export default dashboardSlice.reducer;
