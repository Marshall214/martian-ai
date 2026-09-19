# utils/proof_ai.py
import re

# Load Llama humanizer
from utils.smart_humanizer import rewrite_with_llama

def count_words(text: str) -> int:
    """Count words in text, excluding extra whitespace."""
    return len(re.findall(r'\b\w+\b', text))

def calculate_ai_detection_score(text: str) -> float:
    """
    ENHANCED AI detection score calibrated to match external detectors like ZeroGPT.
    More aggressive scoring to ensure better external compatibility.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    
    if len(words) == 0:
        return 50.0
    
    ai_indicators = 0
    
    # EXPANDED AI indicators - aligned with ZeroGPT patterns
    strong_ai_phrases = [
        # High-confidence AI patterns
        'it is important to note', 'it should be noted', 'it is worth mentioning',
        'furthermore', 'moreover', 'additionally', 'consequently', 'therefore',
        'this study demonstrates', 'research shows', 'studies indicate',
        'evidence indicates', 'findings demonstrate', 'analysis reveals',
        'comprehensive analysis', 'systematic approach', 'rigorous assessment',
        'multidisciplinary approach', 'evidence-based decisions', 'transformative potential',
        'strategic planning', 'actionable knowledge', 'driving innovation',
        
        # Academic formality markers (ZeroGPT sensitive)
        'in conclusion', 'to summarize', 'in summary', 'overall',
        'on the other hand', 'nevertheless', 'however', 'whereas',
        'in light of this', 'given these considerations', 'taking into account',
        'it becomes evident that', 'one can observe that', 'it is apparent that',
        
        # Additional ZeroGPT triggers
        'the aforementioned', 'the preceding', 'the following',
        'serves to illustrate', 'warrants further investigation',
        'bears emphasizing', 'cannot be overstated', 'plays a pivotal role',
        'constitutes a significant', 'represents a crucial',
        'comprehensive examination', 'thorough investigation',
        'detailed scrutiny', 'extensive evaluation'
    ]
    
    # Higher penalty for AI phrases (ZeroGPT alignment)
    ai_phrase_count = sum(1 for phrase in strong_ai_phrases if phrase in text.lower())
    ai_indicators += ai_phrase_count * 25  # Increased penalty
    
    # ENHANCED sentence pattern analysis (ZeroGPT focus)
    sentences = re.split(r'[.!?]+', text)
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    if clean_sentences:
        # Check for overly uniform sentence structure
        sentence_lengths = [len(s.split()) for s in clean_sentences]
        if len(sentence_lengths) > 2:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            length_variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            
            # ZeroGPT is sensitive to uniform structures
            if length_variance < 10:  # More strict
                ai_indicators += 20  # Higher penalty
        
        # Check for repetitive sentence starters
        sentence_starters = [s.split()[0].lower() for s in clean_sentences if s.split()]
        
        if sentence_starters:
            starter_counts = {}
            for starter in sentence_starters:
                starter_counts[starter] = starter_counts.get(starter, 0) + 1
            
            max_repetition = max(starter_counts.values()) if starter_counts else 0
            if max_repetition > 2:
                ai_indicators += max_repetition * 12  # Higher penalty
    
    # EXPANDED academic buzzword detection (ZeroGPT sensitive)
    academic_buzzwords = [
        'significantly', 'substantially', 'comprehensively', 'extensively',
        'systematically', 'rigorously', 'critically', 'fundamentally',
        'demonstrate', 'facilitate', 'utilize', 'establish', 'implement',
        'optimal', 'robust', 'innovative', 'sophisticated', 'pivotal',
        'crucial', 'paramount', 'distinctive', 'comprehensive',
        
        # Additional ZeroGPT triggers
        'ubiquitous', 'profound', 'imperative', 'paradigm', 'myriad',
        'encompasses', 'multifaceted', 'intricate', 'nuanced', 'holistic',
        'proliferation', 'emergence', 'advent', 'unprecedented', 'inherent',
        'manifest', 'elucidate', 'exemplify', 'substantiate', 'corroborate'
    ]
    
    buzzword_count = sum(1 for word in academic_buzzwords if word in text.lower())
    buzzword_density = buzzword_count / len(words) if words else 0
    if buzzword_density > 0.02:  # Stricter threshold
        ai_indicators += 18  # Higher penalty
    
    # ZeroGPT patterns - lack of contractions is major red flag
    contractions = [
        "don't", "can't", "won't", "isn't", "aren't", "hasn't", "haven't", "doesn't",
        "wasn't", "weren't", "shouldn't", "couldn't", "wouldn't", 
        "they're", "we're", "you're", "it's", "that's", "i'm", "i've", "i'll"
    ]
    contraction_count = sum(1 for contraction in contractions if contraction in text.lower())
    if contraction_count == 0 and len(words) > 25:  # Stricter
        ai_indicators += 15  # Higher penalty
    else:
        ai_indicators -= contraction_count * 3  # More reward
    
    # Enhanced informal language detection
    informal_words = [
        'actually', 'really', 'pretty', 'quite', 'kind of', 'sort of', 'basically', 'anyway',
        'honestly', 'frankly', 'obviously', 'clearly', 'definitely', 'totally',
        'yeah', 'okay', 'sure', 'stuff', 'things', 'lots', 'super', 'way',
        'a bit', 'a little', 'kinda', 'sorta', 'gonna', 'wanna'
    ]
    informal_count = sum(1 for word in informal_words if word in text.lower())
    ai_indicators -= informal_count * 6  # Higher reward
    
    # Personal pronouns check - ZeroGPT values personal language
    personal_pronouns = ['i', 'we', 'you', 'my', 'our', 'your', 'me', 'us']
    pronoun_count = sum(1 for pronoun in personal_pronouns if f' {pronoun} ' in f' {text.lower()} ')
    if pronoun_count == 0 and len(words) > 40:  # Stricter
        ai_indicators += 12  # Higher penalty
    else:
        ai_indicators -= pronoun_count * 2  # More reward
    
    # ZeroGPT sensitive patterns
    # Complex sentence structures
    complex_patterns = [
        'in order to', 'with regard to', 'in relation to', 'with respect to',
        'in accordance with', 'in conjunction with', 'as a consequence of',
        'for the purpose of', 'in the context of', 'by means of'
    ]
    complex_count = sum(1 for pattern in complex_patterns if pattern in text.lower())
    ai_indicators += complex_count * 8
    
    # Passive voice (AI loves passive voice)
    passive_indicators = [
        'was conducted', 'were analyzed', 'was observed', 'were found',
        'was determined', 'were identified', 'was established', 'were examined',
        'is considered', 'are regarded', 'is recognized', 'are acknowledged'
    ]
    passive_count = sum(1 for phrase in passive_indicators if phrase in text.lower())
    ai_indicators += passive_count * 10
    
    # Hedge language (AI uncertainty patterns)
    hedging = [
        'it appears that', 'it seems that', 'it is likely that',
        'it is possible that', 'it may be that', 'one might argue',
        'one could suggest', 'one may conclude'
    ]
    hedge_count = sum(1 for phrase in hedging if phrase in text.lower())
    ai_indicators += hedge_count * 12
    
    # Reward casual connectors more heavily
    casual_connectors = ['but', 'so', 'and', 'plus', 'also', 'too', 'though', 'still', 'yet', 'well']
    casual_count = sum(1 for connector in casual_connectors if f' {connector} ' in f' {text.lower()} ')
    ai_indicators -= casual_count * 3  # Higher reward
    
    # Questions and exclamations (human traits)
    question_count = text.count('?')
    ai_indicators -= question_count * 5  # Higher reward
    
    exclamation_count = text.count('!')
    ai_indicators -= exclamation_count * 4  # Higher reward
    
    # ZeroGPT calibrated base score
    base_score = 8  # Higher base to align with ZeroGPT
    final_score = base_score + ai_indicators
    final_score = max(1, min(final_score, 99))  # Allow higher ceiling
    
    return round(final_score, 1)

def proofread_text(text: str) -> dict:
    """
    Semantic humanization system using Llama 3.1 8B.
    
    Sends the input text to the locally-hosted Llama model for rewriting,
    then scores both the original and rewritten text using the AI detection
    heuristic.

    Args:
        text: The text to humanize (50-1500 words).

    Returns:
        A dict with original/humanized text, word counts, AI scores, and
        improvement metrics.

    Raises:
        ValueError: If word count is outside the 50-1500 range.
        RuntimeError: If Llama model fails (no silent fallback).
    """
    word_count = count_words(text)
    
    if not (50 <= word_count <= 1500):
        raise ValueError(f"Input text must be between 50 and 1500 words. Current word count: {word_count}")

    # Calculate AI detection score BEFORE humanization
    ai_score_before = calculate_ai_detection_score(text)
    print(f"🎯 Starting semantic humanization | Initial AI score: {ai_score_before}%")
    
    # Call Llama — let errors propagate so the user gets a clear error message
    # instead of silently receiving their original text back.
    print("🔄 Calling Llama 3.1 8B to humanize text...")
    humanized_text = rewrite_with_llama(text)

    current_score = calculate_ai_detection_score(humanized_text)
    
    # Final status report
    print(f"✅ Humanization complete → New AI score: {current_score}%")
    
    return {
        "original_text": text,
        "humanized_text": humanized_text,
        "original_word_count": word_count,
        "humanized_word_count": count_words(humanized_text),
        "ai_score_before_humanizing": ai_score_before,
        "ai_score_after_humanizing": current_score,
        "improvement_percentage": round(max(0, ai_score_before - current_score), 1),
        "target_achieved": current_score < 20,
        "iterations_used": 1
    }