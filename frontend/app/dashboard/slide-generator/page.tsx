"use client"

import type React from "react"

import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard } from "@/components/glass-card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"
import { Presentation, Upload, Download, Loader2, FileText, Eye } from "lucide-react"
import { motion } from "framer-motion"
import { useToast } from "@/hooks/use-toast"
import { Progress } from "@/components/ui/progress"

type OutputFormat = "pptx" | "pdf"

export default function SlideGeneratorPage() {
  const [inputText, setInputText] = useState("")
  const [outputFormat, setOutputFormat] = useState<OutputFormat>("pptx")
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [generatedFile, setGeneratedFile] = useState<string | null>(null)
  const [fileName, setFileName] = useState("")
  const { toast } = useToast()

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (event) => {
      const text = event.target?.result as string
      setInputText(text)
      setFileName(file.name)
      toast({
        title: "File uploaded",
        description: `${file.name} has been loaded`,
      })
    }
    reader.readAsText(file)
  }

  const handleGenerateSlides = async () => {
    if (!inputText.trim()) {
      toast({
        title: "Error",
        description: "Please enter text or upload a file",
        variant: "destructive",
      })
      return
    }

    setIsGenerating(true)
    setProgress(0)

    // Mock progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 10
      })
    }, 300)

    // Mock API call
    await new Promise((resolve) => setTimeout(resolve, 3500))

    setGeneratedFile(`mock-presentation.${outputFormat}`)
    setIsGenerating(false)

    toast({
      title: "Success",
      description: `Presentation has been generated as ${outputFormat.toUpperCase()}`,
    })
  }

  const handleDownload = () => {
    toast({
      title: "Downloaded",
      description: "Presentation has been downloaded",
    })
  }

  return (
    <DashboardLayout>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Presentation className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold text-foreground">Slide Generator</h1>
          </div>
          <p className="text-muted-foreground text-lg">Transform your notes into professional presentations</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <GlassCard>
            <h2 className="text-xl font-semibold text-foreground mb-4">Input Content</h2>

            {/* File Upload */}
            <div className="mb-4">
              <Label htmlFor="file-upload" className="text-foreground mb-2 block">
                Upload Notes (TXT, DOCX)
              </Label>
              <div className="relative">
                <input
                  id="file-upload"
                  type="file"
                  accept=".txt,.docx"
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

            {/* Text Input */}
            <Textarea
              placeholder="Paste your lecture notes or thesis content here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="min-h-[250px] bg-secondary/50 border-border text-foreground placeholder:text-muted-foreground resize-none mb-4"
            />

            {/* Output Format Selection */}
            <div className="mb-4">
              <Label htmlFor="output-format" className="text-foreground mb-2 block">
                Output Format
              </Label>
              <Select value={outputFormat} onValueChange={(value) => setOutputFormat(value as OutputFormat)}>
                <SelectTrigger className="bg-secondary/50 border-border text-foreground">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-popover border-border">
                  <SelectItem value="pptx" className="text-foreground hover:bg-secondary">
                    PowerPoint (.pptx)
                  </SelectItem>
                  <SelectItem value="pdf" className="text-foreground hover:bg-secondary">
                    PDF Slides (.pdf)
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button
              onClick={handleGenerateSlides}
              disabled={isGenerating}
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Presentation className="mr-2 h-4 w-4" />
                  Generate Slides
                </>
              )}
            </Button>
          </GlassCard>

          {/* Output Section */}
          <GlassCard>
            <h2 className="text-xl font-semibold text-foreground mb-4">Generated Presentation</h2>

            {isGenerating ? (
              <div className="min-h-[400px] flex flex-col items-center justify-center">
                <Loader2 className="h-12 w-12 text-primary animate-spin mb-4" />
                <p className="text-foreground font-medium mb-2">Generating your presentation...</p>
                <Progress value={progress} className="w-full max-w-xs" />
                <p className="text-sm text-muted-foreground mt-2">{progress}% complete</p>
              </div>
            ) : generatedFile ? (
              <div className="space-y-4">
                <div className="p-6 bg-secondary/50 border border-border rounded-lg">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="h-16 w-16 bg-primary/20 rounded-lg flex items-center justify-center">
                      <FileText className="h-8 w-8 text-primary" />
                    </div>
                    <div className="flex-1">
                      <p className="text-foreground font-medium">{generatedFile}</p>
                      <p className="text-sm text-muted-foreground">Ready to download</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Button
                      onClick={handleDownload}
                      className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
                    >
                      <Download className="mr-2 h-4 w-4" />
                      Download Presentation
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full border-border text-foreground hover:bg-secondary bg-transparent"
                    >
                      <Eye className="mr-2 h-4 w-4" />
                      Preview Slides
                    </Button>
                  </div>
                </div>

                <div className="p-4 bg-secondary/50 border border-border rounded-lg">
                  <h3 className="text-foreground font-medium mb-2">Presentation Details</h3>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Slides:</span>
                      <span className="text-foreground">12</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Format:</span>
                      <span className="text-foreground">{outputFormat.toUpperCase()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Size:</span>
                      <span className="text-foreground">2.4 MB</span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="min-h-[400px] flex items-center justify-center border border-dashed border-border rounded-lg">
                <div className="text-center">
                  <Presentation className="h-12 w-12 text-muted-foreground mx-auto mb-2" />
                  <p className="text-muted-foreground">Your presentation will appear here</p>
                </div>
              </div>
            )}
          </GlassCard>
        </div>
      </motion.div>
    </DashboardLayout>
  )
}
