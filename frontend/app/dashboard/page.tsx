"use client"

import type React from "react"
import { useEffect } from "react"

import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard } from "@/components/glass-card"
import { Sparkles, FileText, Mic, Presentation, TrendingUp, Clock } from "lucide-react"
import Link from "next/link"
import { useAuth } from "@/lib/auth-context"
import { motion } from "framer-motion"
import { useRouter } from "next/navigation"

export default function DashboardPage() {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login")
    }
  }, [user, isLoading, router])

  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading authentication...</p>
      </div>
    ) // Or a loading spinner
  }

  return (
    <DashboardLayout>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Welcome back, {user?.full_name || user?.email}!</h1>
          <p className="text-muted-foreground text-lg">Ready to supercharge your academic work with AI?</p>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <QuickActionCard
            href="/dashboard/proof-ai"
            icon={<Sparkles className="h-6 w-6 text-primary" />}
            title="Proof AI"
            description="Humanize & proofread"
          />
          <QuickActionCard
            href="/dashboard/summarizer"
            icon={<FileText className="h-6 w-6 text-primary" />}
            title="Summarizer"
            description="Generate summaries"
          />
          <QuickActionCard
            href="/dashboard/smart-notes"
            icon={<Mic className="h-6 w-6 text-primary" />}
            title="Smart Notes"
            description="Audio & text notes"
          />
          <QuickActionCard
            href="/dashboard/slide-generator"
            icon={<Presentation className="h-6 w-6 text-primary" />}
            title="Slide Generator"
            description="Create presentations"
          />
        </div>

        {/* Stats & Recent Activity */}
        <div className="grid md:grid-cols-2 gap-6">
          <GlassCard>
            <div className="flex items-center gap-3 mb-4">
              <TrendingUp className="h-6 w-6 text-primary" />
              <h2 className="text-xl font-semibold text-foreground">Usage Stats</h2>
            </div>
            <div className="space-y-4">
              <StatItem label="Documents Processed" value="0" />
              <StatItem label="AI Generations" value="0" />
              <StatItem label="Time Saved" value="0 hours" />
            </div>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-3 mb-4">
              <Clock className="h-6 w-6 text-primary" />
              <h2 className="text-xl font-semibold text-foreground">Recent Activity</h2>
            </div>
            <div className="text-center py-8">
              <p className="text-muted-foreground">No recent activity yet</p>
              <p className="text-sm text-muted-foreground mt-2">Start using our AI tools to see your activity here</p>
            </div>
          </GlassCard>
        </div>
      </motion.div>
    </DashboardLayout>
  )
}

function QuickActionCard({
  href,
  icon,
  title,
  description,
}: { href: string; icon: React.ReactNode; title: string; description: string }) {
  return (
    <Link href={href}>
      <GlassCard className="hover:border-primary/50 transition-all duration-300 cursor-pointer h-full">
        <div className="mb-3">{icon}</div>
        <h3 className="text-lg font-semibold text-foreground mb-1">{title}</h3>
        <p className="text-sm text-muted-foreground">{description}</p>
      </GlassCard>
    </Link>
  )
}

function StatItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-muted-foreground">{label}</span>
      <span className="text-foreground font-semibold">{value}</span>
    </div>
  )
}
