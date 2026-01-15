"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard } from "@/components/glass-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"
import { SettingsIcon, User, Lock, Palette, Save } from "lucide-react"
import { motion } from "framer-motion"
import { useToast } from "@/hooks/use-toast"
import { useAuth } from "@/lib/auth-context"

export default function SettingsPage() {
  const { user } = useAuth()
  const [name, setName] = useState(user?.name || "")
  const [email, setEmail] = useState(user?.email || "")
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [aiModel, setAiModel] = useState("gpt-4")
  const { toast } = useToast()

  const handleSaveProfile = () => {
    toast({
      title: "Success",
      description: "Profile updated successfully",
    })
  }

  const handleChangePassword = () => {
    if (newPassword !== confirmPassword) {
      toast({
        title: "Error",
        description: "Passwords do not match",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Success",
      description: "Password changed successfully",
    })

    setCurrentPassword("")
    setNewPassword("")
    setConfirmPassword("")
  }

  const handleSavePreferences = () => {
    toast({
      title: "Success",
      description: "Preferences saved successfully",
    })
  }

  return (
    <DashboardLayout>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <SettingsIcon className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold text-foreground">Settings</h1>
          </div>
          <p className="text-muted-foreground text-lg">Manage your account and preferences</p>
        </div>

        <div className="space-y-6 max-w-3xl">
          {/* Profile Settings */}
          <GlassCard>
            <div className="flex items-center gap-3 mb-6">
              <User className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-semibold text-foreground">Profile Details</h2>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name" className="text-foreground">
                  Full Name
                </Label>
                <Input
                  id="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="bg-secondary/50 border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email" className="text-foreground">
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-secondary/50 border-border text-foreground"
                />
              </div>

              <Button onClick={handleSaveProfile} className="bg-primary text-primary-foreground hover:bg-primary/90">
                <Save className="mr-2 h-4 w-4" />
                Save Profile
              </Button>
            </div>
          </GlassCard>

          {/* Password Settings */}
          <GlassCard>
            <div className="flex items-center gap-3 mb-6">
              <Lock className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-semibold text-foreground">Change Password</h2>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="current-password" className="text-foreground">
                  Current Password
                </Label>
                <Input
                  id="current-password"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="bg-secondary/50 border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="new-password" className="text-foreground">
                  New Password
                </Label>
                <Input
                  id="new-password"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="bg-secondary/50 border-border text-foreground"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirm-password" className="text-foreground">
                  Confirm New Password
                </Label>
                <Input
                  id="confirm-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="bg-secondary/50 border-border text-foreground"
                />
              </div>

              <Button onClick={handleChangePassword} className="bg-primary text-primary-foreground hover:bg-primary/90">
                <Lock className="mr-2 h-4 w-4" />
                Change Password
              </Button>
            </div>
          </GlassCard>

          {/* Preferences */}
          <GlassCard>
            <div className="flex items-center gap-3 mb-6">
              <Palette className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-semibold text-foreground">Preferences</h2>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="ai-model" className="text-foreground">
                  AI Model
                </Label>
                <Select value={aiModel} onValueChange={setAiModel}>
                  <SelectTrigger className="bg-secondary/50 border-border text-foreground">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-popover border-border">
                    <SelectItem value="gpt-4" className="text-foreground hover:bg-secondary">
                      GPT-4 (Recommended)
                    </SelectItem>
                    <SelectItem value="gpt-3.5" className="text-foreground hover:bg-secondary">
                      GPT-3.5 (Faster)
                    </SelectItem>
                    <SelectItem value="claude" className="text-foreground hover:bg-secondary">
                      Claude
                    </SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-sm text-muted-foreground">Choose the AI model for processing your requests</p>
              </div>

              <Button
                onClick={handleSavePreferences}
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <Save className="mr-2 h-4 w-4" />
                Save Preferences
              </Button>
            </div>
          </GlassCard>
        </div>
      </motion.div>
    </DashboardLayout>
  )
}
