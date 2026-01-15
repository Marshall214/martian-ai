"use client"

import type React from "react"

import { DashboardLayout } from "@/components/dashboard-layout"
import { GlassCard } from "@/components/glass-card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useState, useEffect } from "react"
import { Mic, FileText, Volume2, Upload, Copy, Download, Loader2, Play, Pause, Check } from "lucide-react"
import { motion } from "framer-motion"
import { useToast } from "@/hooks/use-toast"

export default function SmartNotesPage() {
  const [textNotes, setTextNotes] = useState("")
  const [audioFile, setAudioFile] = useState<File | null>(null)
  const [textSummary, setTextSummary] = useState("")
  const [audioSummary, setAudioSummary] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [textWordCount, setTextWordCount] = useState(0)
  const [summaryWordCount, setSummaryWordCount] = useState(0)
  const [isValidLength, setIsValidLength] = useState(true)
  const [copyIconState, setCopyIconState] = useState<'copy' | 'check'>('copy')
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null)
  const { toast } = useToast()

  // Update word count when text changes
  useEffect(() => {
    const words = textNotes.trim().split(/\s+/).filter(word => word.length > 0)
    const count = textNotes.trim() === "" ? 0 : words.length
    setTextWordCount(count)
    setIsValidLength(count <= 3000 && count >= 30)
  }, [textNotes])

  // Update summary word count when summary changes
  useEffect(() => {
    const words = textSummary.trim().split(/\s+/).filter(word => word.length > 0)
    const count = textSummary.trim() === "" ? 0 : words.length
    setSummaryWordCount(count)
  }, [textSummary])

  const getWordCountColor = (count: number) => {
    if (count < 30) return "text-red-500"
    if (count > 3000) return "text-red-500"
    if (count > 2500) return "text-orange-500"
    return "text-green-600"
  }

  const handleAudioUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setAudioFile(file)
    toast({
      title: "Audio uploaded",
      description: `${file.name} has been loaded`,
    })
  }

  const handleGenerateTextSummary = async () => {
    if (!audioFile) {
      toast({
        title: "Error",
        description: "Please upload an audio file",
        variant: "destructive",
      })
      return
    }

    setIsProcessing(true)
    setTextSummary("")

    try {
      const formData = new FormData()
      formData.append('audio', audioFile)

      const response = await fetch("http://localhost:8000/audio-to-text", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to process audio file")
      }

      setTextSummary(data.detailed_summary)
      toast({
        title: "Success",
        description: `Audio transcribed: ${data.word_count} words processed`,
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

  const handleGenerateAudioSummary = async () => {
    if (!textNotes.trim()) {
      toast({
        title: "Error",
        description: "Please enter some text notes",
        variant: "destructive",
      })
      return
    }

    if (!isValidLength) {
      toast({
        title: "Error",
        description: textWordCount < 30 ? "Text must be at least 30 words" : "Text must be under 3000 words",
        variant: "destructive",
      })
      return
    }

    setIsProcessing(true)
    setAudioSummary("")
    setAudioUrl(null)

    try {
      const response = await fetch("http://localhost:8000/text-to-audio", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: textNotes,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate audio summary")
      }

      setAudioSummary(data.enhanced_text)
      if (data.audio_url) {
        const fullAudioUrl = `http://localhost:8000${data.audio_url}`
        setAudioUrl(fullAudioUrl)
        
        // Create new audio element
        const audio = new Audio(fullAudioUrl)
        audio.addEventListener('ended', () => setIsPlaying(false))
        setAudioElement(audio)
      }
      toast({
        title: "Success",
        description: `Audio enhanced: ${data.duration_estimate} estimated`,
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
    setCopyIconState('check')
    toast({
      title: "Copied",
      description: "Text copied to clipboard",
    })
    
    setTimeout(() => {
      setCopyIconState('copy')
    }, 2000)
  }

  const downloadText = (text: string, filename: string = "notes") => {
    const blob = new Blob([text], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${filename}.txt`
    a.click()
    URL.revokeObjectURL(url)

    toast({
      title: "Downloaded",
      description: "Text has been downloaded",
    })
  }

  const downloadAudio = () => {
    if (!audioUrl) {
      toast({
        title: "Error",
        description: "No audio available to download",
        variant: "destructive",
      })
      return
    }
    
    // Create download link for the actual audio file
    const link = document.createElement('a')
    link.href = audioUrl
    link.download = 'enhanced-audio-summary.mp3'
    link.click()
    
    toast({
      title: "Downloaded",
      description: "Audio file has been downloaded",
    })
  }

  const toggleAudioPlayback = () => {
    if (!audioElement) {
      toast({
        title: "Error",
        description: "No audio available to play",
        variant: "destructive",
      })
      return
    }
    
    if (isPlaying) {
      audioElement.pause()
      setIsPlaying(false)
      toast({
        title: "Paused",
        description: "Audio playback paused",
      })
    } else {
      audioElement.play().catch((error) => {
        console.error("Audio playback failed:", error)
        toast({
          title: "Error",
          description: "Failed to play audio. Please check your connection.",
          variant: "destructive",
        })
      })
      setIsPlaying(true)
      toast({
        title: "Playing",
        description: "Audio playback started",
      })
    }
  }

  return (
    <DashboardLayout>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Mic className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold text-foreground">Smart Notes</h1>
          </div>
          <p className="text-muted-foreground text-lg">Convert between text and audio with AI-enhanced summaries</p>
        </div>

        <Tabs defaultValue="audio-to-text" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 bg-secondary/50 border border-border">
            <TabsTrigger value="audio-to-text" className="text-foreground data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Mic className="mr-2 h-4 w-4" />
              Audio to Text
            </TabsTrigger>
            <TabsTrigger value="text-to-audio" className="text-foreground data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              <Volume2 className="mr-2 h-4 w-4" />
              Text to Audio
            </TabsTrigger>
          </TabsList>

          <TabsContent value="audio-to-text">
            <div className="grid lg:grid-cols-2 gap-6 items-start">
              <GlassCard>
                <h2 className="text-xl font-semibold text-foreground mb-4">Audio Input</h2>
                <div className="mb-4">
                  <Label htmlFor="audio-upload" className="text-foreground mb-2 block">
                    Upload Audio File (MP3, WAV, M4A)
                  </Label>
                  <div className="relative">
                    <input
                      id="audio-upload"
                      type="file"
                      accept=".mp3,.wav,.m4a,.ogg"
                      onChange={handleAudioUpload}
                      className="hidden"
                    />
                    <Button
                      onClick={() => document.getElementById("audio-upload")?.click()}
                      variant="outline"
                      className="w-full border-border text-foreground hover:bg-secondary bg-transparent"
                    >
                      <Upload className="mr-2 h-4 w-4" />
                      {audioFile?.name || "Choose Audio File"}
                    </Button>
                  </div>
                </div>
                <Button
                  onClick={handleGenerateTextSummary}
                  disabled={!audioFile || isProcessing}
                  className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Processing Audio...
                    </>
                  ) : (
                    <>
                      <FileText className="mr-2 h-4 w-4" />
                      Generate Detailed Summary
                    </>
                  )}
                </Button>
              </GlassCard>

              <GlassCard>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-foreground">Text Summary</h2>
                  <div className="flex items-center gap-2">
                    {textSummary && (
                      <>
                        <span className="text-sm text-muted-foreground">
                          {summaryWordCount} words
                        </span>
                        <Button
                          onClick={() => copyToClipboard(textSummary)}
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
                          onClick={() => downloadText(textSummary, "audio-transcript")}
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

                <div className="h-[400px] p-4 bg-secondary/50 border border-border rounded-md overflow-y-auto">
                  {textSummary ? (
                    <div className="text-foreground whitespace-pre-wrap text-sm leading-relaxed">
                      {textSummary}
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-full text-muted-foreground">
                      <FileText className="h-12 w-12 mb-4 opacity-50" />
                      <p className="text-center">
                        {isProcessing
                          ? "Transcribing and analyzing your audio..."
                          : "Upload an audio file to generate a detailed summary"}
                      </p>
                    </div>
                  )}
                </div>
              </GlassCard>
            </div>
          </TabsContent>

          <TabsContent value="text-to-audio">
            <div className="grid lg:grid-cols-2 gap-6 items-start">
              <GlassCard>
                <h2 className="text-xl font-semibold text-foreground mb-4">Text Input</h2>
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <Label htmlFor="text-notes" className="text-foreground">
                      Enter Your Text
                    </Label>
                    <span className={`text-sm font-medium ${getWordCountColor(textWordCount)}`}>
                      {textWordCount}/3000 words
                    </span>
                  </div>
                  <Textarea
                    id="text-notes"
                    placeholder="Enter your text here to convert to enhanced audio summary..."
                    value={textNotes}
                    onChange={(e) => setTextNotes(e.target.value)}
                    className="h-[300px] bg-secondary/50 border-border text-foreground placeholder:text-muted-foreground resize-none overflow-y-auto"
                  />
                </div>
                <Button
                  onClick={handleGenerateAudioSummary}
                  disabled={isProcessing || !isValidLength || !textNotes.trim()}
                  className="w-full bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating Audio...
                    </>
                  ) : (
                    <>
                      <Volume2 className="mr-2 h-4 w-4" />
                      Generate Enhanced Audio
                    </>
                  )}
                </Button>
              </GlassCard>

              <GlassCard>
                <h2 className="text-xl font-semibold text-foreground mb-4">Audio Summary</h2>

                {audioSummary ? (
                  <div className="space-y-4">
                    <div className="h-[200px] p-4 bg-secondary/50 border border-border rounded-md overflow-y-auto">
                      <div className="text-foreground whitespace-pre-wrap text-sm leading-relaxed">
                        {audioSummary}
                      </div>
                    </div>

                    <div className="p-6 bg-secondary/50 border border-border rounded-lg">
                      <div className="flex items-center justify-center gap-4 mb-4">
                        <Button
                          size="icon"
                          onClick={toggleAudioPlayback}
                          className="h-16 w-16 rounded-full bg-primary text-primary-foreground hover:bg-primary/90"
                        >
                          {isPlaying ? <Pause className="h-8 w-8" /> : <Play className="h-8 w-8 ml-1" />}
                        </Button>
                      </div>

                      <div className="w-full bg-secondary rounded-full h-2 mb-2">
                        <div className="bg-primary h-2 rounded-full w-1/3 transition-all duration-300" />
                      </div>

                      <div className="flex justify-between text-sm text-muted-foreground">
                        <span>0:00</span>
                        <span>Demo Mode</span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <Button
                        onClick={() => copyToClipboard(audioSummary)}
                        variant="outline"
                        className="border-border text-foreground hover:bg-secondary bg-transparent"
                      >
                        <Copy className="mr-2 h-4 w-4" />
                        Copy Text
                      </Button>
                      <Button
                        onClick={downloadAudio}
                        variant="outline"
                        className="border-border text-foreground hover:bg-secondary bg-transparent"
                      >
                        <Download className="mr-2 h-4 w-4" />
                        Download Audio
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="h-[400px] flex flex-col items-center justify-center border border-dashed border-border rounded-lg">
                    <Volume2 className="h-12 w-12 text-muted-foreground mb-4 opacity-50" />
                    <p className="text-center text-muted-foreground">
                      {isProcessing
                        ? "Creating enhanced audio summary..."
                        : "Enter text to generate an enhanced audio summary"}
                    </p>
                  </div>
                )}
              </GlassCard>
            </div>
          </TabsContent>
        </Tabs>
      </motion.div>
    </DashboardLayout>
  )
}
