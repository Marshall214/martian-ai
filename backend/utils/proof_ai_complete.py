# utils/proof_ai.py
from transformers import pipeline
from difflib import SequenceMatcher
import re

# Load multiple models for better humanization
try:
    # Primary: T5-large for better instruction following
    humanization_model = pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        truncation=True,
        device=0 if __import__('torch').cuda.is_available() else -1
    )
    model_type = "flan-t5"
except Exception as e:
    try:
        # Fallback: T5-base if flan-t5-large fails
        humanization_model = pipeline(
            "text2text-generation", 
            model="t5-base",
            truncation=True
        )
        model_type = "t5-base"
    except Exception as e2:
        # Final fallback: Use paraphrasing model
        humanization_model = pipeline(
            "text2text-generation",
            model="Vamsi/T5_Paraphrase_Paws",
            truncation=True
        )
        model_type = "paraphrase"

def count_words(text: str) -> int:
    """Count words in text, excluding extra whitespace."""
    return len(re.findall(r'\b\w+\b', text))

def calculate_ai_detection_score(text: str) -> float:
    """
    Enhanced AI detection score calculation.
    Higher score = more likely to be AI-generated.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    
    if len(words) == 0:
        return 50.0
    
    ai_indicators = 0
    
    # Strong AI indicators with measured penalties  
    strong_ai_phrases = [
        'it is important to note', 'it should be noted', 'it is worth mentioning',
        'furthermore', 'moreover', 'additionally', 'consequently', 'therefore',
        'in conclusion', 'to summarize', 'in summary', 'overall',
        'this study demonstrates', 'research shows', 'studies indicate',
        'it can be concluded', 'the results suggest', 'evidence indicates',
        'significantly transformed', 'critical concerns', 'ongoing research',
        'multidisciplinary approach', 'rigorous oversight', 'policy frameworks',
        'systematic extraction', 'evidence-based decisions', 'transformative potential',
        'persistent challenges', 'technical proficiency', 'interdisciplinary approach',
        'equitable and sustainable', 'actionable knowledge', 'strategic planning',
        'indispensable discipline', 'complex datasets', 'driving innovation'
    ]
    
    # Count AI phrases with penalty
    ai_phrase_count = sum(1 for phrase in strong_ai_phrases if phrase in text.lower())
    ai_indicators += ai_phrase_count * 12
    
    # Check for AI-typical sentence patterns
    sentences = re.split(r'[.!?]+', text)
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    if clean_sentences:
        # Penalty for uniform sentence structure
        sentence_lengths = [len(s.split()) for s in clean_sentences]
        if len(sentence_lengths) > 2:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            length_variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            
            if length_variance < 10:
                ai_indicators += 15
        
        # Check for repetitive sentence starters
        sentence_starters = []
        for sentence in clean_sentences:
            words_in_sentence = sentence.split()
            if len(words_in_sentence) >= 1:
                starter = words_in_sentence[0].lower()
                sentence_starters.append(starter)
        
        if sentence_starters:
            starter_counts = {}
            for starter in sentence_starters:
                starter_counts[starter] = starter_counts.get(starter, 0) + 1
            
            max_repetition = max(starter_counts.values()) if starter_counts else 0
            if max_repetition > 2:
                ai_indicators += max_repetition * 5
    
    # Check for academic buzzword density
    academic_buzzwords = [
        'significantly', 'critically', 'essentially', 'fundamentally', 'comprehensively',
        'extensively', 'substantially', 'considerably', 'notably', 'remarkably'
    ]
    
    buzzword_count = sum(1 for word in academic_buzzwords if word in text.lower())
    buzzword_density = buzzword_count / len(words) if words else 0
    if buzzword_density > 0.03:
        ai_indicators += 12
    
    # Fixed base score calculation - no random hash
    base_score = 25
    final_score = base_score + ai_indicators
    final_score = min(final_score, 95)
    
    return round(final_score, 1)

def detect_academic_discipline(text: str) -> str:
    """Detect the academic discipline to tailor humanization approach."""
    text_lower = text.lower()
    
    disciplines = {
        'stem': ['algorithm', 'data', 'method', 'analysis', 'system', 'model', 'experiment', 
                'technology', 'process', 'function', 'variable', 'parameter', 'hypothesis'],
        'social': ['society', 'behavior', 'culture', 'social', 'community', 'individual', 
                  'group', 'participant', 'survey', 'interview', 'qualitative', 'quantitative'],
        'humanities': ['literature', 'text', 'narrative', 'interpretation', 'meaning', 
                      'context', 'historical', 'cultural', 'linguistic', 'discourse'],
        'business': ['organization', 'management', 'strategy', 'performance', 'market', 
                    'business', 'economic', 'financial', 'customer', 'competitive'],
        'medical': ['patient', 'treatment', 'clinical', 'medical', 'health', 'disease', 
                   'therapy', 'diagnosis', 'symptom', 'intervention']
    }
    
    scores = {}
    for discipline, keywords in disciplines.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[discipline] = score
    
    return max(scores.items(), key=lambda x: x[1])[0] if scores else 'general'

def apply_aggressive_humanization(text: str, iteration: int) -> str:
    """Apply comprehensive humanization with vast vocabulary."""
    
    # Massive replacement dictionary - cycling through options based on iteration
    replacements = {
        # Transitions
        r'\bfurthermore,?\s*': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that'][iteration % 5] + ', ',
        r'\bmoreover,?\s*': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that'][iteration % 5] + ', ',
        r'\badditionally,?\s*': ['also', 'plus', 'what\'s more', 'too', 'as well'][iteration % 5] + ', ',
        r'\bconsequently,?\s*': ['so', 'as a result', 'this means', 'because of this'][iteration % 4] + ', ',
        r'\btherefore,?\s*': ['so', 'as a result', 'this means', 'hence'][iteration % 4] + ', ',
        r'\bhowever,?\s*': ['but', 'yet', 'still', 'though', 'even so'][iteration % 5] + ', ',
        
        # Formal phrases to casual
        r'\bit is important to note that\b': ['notably', 'worth mentioning', 'keep in mind', 'by the way'][iteration % 4] + ', ',
        r'\bit should be noted that\b': ['notably', 'worth mentioning', 'importantly'][iteration % 3] + ', ',
        r'\bin conclusion,?\s*': ['to wrap up', 'in summary', 'overall', 'finally'][iteration % 4] + ', ',
        r'\bto summarize,?\s*': ['to sum up', 'in short', 'overall', 'basically'][iteration % 4] + ', ',
        
        # Research language
        r'\bthis study demonstrates\b': ['research shows', 'we found', 'data reveals', 'studies find'][iteration % 4],
        r'\bresearch shows\b': ['studies find', 'evidence suggests', 'data shows', 'we found'][iteration % 4],
        r'\bstudies indicate\b': ['research suggests', 'findings show', 'data points to'][iteration % 3],
        r'\bevidence indicates\b': ['data shows', 'findings suggest', 'research points to'][iteration % 3],
        
        # Academic buzzwords
        r'\bsignificantly\b': ['greatly', 'substantially', 'considerably', 'dramatically'][iteration % 4],
        r'\bsubstantially\b': ['greatly', 'considerably', 'dramatically', 'notably'][iteration % 4],
        r'\bfundamentally\b': ['basically', 'essentially', 'at its core', 'primarily'][iteration % 4],
        r'\bessentially\b': ['basically', 'at its core', 'primarily', 'mainly'][iteration % 4],
        r'\bcomprehensively\b': ['thoroughly', 'completely', 'fully', 'extensively'][iteration % 4],
        r'\bremarkably\b': ['surprisingly', 'notably', 'impressively', 'amazingly'][iteration % 4],
        
        # Verbs to natural alternatives
        r'\bdemonstrates\b': ['shows', 'reveals', 'proves', 'illustrates'][iteration % 4],
        r'\bindicates\b': ['shows', 'suggests', 'points to', 'reveals'][iteration % 4],
        r'\breveals\b': ['shows', 'uncovers', 'exposes', 'demonstrates'][iteration % 4],
        r'\bestablishes\b': ['proves', 'shows', 'confirms', 'sets up'][iteration % 4],
        r'\bfacilitates\b': ['helps', 'enables', 'makes easier', 'supports'][iteration % 4],
        r'\butilizes\b': ['uses', 'employs', 'applies', 'works with'][iteration % 4],
        
        # Complex academic phrases
        r'\bsystematic extraction\b': 'organized gathering',
        r'\bevidence-based decisions\b': 'data-driven choices', 
        r'\btransformative potential\b': 'game-changing possibilities',
        r'\bpersistent challenges\b': 'ongoing problems',
        r'\btechnical proficiency\b': 'technical skills',
        r'\binterdisciplinary approach\b': 'cross-field method',
        r'\bmultidisciplinary approach\b': 'multi-field method',
        r'\bactionable knowledge\b': 'useful insights',
        r'\bstrategic planning\b': 'smart planning',
        r'\bindispensable discipline\b': 'essential field',
        r'\bcomplex datasets\b': 'complicated data',
        r'\bdriving innovation\b': 'pushing new ideas',
        r'\bcritical concerns\b': 'key issues',
        r'\bongoing research\b': 'current studies',
        r'\brigorous oversight\b': 'careful monitoring',
        r'\bpolicy frameworks\b': 'policy structures',
    }
    
    # Apply all replacements
    humanized = text
    for pattern, replacement in replacements.items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    return humanized

def proofread_text(text: str) -> dict:
    """
    Advanced iterative humanization system that reduces AI score to < 20%.
    """
    word_count = count_words(text)
    
    if not (50 <= word_count <= 1500):
        raise ValueError(f"Input text must be between 50 and 1500 words. Current word count: {word_count}")

    # Calculate AI detection score BEFORE humanization
    ai_score_before = calculate_ai_detection_score(text)
    print(f"Starting humanization - Initial AI score: {ai_score_before}%")
    
    humanized_text = text
    current_score = ai_score_before
    max_iterations = 6
    iteration = 0
    
    # Iterative humanization until score < 20%
    while current_score >= 20 and iteration < max_iterations:
        print(f"Iteration {iteration + 1}: Current AI score {current_score}% - humanizing...")
        
        # Apply aggressive humanization
        humanized_text = apply_aggressive_humanization(humanized_text, iteration)
        
        # AI Model enhancement
        try:
            discipline = detect_academic_discipline(text)
            
            prompt = f"""Rewrite this {discipline} text to sound completely natural and human. Make it conversational but accurate.

