import { baseApi } from './baseApi';

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
  sources: string[];
  conversation_id: string;
  timestamp?: string;
}

// Chat API endpoints
export const chatApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    sendMessage: builder.mutation<ChatResponse, ChatRequest>({
      query: (body) => ({
        url: '/chat',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Chat'],
    }),
  }),
});

// Export hooks for usage in components
export const { useSendMessageMutation } = chatApi;

