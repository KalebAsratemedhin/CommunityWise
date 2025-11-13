# RTK Query API Structure

This directory contains the RTK Query API definitions organized in a standard, scalable way.

## Structure

```
lib/api/
├── baseApi.ts        # Base API slice with common configuration
├── chatApi.ts        # Chat-related endpoints
├── documentApi.ts    # Document-related endpoints
├── index.ts          # Barrel export for convenient imports
└── README.md         # This file
```

## Architecture

### Base API (`baseApi.ts`)
- Defines the base API slice with common configuration
- Sets up base URL, headers, and tag types
- Provides the foundation for all other API slices

### Feature APIs
Each feature has its own API file:
- **chatApi.ts**: Chat endpoints (`/chat`)
- **documentApi.ts**: Document endpoints (`/documents`, `/documents/upload`)

### Store Integration
All APIs are automatically registered when imported in `store.ts`:
```typescript
import './api/chatApi';
import './api/documentApi';
```

## Usage

### In Components

```typescript
// Import hooks directly
import { useSendMessageMutation } from '@/lib/api';

// Or import from specific API
import { useSendMessageMutation } from '@/lib/api/chatApi';
```

### Adding New Endpoints

1. **Add to existing API file** (if related):
```typescript
// In chatApi.ts
export const chatApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // ... existing endpoints
    newEndpoint: builder.query<ResponseType, RequestType>({
      query: (params) => ({ url: '/new-endpoint', params }),
    }),
  }),
});
```

2. **Or create new API file** (if different domain):
```typescript
// In newApi.ts
import { baseApi } from './baseApi';

export const newApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // endpoints here
  }),
});
```

3. **Register in store.ts**:
```typescript
import './api/newApi';
```

## Benefits

- ✅ **Separation of Concerns**: Each API domain is isolated
- ✅ **Scalability**: Easy to add new endpoints/APIs
- ✅ **Type Safety**: TypeScript types for all requests/responses
- ✅ **Code Splitting**: Only load what you need
- ✅ **Standard Pattern**: Follows RTK Query best practices