Remove all formal academic language. Make it sound like someone explaining this naturally:
{humanized_text}

Natural version:"""
            
            if model_type == "flan-t5":
                ai_result = humanization_model(
                    prompt,
                    max_new_tokens=word_count * 2,
                    do_sample=True,
                    temperature=0.9 + (iteration * 0.1),
                    top_p=0.8,
                    repetition_penalty=1.4
                )[0]["generated_text"].strip()
            else:
                ai_result = humanization_model(
                    f"paraphrase: {humanized_text}",
                    max_new_tokens=word_count * 2,
                    do_sample=True,
                    temperature=0.9 + (iteration * 0.1)
                )[0]["generated_text"].strip()
            
            # Clean and validate AI output
            ai_result = re.sub(r'^.*?Natural version:\s*', '', ai_result, flags=re.IGNORECASE)
            
            if (len(ai_result.split()) >= word_count * 0.6 and 
                len(ai_result.split()) <= word_count * 1.8 and
                ai_result and not ai_result.lower().startswith(('sorry', 'i cannot'))):
                humanized_text = ai_result
                
        except Exception as e:
            print(f"AI model failed: {e}")
        
        # Emergency measures if score not improving
        if iteration >= 2 and current_score >= ai_score_before - 10:
            print("Applying emergency humanization...")
            
            # Super casual replacements
            emergency_fixes = {
                r'\bdata science\b': 'working with data',
                r'\bmachine learning\b': 'AI systems',
                r'\balgorithms?\b': 'computer programs',
                r'\bmethodology\b': 'approach',
                r'\bframework\b': 'structure',
                r'\bimplementation\b': 'putting it to work',
                r'\bThe study\b': 'This research',
                r'\bThis study\b': 'Our work',
                r'\bThe research\b': 'This work',
                r'\baccording to\b': 'based on',
                r'\bin terms of\b': 'when it comes to',
                r'\bwith respect to\b': 'regarding',
            }
            
            for pattern, replacement in emergency_fixes.items():
                humanized_text = re.sub(pattern, replacement, humanized_text, flags=re.IGNORECASE)
        
        # Final cleanup
        humanized_text = re.sub(r'\s+([,.!?;:])', r'\1', humanized_text)
        humanized_text = re.sub(r'\s+', ' ', humanized_text)
        humanized_text = re.sub(r'\.([A-Z][a-z]+)', r'. \1', humanized_text)
        
        if humanized_text and not humanized_text[-1] in '.!?':
            humanized_text += '.'
        
        # Calculate new score
        current_score = calculate_ai_detection_score(humanized_text)
        print(f"Iteration {iteration + 1} complete - AI score: {current_score}%")
        
        iteration += 1
    
    print(f"Final result - AI score reduced from {ai_score_before}% to {current_score}%")
    
    return {
        "original_text": text,
        "humanized_text": humanized_text,
        "original_word_count": word_count,
        "humanized_word_count": count_words(humanized_text),
        "ai_score_before_humanizing": ai_score_before,
        "ai_score_after_humanizing": current_score,
        "improvement_percentage": round(max(0, ai_score_before - current_score), 1)
    }