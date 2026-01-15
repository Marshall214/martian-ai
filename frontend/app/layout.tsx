import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import { Providers } from "./providers"
import { AuthProvider } from "@/lib/auth-context"
import "./globals.css"
import { Suspense } from "react"

export const metadata: Metadata = {
  title: "Martian AI - Your AI-Powered Academic Companion",
  description: "AI-powered academic assistant platform for students and researchers",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable} antialiased`}>
        <AuthProvider>
          <Providers>
            {children}
          </Providers>
        </AuthProvider>
        <Analytics />
      </body>
    </html>
  )
}
