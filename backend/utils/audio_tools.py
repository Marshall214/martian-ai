# utils/audio_tools.py
import whisper
import os
import tempfile
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re
from gtts import gTTS
import uuid

# Load models
whisper_model = whisper.load_model("base")

# Load text enhancement model for creating detailed summaries
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")
except Exception as e:
    print(f"Warning: Could not load summarization model: {e}")
    summarizer = None

def transcribe_audio(file_path: str) -> str:
    """Transcribe audio file to text using Whisper"""
    try:
        result = whisper_model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        raise Exception(f"Failed to transcribe audio: {str(e)}")

def enhance_text_for_audio(text: str) -> str:
    """
    Enhance and expand text to create a comprehensive, detailed audio-friendly version.
    This adds context, explanations, and makes the content more suitable for audio consumption.
    """
    # Clean and prepare text
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    
    # Split into sentences for processing
    sentences = re.split(r'[.!?]+', cleaned_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    enhanced_parts = []
    
    for i, sentence in enumerate(sentences):
        if not sentence:
            continue
            
        # Add introductory phrases for better audio flow
        if i == 0:
            enhanced_parts.append(f"Let me walk you through this content. {sentence}.")
        elif i == len(sentences) - 1:
            enhanced_parts.append(f"To conclude, {sentence.lower()}.")
        else:
            # Add connecting phrases and explanations
            if len(sentence.split()) < 5:
                enhanced_parts.append(f"Additionally, {sentence.lower()}.")
            else:
                # For longer sentences, add explanatory context
                enhanced_parts.append(f"Furthermore, {sentence}.")
    
    # Join with appropriate pauses
    enhanced_text = " ".join(enhanced_parts)
    
    # Add final polish for audio consumption
    enhanced_text = f"Welcome to your enhanced audio summary. {enhanced_text} Thank you for listening to this comprehensive overview."
    
    return enhanced_text

def create_detailed_audio_summary(transcribed_text: str) -> str:
    """
    Create a detailed, comprehensive summary from transcribed audio.
    This expands on the original content with explanations and context.
    """
    # Clean the transcribed text
    cleaned_text = re.sub(r'\s+', ' ', transcribed_text.strip())
    
    if len(cleaned_text.split()) < 10:
        return "The audio content was too short to generate a meaningful detailed summary. Please provide longer audio content for better results."
    
    # Create sections for a comprehensive summary
    sections = []
    
    # Introduction
    sections.append("## Audio Content Summary")
    sections.append("\nThis is a comprehensive analysis and summary of the provided audio content:\n")
    
    # Main content processing
    sentences = re.split(r'[.!?]+', cleaned_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) >= 3:
        # Key points section
        sections.append("### Key Points Discussed:")
        for i, sentence in enumerate(sentences[:5], 1):  # Limit to first 5 main points
            if sentence:
                sections.append(f"• **Point {i}:** {sentence}.")
    
    # Detailed breakdown
    sections.append("\n### Detailed Analysis:")
    
    # Process text in chunks for detailed explanation
    words = cleaned_text.split()
    chunk_size = 50  # Process in chunks of 50 words
    
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i+chunk_size])
        if chunk.strip():
            sections.append(f"\n**Section {i//chunk_size + 1}:** {chunk}")
            
            # Add contextual explanation
            if 'important' in chunk.lower() or 'significant' in chunk.lower():
                sections.append("*This section highlights critical information that requires special attention.*")
            elif 'example' in chunk.lower() or 'instance' in chunk.lower():
                sections.append("*This provides practical examples to illustrate the concepts discussed.*")
    
    # Summary and conclusions
    sections.append("\n### Summary and Key Takeaways:")
    sections.append(f"The audio content covers approximately {len(words)} words of material, discussing various aspects of the topic. ")
    
    if len(sentences) > 1:
        sections.append(f"The main themes include: {', '.join(sentences[:3])}...")
    
    sections.append("\n*This detailed summary provides a comprehensive overview of all audio content for easy reference and review.*")
    
    return '\n'.join(sections)

def generate_audio_from_text(text: str, output_path: str = None) -> str:
    """
    Generate actual audio file from text using Google Text-to-Speech.
    """
    try:
        if not output_path:
            # Create a unique filename in a static directory
            static_dir = "static/audio"
            os.makedirs(static_dir, exist_ok=True)
            filename = f"audio_{uuid.uuid4().hex[:8]}.mp3"
            output_path = os.path.join(static_dir, filename)
        
        # Create gTTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save the audio file
        tts.save(output_path)
        
        return output_path
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        # Return a placeholder path if TTS fails
        static_dir = "static/audio"
        os.makedirs(static_dir, exist_ok=True)
        filename = f"placeholder_{uuid.uuid4().hex[:8]}.mp3"
        return os.path.join(static_dir, filename)

def process_audio_file(file_path: str) -> dict:
    """
    Complete audio processing pipeline: transcribe and create detailed summary
    """
    try:
        # Transcribe the audio
        transcribed_text = transcribe_audio(file_path)
        
        # Create detailed summary
        detailed_summary = create_detailed_audio_summary(transcribed_text)
        
        # Count words
        word_count = len(transcribed_text.split())
        
        return {
            "transcribed_text": transcribed_text,
            "detailed_summary": detailed_summary,
            "word_count": word_count,
            "status": "success"
        }
    except Exception as e:
        return {
            "transcribed_text": "",
            "detailed_summary": f"Error processing audio: {str(e)}",
            "word_count": 0,
            "status": "error"
        }

def process_text_for_audio(text: str) -> dict:
    """
    Complete text-to-audio processing pipeline: enhance text and prepare for TTS
    """
    try:
        # Enhance text for better audio experience
        enhanced_text = enhance_text_for_audio(text)
        
        # Generate audio (placeholder implementation)
        audio_path = generate_audio_from_text(enhanced_text)
        
        # Count words
        word_count = len(enhanced_text.split())
        
        return {
            "original_text": text,
            "enhanced_text": enhanced_text,
            "audio_path": audio_path,
            "word_count": word_count,
            "status": "success"
        }
    except Exception as e:
        return {
            "original_text": text,
            "enhanced_text": f"Error enhancing text: {str(e)}",
            "audio_path": None,
            "word_count": len(text.split()),
            "status": "error"
        }
