import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { fetchComplaints, fetchComplaintById, saveComplaint, updateComplaint, analyzeComplaintText } from '../services/api';

export const getComplaints = createAsyncThunk(
  'complaints/getComplaints',
  async (params, { rejectWithValue }) => {
    try {
      return await fetchComplaints(params);
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

export const getComplaintById = createAsyncThunk(
  'complaints/getComplaintById',
  async (id, { rejectWithValue }) => {
    try {
      return await fetchComplaintById(id);
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

export const analyzeComplaint = createAsyncThunk(
  'complaints/analyzeComplaint',
  async ({ text, sourceType }, { rejectWithValue }) => {
    try {
      return await analyzeComplaintText(text, sourceType);
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

export const createNewComplaint = createAsyncThunk(
  'complaints/createNewComplaint',
  async (complaintData, { rejectWithValue }) => {
    try {
      return await saveComplaint(complaintData);
    } catch (err) {
      return rejectWithValue(err.message);
    }
  }
);

const complaintSlice = createSlice({
  name: 'complaints',
  initialState: {
    items: [],
    selectedComplaint: null,
    aiAnalysisResult: null,
    loading: false,
    aiAnalyzing: false,
    saving: false,
    error: null
  },
  reducers: {
    clearAIAnalysis: (state) => {
      state.aiAnalysisResult = null;
    },
    clearSelectedComplaint: (state) => {
      state.selectedComplaint = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // getComplaints
      .addCase(getComplaints.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getComplaints.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(getComplaints.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // getComplaintById
      .addCase(getComplaintById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getComplaintById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedComplaint = action.payload;
      })
      .addCase(getComplaintById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // analyzeComplaint
      .addCase(analyzeComplaint.pending, (state) => {
        state.aiAnalyzing = true;
        state.error = null;
      })
      .addCase(analyzeComplaint.fulfilled, (state, action) => {
        state.aiAnalyzing = false;
        state.aiAnalysisResult = action.payload;
      })
      .addCase(analyzeComplaint.rejected, (state, action) => {
        state.aiAnalyzing = false;
        state.error = action.payload;
      })
      // createNewComplaint
      .addCase(createNewComplaint.pending, (state) => {
        state.saving = true;
        state.error = null;
      })
      .addCase(createNewComplaint.fulfilled, (state, action) => {
        state.saving = false;
        state.items.unshift(action.payload);
      })
      .addCase(createNewComplaint.rejected, (state, action) => {
        state.saving = false;
        state.error = action.payload;
      });
  }
});

export const { clearAIAnalysis, clearSelectedComplaint } = complaintSlice.actions;
export default complaintSlice.reducer;
