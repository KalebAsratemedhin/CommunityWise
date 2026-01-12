import { getFormattedAppName } from '@/lib/app-name';

export const metadata = {
  title: 'Terms of Service',
  description: `Terms of Service for ${getFormattedAppName()}`,
};

export default function TermsPage() {
  const appName = getFormattedAppName();

  return (
    <div className="container max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Terms of Service</h1>
      
      <div className="prose prose-lg max-w-none space-y-6">
        <p className="text-sm text-muted-foreground">
          Last updated: {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Acceptance of Terms</h2>
          <p className="text-muted-foreground leading-relaxed">
            By accessing and using {appName}, you accept and agree to be bound by the terms 
            and provision of this agreement. If you do not agree to these terms, please do 
            not use our service.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Use License</h2>
          <p className="text-muted-foreground leading-relaxed mb-4">
            Permission is granted to use {appName} for personal and commercial purposes, subject 
            to the following restrictions:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
            <li>You must not use the service for any unlawful purpose</li>
            <li>You must not violate any laws in your jurisdiction</li>
            <li>You must not infringe on the rights of others</li>
            <li>You must not interfere with or disrupt the service</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">User Accounts</h2>
          <p className="text-muted-foreground leading-relaxed">
            You are responsible for maintaining the confidentiality of your account credentials. 
            You agree to accept responsibility for all activities that occur under your account. 
            You must immediately notify us of any unauthorized use of your account.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">User Content</h2>
          <p className="text-muted-foreground leading-relaxed mb-4">
            You retain ownership of any content you upload to {appName}. By uploading content, 
            you grant us a license to use, store, and process your content to provide and 
            improve our services. You are responsible for ensuring you have the right to upload 
            any content you submit.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Prohibited Uses</h2>
          <p className="text-muted-foreground leading-relaxed mb-4">
            You agree not to use {appName} to:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
            <li>Upload malicious software or content</li>
            <li>Violate intellectual property rights</li>
            <li>Harass, abuse, or harm other users</li>
            <li>Collect or harvest information about other users</li>
            <li>Impersonate any person or entity</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Service Availability</h2>
          <p className="text-muted-foreground leading-relaxed">
            We strive to maintain service availability, but we do not guarantee uninterrupted 
            access. We reserve the right to modify, suspend, or discontinue any part of the 
            service at any time with or without notice.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Limitation of Liability</h2>
          <p className="text-muted-foreground leading-relaxed">
            {appName} is provided "as is" without warranties of any kind. We shall not be 
            liable for any indirect, incidental, special, or consequential damages arising 
            from your use of the service.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Changes to Terms</h2>
          <p className="text-muted-foreground leading-relaxed">
            We reserve the right to modify these terms at any time. We will notify users of 
            significant changes. Continued use of the service after changes constitutes 
            acceptance of the modified terms.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-4">Contact Information</h2>
          <p className="text-muted-foreground leading-relaxed">
            If you have any questions about these Terms of Service, please contact us through 
            our support channels.
          </p>
        </section>
      </div>
    </div>
  );
}
