import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

import router from './router'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider } from 'react-router'

const qClient= new QueryClient(
  {
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false
      }
    }
  }
);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={qClient}>
      {/* <App /> */}
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
