import { getFormattedAppName } from '@/lib/app-name';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export const metadata = {
  title: 'About',
  description: `Learn more about ${getFormattedAppName()}`,
};

export default function AboutPage() {
  const appName = getFormattedAppName();

  return (
    <div className="container max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">About {appName}</h1>
      
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
          <p className="text-muted-foreground leading-relaxed">
            {appName} is a community knowledge platform that empowers teams and communities to 
            share, discover, and learn together. We believe that collective knowledge is more 
            powerful when it's easily accessible and searchable.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">What We Do</h2>
          <p className="text-muted-foreground leading-relaxed mb-4">
            Our platform combines the power of Retrieval-Augmented Generation (RAG) technology 
            with intuitive collaboration tools to help you:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
            <li>Upload and organize your private documents</li>
            <li>Ask questions and get instant, accurate answers</li>
            <li>Build a searchable knowledge base for your community</li>
            <li>Collaborate on questions and answers</li>
            <li>Discover insights from your collective knowledge</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Technology</h2>
          <p className="text-muted-foreground leading-relaxed">
            Built with cutting-edge RAG technology, {appName} uses advanced AI to understand 
            your documents and provide contextually relevant answers. Our platform ensures your 
            data remains secure and private while delivering powerful search and discovery capabilities.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Get Started</h2>
          <p className="text-muted-foreground leading-relaxed mb-6">
            Ready to transform how your community shares knowledge? Join us today and start 
            building your knowledge base.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Button className="h-11 w-full sm:w-auto bg-primary text-white hover:bg-primary/90" asChild>
              <Link href="/signup">Sign Up</Link>
            </Button>
            <Button className="h-11 w-full sm:w-auto border border-border bg-background text-foreground hover:bg-accent" variant="outline" asChild>
              <Link href="/">Learn More</Link>
            </Button>
          </div>
        </section>
      </div>
    </div>
  );
}
