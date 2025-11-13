import { baseApi } from './baseApi';

export interface DocumentUploadResponse {
  message: string;
  filename?: string;
  chunks_count?: number;
  count?: number;
}

// Document API endpoints
export const documentApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    uploadDocument: builder.mutation<DocumentUploadResponse, FormData>({
      query: (formData) => ({
        url: '/documents/upload',
        method: 'POST',
        body: formData,
      }),
      invalidatesTags: ['Document'],
    }),
    addDocuments: builder.mutation<
      DocumentUploadResponse,
      { directory?: string }
    >({
      query: ({ directory = 'data/documents' }) => ({
        url: '/documents',
        method: 'POST',
        params: { directory },
      }),
      invalidatesTags: ['Document'],
    }),
  }),
});

// Export hooks for usage in components
export const { useUploadDocumentMutation, useAddDocumentsMutation } =
  documentApi;

