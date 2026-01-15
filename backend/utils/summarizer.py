# utils/summarizer.py
from transformers import pipeline
import re

# Initialize models
summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")

def count_words(text: str) -> int:
    return len(text.split())

def split_text_into_chunks(text: str, max_chunk_size: int = 900) -> list:
    """Split text into chunks that fit model limits while preserving sentence boundaries"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_key_points(text: str) -> str:
    """Extract key points and format as bullet points"""
    try:
        chunks = split_text_into_chunks(text, 900)
        all_key_points = []
        
        for chunk in chunks:
            # Generate summary focusing on key points
            summary = summarizer_model(
                chunk, 
                max_length=150, 
                min_length=50, 
                do_sample=False
            )[0]["summary_text"]
            
            # Split summary into sentences and format as bullet points
            sentences = re.split(r'(?<=[.!?])\s+', summary)
            for sentence in sentences:
                if sentence.strip() and len(sentence.strip()) > 10:
                    all_key_points.append(f"• {sentence.strip()}")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_points = []
        for point in all_key_points:
            if point.lower() not in seen:
                seen.add(point.lower())
                unique_points.append(point)
        
        return "\n".join(unique_points[:15])  # Limit to 15 key points
        
    except Exception as e:
        raise ValueError(f"Error extracting key points: {str(e)}")

def generate_detailed_summary(text: str) -> str:
    """Generate comprehensive multi-paragraph summary"""
    try:
        chunks = split_text_into_chunks(text, 900)
        summaries = []
        
        for i, chunk in enumerate(chunks):
            # Generate detailed summary for each chunk
            summary = summarizer_model(
                chunk,
                max_length=250,
                min_length=100,
                do_sample=False
            )[0]["summary_text"]
            summaries.append(summary)
        
        # Combine and format as multiple paragraphs
        if len(summaries) == 1:
            return summaries[0]
        else:
            # Create cohesive multi-paragraph summary
            detailed_summary = ""
            for i, summary in enumerate(summaries):
                if i == 0:
                    detailed_summary += f"{summary}\n\n"
                elif i == len(summaries) - 1:
                    detailed_summary += f"Furthermore, {summary.lower()}"
                else:
                    detailed_summary += f"Additionally, {summary.lower()}\n\n"
            
            return detailed_summary.strip()
            
    except Exception as e:
        raise ValueError(f"Error generating detailed summary: {str(e)}")

def generate_short_summary(text: str) -> str:
    """Generate more detailed but still single paragraph summary"""
    try:
        chunks = split_text_into_chunks(text, 900)
        
        if len(chunks) == 1:
            # Single chunk - direct summarization with more detail
            summary = summarizer_model(
                chunks[0],
                max_length=180,  # Increased from 120
                min_length=80,   # Increased from 40
                do_sample=False
            )[0]["summary_text"]
            return summary
        else:
            # Multiple chunks - summarize each then combine
            chunk_summaries = []
            for chunk in chunks:
                summary = summarizer_model(
                    chunk,
                    max_length=120,  # Increased from 80
                    min_length=60,   # Increased from 30
                    do_sample=False
                )[0]["summary_text"]
                chunk_summaries.append(summary)
            
            # Combine chunk summaries into single paragraph
            combined_text = " ".join(chunk_summaries)
            
            # Final summarization to create detailed but concise paragraph
            final_summary = summarizer_model(
                combined_text,
                max_length=200,  # Increased from 150
                min_length=100,  # Increased from 50
                do_sample=False
            )[0]["summary_text"]
            
            return final_summary
            
    except Exception as e:
        raise ValueError(f"Error generating short summary: {str(e)}")

def summarize_text(text: str, mode: str = "short") -> str:
    """Main summarization function with improved modes and larger text support"""
    
    # Validate input
    if not text or len(text.strip()) < 50:
        raise ValueError("Input text must be at least 50 characters long.")
    
    word_count = count_words(text)
    if word_count > 5000:
        raise ValueError("Input text must be under 5000 words for optimal processing.")
    
    # Clean and preprocess text
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Route to appropriate summarization method
    try:
        if mode == "keypoints":
            return extract_key_points(text)
        elif mode == "detailed":
            return generate_detailed_summary(text)
        elif mode == "short":
            return generate_short_summary(text)
        else:
            # Default to short summary
            return generate_short_summary(text)
            
    except Exception as e:
        raise ValueError(f"Summarization failed: {str(e)}")
