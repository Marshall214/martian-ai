"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard } from "@/components/glass-card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState, useEffect } from "react"
import { FileText, Upload, Copy, Download, Loader2, Check } from "lucide-react"
import { motion } from "framer-motion"
import { useToast } from "@/hooks/use-toast"

type SummaryType = "key-points" | "detailed" | "short"

export default function SummarizerPage() {
  const [inputText, setInputText] = useState("")
  const [summaryType, setSummaryType] = useState<SummaryType>("key-points")
  const [summary, setSummary] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [fileName, setFileName] = useState("")
  const [inputWordCount, setInputWordCount] = useState(0)
  const [summaryWordCount, setSummaryWordCount] = useState(0)
  const [isValidLength, setIsValidLength] = useState(true)
  const [copyIconState, setCopyIconState] = useState<'copy' | 'check'>('copy')
  const { toast } = useToast()

  // Update word count when input text changes
  useEffect(() => {
    const words = inputText.trim().split(/\s+/).filter(word => word.length > 0)
    const count = inputText.trim() === "" ? 0 : words.length
    setInputWordCount(count)
    setIsValidLength(count <= 5000 && count >= 50)
  }, [inputText])

  // Update summary word count when summary changes
  useEffect(() => {
    const words = summary.trim().split(/\s+/).filter(word => word.length > 0)
    const count = summary.trim() === "" ? 0 : words.length
    setSummaryWordCount(count)
  }, [summary])

  const getWordCountColor = (count: number) => {
    if (count < 50) return "text-red-500"
    if (count > 5000) return "text-red-500"
    if (count > 4500) return "text-orange-500"
    return "text-green-600"
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch("http://localhost:8000/upload-document", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to upload document")
      }

      setInputText(data.text)
      setFileName(file.name)
      toast({
        title: "File uploaded",
        description: `${file.name} has been processed (${data.word_count} words)`,
      })

      if (!data.is_valid) {
        toast({
          title: "Warning",
          description: data.status_message,
          variant: "destructive",
        })
      }

    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "Failed to upload document",
        variant: "destructive",
      })
    }
  }

  const handleGenerateSummary = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Error",
        description: "Please enter text or upload a file",
        variant: "destructive",
      })
      return
    }

    if (!isValidLength) {
      toast({
        title: "Error",
        description: inputWordCount < 50 ? "Text must be at least 50 words" : "Text must be under 5000 words",
        variant: "destructive",
      })
      return
    }

    setIsProcessing(true)
    setSummary("") // Clear previous summary

    try {
      const response = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: inputText,
          mode: summaryType === "key-points" ? "keypoints" : summaryType,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate summary")
      }

      setSummary(data.summary_text)
      toast({
        title: "Success",
        description: "Summary has been generated",
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

  const copyToClipboard = () => {
    navigator.clipboard.writeText(summary)
    setCopyIconState('check')
    toast({
      title: "Copied",
      description: "Summary copied to clipboard",
    })
    
    // Reset icon after 2 seconds
    setTimeout(() => {
      setCopyIconState('copy')
    }, 2000)
  }

  const downloadSummary = () => {
    const blob = new Blob([summary], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "summary.txt"
    a.click()
    URL.revokeObjectURL(url)

    toast({
      title: "Downloaded",
      description: "Summary has been downloaded",
    })
  }

  return (
    <DashboardLayout>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold text-foreground">Summarizer</h1>
          </div>
          <p className="text-muted-foreground text-lg">Generate concise summaries from documents and text</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 items-start">
          {/* Input Section */}
          <GlassCard>
            <h2 className="text-xl font-semibold text-foreground mb-4">Input</h2>

            {/* File Upload */}
            <div className="mb-4">
              <Label htmlFor="file-upload" className="text-foreground mb-2 block">
                Upload File (PDF, TXT, DOCX)
              </Label>
              <div className="relative">
                <input
                  id="file-upload"
                  type="file"
                  accept=".pdf,.txt,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <Button
                  onClick={() => document.getElementById("file-upload")?.click()}
                  variant="outline"
                  className="w-full border-border text-foreground hover:bg-secondary bg-transparent"
                >
                  <Upload className="mr-2 h-4 w-4" />
                  {fileName || "Choose File"}
                </Button>
              </div>
            </div>

            <div className="relative mb-4">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-border" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Or paste text</span>
              </div>
            </div>

            {/* Text Input with Fixed Height and Scroller */}
            <div className="mb-4">
              <div className="flex justify-between items-center mb-2">
                <Label htmlFor="input-text" className="text-foreground">
                  Input Text
                </Label>
                <span className={`text-sm font-medium ${getWordCountColor(inputWordCount)}`}>
                  {inputWordCount}/5000 words
                </span>
              </div>
              <Textarea
                id="input-text"
                placeholder="Paste your text here..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="h-[300px] bg-secondary/50 border-border text-foreground placeholder:text-muted-foreground resize-none overflow-y-auto"
              />
            </div>

            {/* Summary Type Selection */}
            <div className="mb-4">
              <Label htmlFor="summary-type" className="text-foreground mb-2 block">
                Summary Type
              </Label>
              <Select value={summaryType} onValueChange={(value) => setSummaryType(value as SummaryType)}>
                <SelectTrigger className="bg-secondary/50 border-border text-foreground">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="key-points" className="text-foreground hover:bg-secondary">
                    Key Points
                  </SelectItem>
                  <SelectItem value="detailed" className="text-foreground hover:bg-secondary">
                    Detailed Summary
                  </SelectItem>
                  <SelectItem value="short" className="text-foreground hover:bg-secondary">
                    Short Paragraph
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Generate Button */}
            <Button
              onClick={handleGenerateSummary}
              disabled={isProcessing || !isValidLength || !inputText.trim()}
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating Summary...
                </>
              ) : (
                <>
                  <FileText className="mr-2 h-4 w-4" />
                  Generate Summary
                </>
              )}
            </Button>
          </GlassCard>

          {/* Output Section */}
          <GlassCard>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-foreground">Summary</h2>
              <div className="flex items-center gap-2">
                {summary && (
                  <>
                    <span className="text-sm text-muted-foreground">
                      {summaryWordCount} words
                    </span>
                    <Button
                      onClick={copyToClipboard}
                      variant="outline"
                      size="icon"
                      className="h-8 w-8 border-border text-foreground hover:bg-secondary bg-transparent"
                    >
                      {copyIconState === 'copy' ? (
                        <Copy className="h-4 w-4" />
                      ) : (
                        <Check className="h-4 w-4 text-green-600" />
                      )}
                    </Button>
                    <Button
                      onClick={downloadSummary}
                      variant="outline"
                      size="icon"
                      className="h-8 w-8 border-border text-foreground hover:bg-secondary bg-transparent"
                    >
                      <Download className="h-4 w-4" />
                    </Button>
                  </>
                )}
              </div>
            </div>

            {/* Summary Output with Fixed Height and Scroller */}
            <div className="h-[400px] p-4 bg-secondary/50 border border-border rounded-md overflow-y-auto">
              {summary ? (
                <div className="text-foreground whitespace-pre-wrap text-sm leading-relaxed">
                  {summary}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
                  <FileText className="h-12 w-12 mb-4 opacity-50" />
                  <p className="text-center">
                    {isProcessing
                      ? "Generating your summary..."
                      : "Upload a file or paste text to generate a summary"}
                  </p>
                </div>
              )}
            </div>
          </GlassCard>
        </div>
      </motion.div>
    </DashboardLayout>
  )
}
