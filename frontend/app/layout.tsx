import type { Metadata } from "next";
import { Geist, Geist_Mono, Dancing_Script } from "next/font/google";
import "./globals.css";
import { StoreProvider } from "@/lib/store-provider";
import { Footer } from "@/components/ui/footer";
import { AppHeader } from "@/components/ui/app-header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const dancingScript = Dancing_Script({
  variable: "--font-dancing",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const appName = process.env.NEXT_PUBLIC_APP_NAME || "CommunityWise";

export const metadata: Metadata = {
  title: appName,
  description: "A community knowledge platform powered by RAG technology. Share, discover, and learn together.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${dancingScript.variable} antialiased`}
      >
        <StoreProvider>
          <div className="flex flex-col min-h-screen">
            <AppHeader />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </StoreProvider>
      </body>
    </html>
  );
}
