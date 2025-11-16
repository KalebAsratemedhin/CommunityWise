'use client';

import { ThemeToggle } from '@/components/ui/theme-toggle';

export function ChatHeader() {
  return (
    <header className="sticky top-0 z-20 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center px-4 justify-between">
        <h1 className="text-lg font-semibold">RAG Chat Bot</h1>
        <ThemeToggle />
      </div>
    </header>
  );
}

