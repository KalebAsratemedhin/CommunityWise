import { baseApi } from './baseApi';

// Backend-aligned types
export interface DocumentUploadResponse {
  message: string;
  filename?: string;
  chunks_count?: number | null;
  s3_key?: string;
}

export interface DocumentIndexRequest {
  s3_key: string;
  filename?: string | null;
}

export interface DocumentIndexResponse {
  message: string;
  filename?: string;
  chunks_count: number;
  s3_key: string;
}

export interface DocumentInfo {
  key: string;
  size?: number;
  last_modified?: string;
  original_filename?: string;
  signed_url?: string;
}

export interface IndexedDocumentInfo {
  source: string;
  chunks_count: number;
  last_indexed_at?: string | null;
}

export interface IndexedDocumentDeleteResponse {
  source: string;
  deleted_chunks: number;
}

// Document API endpoints
export const documentApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // GET /documents/list
    listDocuments: builder.query<DocumentInfo[], void>({
      query: () => ({
        url: '/documents/list',
        method: 'GET',
      }),
      providesTags: ['Document'],
    }),

    // POST /documents/upload (multipart/form-data)
    uploadDocument: builder.mutation<DocumentUploadResponse, File>({
      query: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return {
          url: '/documents/upload',
          method: 'POST',
          body: formData,
        };
      },
      invalidatesTags: ['Document'],
    }),

    // POST /documents/index (JSON body)
    indexDocument: builder.mutation<DocumentIndexResponse, DocumentIndexRequest>({
      query: (body) => ({
        url: '/documents/index',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Document'],
    }),

    // GET /documents/indexed
    listIndexedDocuments: builder.query<IndexedDocumentInfo[], void>({
      query: () => ({
        url: '/documents/indexed',
        method: 'GET',
      }),
      providesTags: ['Document'],
    }),

    // DELETE /documents/indexed/{source}
    deleteIndexedDocument: builder.mutation<
      IndexedDocumentDeleteResponse,
      string
    >({
      query: (source) => ({
        url: `/documents/indexed/${encodeURIComponent(source)}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Document'],
    }),
  }),
});

// Export hooks for usage in components
export const {
  useListDocumentsQuery,
  useUploadDocumentMutation,
  useIndexDocumentMutation,
   useListIndexedDocumentsQuery,
   useDeleteIndexedDocumentMutation,
} = documentApi;

