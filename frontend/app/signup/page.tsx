'use client';

import { FormEvent, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useSignupMutation, useMeQuery } from '@/lib/api';

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [signup, { isLoading, error }] = useSignupMutation();
  const { data: user } = useMeQuery();

  // Redirect if already logged in
  useEffect(() => {
    if (user) {
      router.push('/chat');
    }
  }, [user, router]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const result = await signup({ email, password }).unwrap();
      // Store the token (if signup now returns a token)
      if (result.access_token) {
        localStorage.setItem('access_token', result.access_token);
        router.push('/chat');
      } else {
        // Fallback: redirect to login if token not returned
        router.push('/login');
      }
    } catch (err: any) {
      console.error('Signup failed', err);
      if (err?.data) {
        console.error('Error details:', err.data);
      }
    }
  };

  // Show loading or nothing while checking auth
  if (user) {
    return null;
  }

  const appName = (process.env.NEXT_PUBLIC_APP_NAME || 'CommunityWise').replace(/([a-z])([A-Z])/g, '$1 $2');

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-12">
      <div className="w-full max-w-6xl grid md:grid-cols-2 gap-12 items-center">
        <div className="hidden md:block relative w-full h-full min-h-[500px] rounded-lg overflow-hidden">
          <Image
            src="/premium_vector-1682300886606-340e0724b946.avif"
            alt="Community"
            fill
            className="object-contain"
            unoptimized
          />
        </div>
        <div className="w-full max-w-md mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold mb-2">{appName}</h1>
            <p className="text-muted-foreground">Create your account to get started</p>
          </div>
          <div className="border rounded-xl p-8 bg-transparent">
          <h2 className="text-2xl font-semibold mb-6 text-center">
            Create an account
          </h2>
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="email">
                Email
              </label>
              <Input
                id="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="h-11"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="password">
                Password
              </label>
              <Input
                id="password"
                type="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="h-11"
              />
            </div>
            {error && (
              <div className="p-3 rounded-md bg-destructive/10 border border-destructive/20">
                <p className="text-sm text-destructive">
                  Failed to sign up. This email might already be registered.
                </p>
              </div>
            )}
            <Button type="submit" className="w-full h-11" disabled={isLoading}>
              {isLoading ? 'Creating account...' : 'Sign up'}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account?{' '}
            <button
              type="button"
              className="text-primary hover:underline font-medium"
              onClick={() => router.push('/login')}
            >
              Sign in
            </button>
          </p>
          </div>
        </div>
      </div>
    </div>
  );
}



