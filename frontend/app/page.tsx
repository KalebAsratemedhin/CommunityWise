'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { getFormattedAppName } from '@/lib/app-name';

export default function LandingPage() {
  const appName = getFormattedAppName();

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Hero Section */}
      <main className="flex-1">
        <div style={{ backgroundColor: 'oklch(0.97 0.005 0)' }}>
          <section className="container mx-auto px-4 min-h-[80vh] flex items-center">
          <div className="max-w-6xl mx-auto w-full py-12">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div className="text-center md:text-left">
                <div className="max-w-xl mx-auto md:mx-0">
            <h2 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
              Your Community Knowledge Hub
            </h2>
                <p className="text-xl text-muted-foreground mb-8">
                  Connect, share, and discover knowledge with AI-powered search. Upload documents, ask questions, and build a smarter community together.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
                  <Button size="lg" asChild>
                    <Link href="/signup">Get Started</Link>
                  </Button>
                  <Button size="lg" variant="outline" asChild>
                    <Link href="/login">Sign In</Link>
                  </Button>
                </div>
                </div>
              </div>
              <div className="hidden md:block relative w-full h-full min-h-[400px] rounded-lg overflow-hidden">
                <Image
                  src="/premium_vector-1682300886606-340e0724b946.avif"
                  alt="Community"
                  fill
                  className="object-contain"
                  unoptimized
                />
              </div>
            </div>
          </div>
          </section>
        </div>

        {/* Features Section */}
        <div style={{ backgroundColor: 'oklch(0.98 0.012 240)' }}>
          <section className="container mx-auto px-4 min-h-[80vh] flex items-center py-12">
            <div className="max-w-6xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">Powerful Features</h3>
            <div className="grid md:grid-cols-3 gap-8 items-center">
              <div className="text-center">
                <div className="relative w-full h-48 mb-4 mx-auto rounded-lg overflow-hidden">
                  <Image
                    src="/premium_vector-1683141305195-6cdfd5214b49.avif"
                    alt="Community"
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
                <h4 className="text-xl font-semibold mb-2">Community Knowledge</h4>
                <p className="text-muted-foreground">
                  Gather and share knowledge with your community. Build a collective knowledge base that grows with every contribution.
                </p>
              </div>
              <div className="text-center">
                <div className="relative w-full h-48 mb-4 mx-auto rounded-lg overflow-hidden">
                  <Image
                    src="/premium_vector-1745447697638-4cb1ea348dbf.avif"
                    alt="AI Assistant"
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
                <h4 className="text-xl font-semibold mb-2">AI Assistant</h4>
                <p className="text-muted-foreground">
                  Get instant answers powered by RAG technology. Ask questions and discover information faster than ever.
                </p>
              </div>
              <div className="text-center">
                <div className="relative w-full h-48 mb-4 mx-auto rounded-lg overflow-hidden">
                  <Image
                    src="/premium_vector-1763370265947-63ed2860f891.avif"
                    alt="Documents"
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
                <h4 className="text-xl font-semibold mb-2">Private Documents</h4>
                <p className="text-muted-foreground">
                  Upload and search through your private documents securely. RAG-based search finds exactly what you need.
                </p>
              </div>
            </div>
            </div>
          </section>
        </div>

        {/* How It Works Section */}
        <div style={{ backgroundColor: 'oklch(0.97 0.005 0)' }}>
          <section className="container mx-auto px-4 min-h-[80vh] flex items-center py-12">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">How It Works</h3>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                  1
                </div>
                <h4 className="text-lg font-semibold mb-3">Sign Up</h4>
                <p className="text-muted-foreground">
                  Create your account in seconds. No credit card required to get started.
                </p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                  2
                </div>
                <h4 className="text-lg font-semibold mb-3">Upload Documents</h4>
                <p className="text-muted-foreground">
                  Add your documents to build your knowledge base. Support for various file formats.
                </p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                  3
                </div>
                <h4 className="text-lg font-semibold mb-3">Ask & Discover</h4>
                <p className="text-muted-foreground">
                  Ask questions and get instant answers. Share knowledge with your community.
                </p>
              </div>
            </div>
          </div>
          </section>
        </div>

        {/* Benefits Section */}
        <div style={{ backgroundColor: 'oklch(0.98 0.012 240)' }}>
          <section className="container mx-auto px-4 min-h-[80vh] flex items-center py-12">
            <div className="max-w-5xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">Why Choose {appName}?</h3>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h4 className="text-lg font-semibold mb-2">Secure & Private</h4>
                  <p className="text-muted-foreground">
                    Your documents are encrypted and stored securely. You have full control over your data.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h4 className="text-lg font-semibold mb-2">Fast & Accurate</h4>
                  <p className="text-muted-foreground">
                    Powered by advanced RAG technology for quick and precise answers from your documents.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h4 className="text-lg font-semibold mb-2">Collaborative</h4>
                  <p className="text-muted-foreground">
                    Build knowledge together. Share insights and learn from your community members.
                  </p>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h4 className="text-lg font-semibold mb-2">Easy to Use</h4>
                  <p className="text-muted-foreground">
                    Intuitive interface designed for everyone. No technical expertise required.
                  </p>
                </div>
              </div>
            </div>
            </div>
          </section>
        </div>

        {/* CTA Section */}
        <div style={{ backgroundColor: 'oklch(0.97 0.005 0)' }}>
          <section className="container mx-auto px-4 min-h-[80vh] flex items-center py-12">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-3xl font-bold mb-4">Ready to Get Started?</h3>
            <p className="text-lg text-muted-foreground mb-8">
              Join {appName} today and start building your community knowledge base.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link href="/signup">Create Your Account</Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/login">Sign In</Link>
              </Button>
            </div>
          </div>
          </section>
        </div>
      </main>
    </div>
  );
}
