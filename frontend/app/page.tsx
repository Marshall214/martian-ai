"use client"

import { Button } from "@/components/ui/button"
import { Brain, Sparkles, FileText, Mic, Presentation, Shield } from "lucide-react"
import Link from "next/link"
import { motion } from "framer-motion"
import type { ReactNode } from "react" // Import ReactNode

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background grid-pattern">
      {/* Navigation */}
      <nav className="glass-nav fixed top-0 left-0 right-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Brain className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold text-foreground">Martian AI</span>
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/signin">
              <Button variant="ghost" className="text-foreground">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-4 pt-32 pb-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto mb-20"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Sparkles className="h-4 w-4 text-primary" />
            <span className="text-sm text-primary font-medium">Your AI-Powered Academic Companion</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-6 text-balance">
            <span className="text-foreground">Transform Your</span>
            <br />
            <span className="bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              Academic Journey
            </span>
          </h1>

          <p className="text-xl text-muted-foreground mb-8 text-pretty max-w-2xl mx-auto leading-relaxed">
            Empower your research and studies with cutting-edge AI tools designed for students and researchers.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/signup">
              <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 text-lg px-8">
                Get Started Free
              </Button>
            </Link>
            <Link href="/signin">
              <Button
                size="lg"
                variant="outline"
                className="text-lg px-8 border-border text-foreground hover:bg-secondary bg-transparent"
              >
                Sign In
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto"
        >
          <FeatureCard
            icon={<Sparkles className="h-6 w-6 text-primary" />}
            title="Proof AI"
            description="Humanize and proofread your writing with advanced AI detection and correction"
          />
          <FeatureCard
            icon={<FileText className="h-6 w-6 text-primary" />}
            title="Smart Summarizer"
            description="Generate concise summaries from PDFs, documents, and text in seconds"
          />
          <FeatureCard
            icon={<Mic className="h-6 w-6 text-primary" />}
            title="Smart Notes"
            description="Convert audio lectures to text summaries or generate audio from notes"
          />
          <FeatureCard
            icon={<Presentation className="h-6 w-6 text-primary" />}
            title="Slide Generator"
            description="Transform your notes into professional PowerPoint or PDF presentations"
          />
          <FeatureCard
            icon={<Shield className="h-6 w-6 text-primary" />}
            title="Secure & Private"
            description="Your data is encrypted and never shared with third parties"
          />
          <FeatureCard
            icon={<Brain className="h-6 w-6 text-primary" />}
            title="AI-Powered"
            description="Leveraging the latest in machine learning and natural language processing"
          />
        </motion.div>
      </main>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: ReactNode; title: string; description: string }) {
  return (
    <div className="glass-card rounded-xl p-6 hover:border-primary/50 transition-all duration-300">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2 text-foreground">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">{description}</p>
    </div>
  )
}
