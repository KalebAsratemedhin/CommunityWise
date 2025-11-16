import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const getBaseUrl = () => {
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }
  return 'http://localhost:8000';
};

// Base API slice with common configuration
export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: getBaseUrl(),
    // Note: do NOT force Content-Type here so that FormData uploads work.
  }),
  tagTypes: ['Chat', 'Document'],
  endpoints: () => ({}), // Endpoints will be injected by other API slices
});

