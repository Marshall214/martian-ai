"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard } from "@/components/glass-card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { useState, useMemo } from "react"
import { Sparkles, Copy, Download, Loader2, FileText, Target, TrendingUp } from "lucide-react"
import { motion } from "framer-motion"
import { useToast } from "@/hooks/use-toast"

interface ProofreadResult {
  original_text: string
  humanized_text: string
  original_word_count: number
  humanized_word_count: number
  ai_score_before_humanizing: number
  ai_score_after_humanizing: number
  improvement_percentage: number
  word_limit: { min: number; max: number }
}

export default function ProofAIPage() {
  const [inputText, setInputText] = useState("")
  const [result, setResult] = useState<ProofreadResult | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const { toast } = useToast()

  // Count words in real-time
  const wordCount = useMemo(() => {
    return inputText.trim() ? inputText.trim().split(/\s+/).length : 0
  }, [inputText])

  const isWithinWordLimit = wordCount >= 50 && wordCount <= 1500
  const wordLimitColor = wordCount < 50 ? "text-red-500" : wordCount > 1500 ? "text-red-500" : "text-green-500"

  const handleProofread = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Error",
        description: "Please enter some text to proofread",
        variant: "destructive",
      })
      return
    }

    if (!isWithinWordLimit) {
      toast({
        title: "Error",
        description: `Text must be between 50-1500 words. Current: ${wordCount} words`,
        variant: "destructive",
      })
      return
    }

    setIsProcessing(true)
    setResult(null)

    try {
      const response = await fetch("http://localhost:8000/proofread", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to proofread text")
      }

      setResult(data)
      toast({
        title: "Success",
        description: `Text processed! AI score improved by ${data.improvement_percentage}%`,
      })
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "An unexpected error occurred",
        variant: "destructive",
      })
    } finally {
      setIsProcessing(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({
      title: "Copied",
      description: "Text copied to clipboard",
    })
  }

  const downloadText = (text: string) => {
    const blob = new Blob([text], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "proofread-text.txt"
    a.click()
    URL.revokeObjectURL(url)
    toast({
      title: "Downloaded",
      description: "Text file has been downloaded",
    })
  }

  return (
    <DashboardLayout>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Sparkles className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold text-foreground">Proof AI</h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Humanize and proofread your writing with advanced AI detection scoring
          </p>
          <div className="flex items-center gap-4 mt-4">
            <Badge variant="outline" className="text-sm">
              📝 Word Limit: 50 - 1,500 words
            </Badge>
            <Badge variant="outline" className="text-sm">
              🎯 AI Detection & Humanization
            </Badge>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <GlassCard>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-foreground">Original Text</h2>
              <div className="flex items-center gap-2">
                <FileText className="h-4 w-4 text-muted-foreground" />
                <span className={`text-sm font-medium ${wordLimitColor}`}>
                  {wordCount} / 1,500 words
                </span>
              </div>
            </div>
            
            <div className="relative">
              <Textarea
                placeholder="Paste or type your text here... (50-1500 words)"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="h-80 bg-secondary/50 border-border text-foreground placeholder:text-muted-foreground resize-none overflow-y-auto"
              />
              {!isWithinWordLimit && wordCount > 0 && (
                <div className="absolute -bottom-6 left-0 text-xs text-red-500">
                  {wordCount < 50 
                    ? `Need ${50 - wordCount} more words` 
                    : `Exceeds limit by ${wordCount - 1500} words`}
                </div>
              )}
            </div>

            <div className="flex gap-3 mt-8">
              <Button
                onClick={handleProofread}
                disabled={isProcessing || !isWithinWordLimit}
                className="flex-1 bg-primary text-primary-foreground hover:bg-primary/90"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Proofread & Humanize
                  </>
                )}
              </Button>
            </div>
          </GlassCard>

          {/* Output Section */}
          <GlassCard>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-foreground">Proofread Text</h2>
              {result && (
                <div className="flex gap-2">
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => copyToClipboard(result.humanized_text)}
                    className="text-foreground hover:bg-secondary"
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => downloadText(result.humanized_text)}
                    className="text-foreground hover:bg-secondary"
                  >
                    <Download className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>

            {result ? (
              <div className="h-80 p-4 bg-secondary/50 border border-border rounded-lg text-foreground overflow-y-auto">
                {result.humanized_text}
              </div>
            ) : (
              <div className="h-80 flex items-center justify-center border border-dashed border-border rounded-lg">
                <p className="text-muted-foreground">Proofread text will appear here</p>
              </div>
            )}

            {/* AI Detection Results */}
            {result && (
              <div className="mt-6 space-y-6">
                {/* Before Score */}
                <div className="p-4 bg-secondary/30 border border-border rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-primary" />
                      <span className="font-medium text-foreground">AI Score (Before)</span>
                    </div>
                    <span className={`text-2xl font-bold ${
                      result.ai_score_before_humanizing < 30 ? "text-green-500" : 
                      result.ai_score_before_humanizing < 60 ? "text-yellow-500" : "text-red-500"
                    }`}>
                      {result.ai_score_before_humanizing}%
                    </span>
                  </div>
                  <Progress 
                    value={result.ai_score_before_humanizing} 
                    className="h-2"
                  />
                  <p className="text-sm text-muted-foreground mt-2">
                    Original text AI detection score
                  </p>
                </div>

                {/* After Score */}
                <div className="p-4 bg-secondary/30 border border-border rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-primary" />
                      <span className="font-medium text-foreground">AI Score (After)</span>
                    </div>
                    <span className={`text-2xl font-bold ${
                      result.ai_score_after_humanizing < 30 ? "text-green-500" : 
                      result.ai_score_after_humanizing < 60 ? "text-yellow-500" : "text-red-500"
                    }`}>
                      {result.ai_score_after_humanizing}%
                    </span>
                  </div>
                  <Progress 
                    value={result.ai_score_after_humanizing} 
                    className="h-2"
                  />
                  <p className="text-sm text-muted-foreground mt-2">
                    Humanized text AI detection score
                  </p>
                </div>

                {/* Improvement */}
                <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-primary" />
                      <span className="font-medium text-foreground">Improvement</span>
                    </div>
                    <span className="text-2xl font-bold text-primary">
                      {result.improvement_percentage}%
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-2">
                    AI detection score reduced by {result.improvement_percentage} points
                  </p>
                </div>

                {/* Word Count Info */}
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Original: {result.original_word_count} words</span>
                  <span>Humanized: {result.humanized_word_count} words</span>
                </div>
              </div>
            )}
          </GlassCard>
        </div>
      </motion.div>
    </DashboardLayout>
  )
}
