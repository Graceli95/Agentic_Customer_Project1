import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Customer Service AI",
    template: "%s | Customer Service AI",
  },
  description:
    "Advanced Multi-Agent AI System for Intelligent Customer Support. Powered by LangChain v1.0+ and LangGraph, handling technical support, billing inquiries, and compliance questions.",
  keywords: [
    "AI",
    "Customer Service",
    "LangChain",
    "LangGraph",
    "Multi-Agent",
    "Technical Support",
    "Billing Support",
    "Compliance",
  ],
  authors: [{ name: "ASU VibeCoding Team" }],
  creator: "ASU VibeCoding Team",
  applicationName: "Customer Service AI",
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    title: "Customer Service AI",
    description:
      "Advanced Multi-Agent AI System for Intelligent Customer Support",
    siteName: "Customer Service AI",
  },
  twitter: {
    card: "summary_large_image",
    title: "Customer Service AI",
    description:
      "Advanced Multi-Agent AI System for Intelligent Customer Support",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#000000" },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
