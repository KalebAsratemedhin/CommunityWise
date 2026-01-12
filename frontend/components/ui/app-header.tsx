'use client';

import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuItem } from '@/components/ui/dropdown-menu';
import { LogOut, MessageSquare, HelpCircle, Moon, Sun, User } from 'lucide-react';
import { useMeQuery } from '@/lib/api';
import { getFormattedAppName } from '@/lib/app-name';
import { useState, useEffect } from 'react';

export function AppHeader() {
  const router = useRouter();
  const pathname = usePathname();
  const { data: user, isLoading } = useMeQuery();
  const appName = getFormattedAppName();
  const isAuthenticated = !!user && !isLoading;
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const root = document.documentElement;
    const stored = localStorage.getItem('theme');
    const initial: 'light' | 'dark' =
      stored === 'light' || stored === 'dark'
        ? stored
        : root.classList.contains('dark')
        ? 'dark'
        : 'light';
    setTheme(initial);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    router.push('/');
  };

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    const root = document.documentElement;
    root.classList.toggle('dark', next === 'dark');
    localStorage.setItem('theme', next);
  };

  const getInitials = (email: string) => {
    return email.substring(0, 2).toUpperCase();
  };

  return (
    <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link 
          href="/" 
          className="text-2xl font-semibold tracking-wide text-primary hover:opacity-80 transition-opacity"
          style={{ fontFamily: 'var(--font-dancing)' }}
        >
          {appName}
        </Link>

        {isAuthenticated && (
          <nav className="absolute left-1/2 transform -translate-x-1/2 flex items-center gap-6">
            <Link
              href="/chat"
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                pathname === '/chat'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
              }`}
            >
              <MessageSquare className="h-4 w-4" />
              Chat
            </Link>
            <Link
              href="/questions"
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                pathname?.startsWith('/questions')
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
              }`}
            >
              <HelpCircle className="h-4 w-4" />
              Q&A
            </Link>
          </nav>
        )}

        <div className="flex items-center gap-2">
          {isAuthenticated ? (
            <DropdownMenu
              trigger={
                <button className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-primary-foreground hover:opacity-80 transition-opacity cursor-pointer">
                  {user?.email ? (
                    <span className="text-sm font-medium">{getInitials(user.email)}</span>
                  ) : (
                    <User className="h-5 w-5" />
                  )}
                </button>
              }
            >
              <DropdownMenuItem onClick={toggleTheme}>
                <div className="flex items-center gap-3">
                  {theme === 'dark' ? (
                    <>
                      <Sun className="h-4 w-4" />
                      <span>Light Mode</span>
                    </>
                  ) : (
                    <>
                      <Moon className="h-4 w-4" />
                      <span>Dark Mode</span>
                    </>
                  )}
                </div>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleLogout}>
                <div className="flex items-center gap-3">
                  <LogOut className="h-4 w-4" />
                  <span>Logout</span>
                </div>
              </DropdownMenuItem>
            </DropdownMenu>
          ) : (
            <div className="flex gap-2">
              <Button variant="ghost" size="sm" asChild>
                <Link href="/login">Sign In</Link>
              </Button>
              <Button size="sm" asChild>
                <Link href="/signup">Sign Up</Link>
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

