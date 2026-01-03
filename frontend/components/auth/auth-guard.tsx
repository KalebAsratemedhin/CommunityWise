'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useMeQuery } from '@/lib/api';

interface AuthGuardProps {
  children: React.ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const router = useRouter();
  const { data: user, isLoading, isError } = useMeQuery();

  useEffect(() => {
    if (!isLoading && isError) {
      // Not authenticated, redirect to login
      router.push('/login');
    }
  }, [isLoading, isError, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    );
  }

  if (isError || !user) {
    return null; // Will redirect
  }

  return <>{children}</>;
}














