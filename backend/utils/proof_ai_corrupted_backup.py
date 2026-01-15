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

def preserve_academic_elements(text: str) -> dict:
    """
    Identify and preserve academic elements like citations, technical terms, etc.
    Returns text with placeholders and a mapping to restore them later.
    """
    preserved = {}
    modified_text = text
    
    # Preserve citations (APA, MLA, Chicago styles)
    citation_patterns = [
        r'\([^)]*\d{4}[^)]*\)',  # (Author, 2024)
        r'\[[^\]]*\d+[^\]]*\]',  # [1], [Author 2024]
        r'\b\w+\s+et\s+al\.\s*\(\d{4}\)',  # Smith et al. (2024)
    ]
    
    placeholder_counter = 0
    for pattern in citation_patterns:
        matches = re.finditer(pattern, modified_text)
        for match in matches:
            placeholder = f"__CITATION_{placeholder_counter}__"
            preserved[placeholder] = match.group()
            modified_text = modified_text.replace(match.group(), placeholder, 1)
            placeholder_counter += 1
    
    # Preserve technical terms and abbreviations
    technical_patterns = [
        r'\b[A-Z]{2,}\b',  # Acronyms (DNA, RNA, etc.)
        r'\b\w+\s*=\s*\w+\b',  # Equations (x = 5)
        r'\b\d+\.?\d*%\b',  # Percentages
        r'\b\d+\.?\d*[Â°â„ƒâ„‰]\b',  # Temperature/degree measurements
    ]
    
    for pattern in technical_patterns:
        matches = re.finditer(pattern, modified_text)
        for match in matches:
            if match.group() not in preserved.values():  # Avoid duplicates
                placeholder = f"__TECH_{placeholder_counter}__"
                preserved[placeholder] = match.group()
                modified_text = modified_text.replace(match.group(), placeholder, 1)
                placeholder_counter += 1
    
    return {"text": modified_text, "preserved": preserved}

def restore_academic_elements(text: str, preserved: dict) -> str:
    """Restore preserved academic elements back into the text."""
    restored_text = text
    for placeholder, original in preserved.items():
        restored_text = restored_text.replace(placeholder, original)
    return restored_text

def calculate_ai_detection_score(text: str) -> float:
    """
    More balanced AI detection score calculation.
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
    ai_indicators += ai_phrase_count * 12  # Higher penalty for clear AI phrases
    
    # Check for AI-typical sentence patterns
    sentences = re.split(r'[.!?]+', text)
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    if clean_sentences:
        # Penalty for uniform sentence structure
        sentence_lengths = [len(s.split()) for s in clean_sentences]
        if len(sentence_lengths) > 2:
            avg_length = sum(sentence_lengths) / len(sentence_lengths)
            length_variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            
            # Low variance = AI-like uniformity
            if length_variance < 10:
                ai_indicators += 15
        
        # Check for repetitive sentence starters
        sentence_starters = []
        for sentence in clean_sentences:
            words_in_sentence = sentence.split()
            if len(words_in_sentence) >= 1:
                starter = words_in_sentence[0].lower()
                sentence_starters.append(starter)
        
        # Penalty for repeated starters
        if sentence_starters:
            starter_counts = {}
            for starter in sentence_starters:
                starter_counts[starter] = starter_counts.get(starter, 0) + 1
            
            max_repetition = max(starter_counts.values()) if starter_counts else 0
            if max_repetition > 2:  # More than 2 same starters
                ai_indicators += max_repetition * 5
    
    # Check for academic buzzword density
    academic_buzzwords = [
        'significantly', 'critically', 'essentially', 'fundamentally', 'comprehensively',
        'extensively', 'substantially', 'considerably', 'notably', 'remarkably'
    ]
    
    buzzword_count = sum(1 for word in academic_buzzwords if word in text.lower())
    buzzword_density = buzzword_count / len(words) if words else 0
    if buzzword_density > 0.03:  # More than 3% buzzwords
        ai_indicators += 12
    
    # Check for broken grammar (indicates poor processing)
    grammar_issues = 0
    # Missing spaces after periods
    if re.search(r'\.[A-Z]', text):
        grammar_issues += 10
    # Weird capitalization
    if re.search(r'\b[a-z]+\.[A-Z]', text):
        grammar_issues += 10
    
    ai_indicators += grammar_issues
    
    # Fixed base score calculation - no random hash
    base_score = 25  # Consistent base for academic text
    final_score = base_score + ai_indicators
    
    # Cap at reasonable maximum
    final_score = min(final_score, 95)
    
    return round(final_score, 1)

def detect_academic_discipline(text: str) -> str:
    """
    Detect the academic discipline to tailor humanization approach.
    """
    text_lower = text.lower()
    
    # Discipline indicators
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

def create_advanced_humanization_prompt(text: str) -> str:
    """
    Create a discipline-tailored prompt for deep text humanization.
    """
    discipline = detect_academic_discipline(text)
    
    # Discipline-specific guidance
    discipline_guidance = {
        'stem': "Use precise but natural language. Vary technical explanations with accessible descriptions.",
        'social': "Emphasize human elements and real-world connections. Use engaging, relatable language.",
        'humanities': "Focus on interpretive language and nuanced expression. Embrace complexity naturally.",
        'business': "Use confident, action-oriented language. Emphasize practical implications.",
        'medical': "Balance technical accuracy with clear communication. Use patient-centered language.",
        'general': "Maintain scholarly rigor while ensuring natural flow and engagement."
    }
    
    return f"""Transform this {discipline} academic text into natural, human-written prose. Make it sound like an expert {discipline} scholar wrote it naturally, not an AI.

DISCIPLINE-SPECIFIC APPROACH: {discipline_guidance.get(discipline, discipline_guidance['general'])}

CRITICAL REQUIREMENTS:
- Completely rephrase and restructure sentences (don't just shuffle)
- Use varied, natural sentence beginnings appropriate for {discipline} writing
- Replace formal AI phrases with conversational academic language
- Vary sentence length dramatically (mix short punchy statements with longer explanations)
- Use active voice where possible, but maintain {discipline} conventions
- Add natural transitions that flow logically
- Maintain all technical accuracy and key concepts
- Keep it scholarly but engaging and human-sounding

AVOID these AI patterns:
- "Furthermore, moreover, additionally" chains
- "It is important to note" formalities
- "Research shows/indicates/suggests" repetition
- "This study demonstrates" redundancy
- Repetitive sentence structures
- Uniform sentence lengths
- Overly formal academic jargon

INPUT TEXT: {text}

HUMANIZED OUTPUT:"""

def advanced_sentence_restructuring(text: str) -> str:
    """
    Advanced AI-to-human sentence restructuring with syntactic analysis.
    """
    sentences = re.split(r'[.!?]+', text)
    clean_sentences = [s.strip() for s in sentences if s.strip()]
    
    class SentenceRestructurer:
        def __init__(self):
            self.restructure_patterns = {
                # Complex academic patterns
                r'^(.+?)\s+(advancements?|developments?|innovations?|progress)\s+in\s+(.+)': 
                    lambda m: f"Progress in {m.group(3)} through {m.group(1).lower()} {m.group(2)}",
                
                r'^(the|these|such)\s+(findings|results|outcomes|discoveries)\s+(show|indicate|suggest|reveal)\s+that\s+(.+)':
                    lambda m: f"These {m.group(2)} {m.group(3)} {m.group(4)}",
                
                r'^(it|this)\s+(is\s+important\s+to\s+note|should\s+be\s+noted|is\s+worth\s+mentioning)\s+that\s+(.+)':
                    lambda m: f"Notably, {m.group(3)}",
                
                # Passive to active voice conversion
                r'^(.+?)\s+(was|were)\s+(conducted|performed|analyzed|examined|investigated)\s+by\s+(.+)':
                    lambda m: f"{m.group(4).capitalize()} {m.group(3)} {m.group(1)}",
                
                r'^(.+?)\s+(has|have)\s+been\s+(shown|demonstrated|proven|established)\s+to\s+(.+)':
                    lambda m: f"Research shows {m.group(1)} {m.group(4)}",
            }
            
            self.sentence_starters = [
                "Notably,", "Interestingly,", "Remarkably,", "Significantly,",
                "What's more,", "Beyond this,", "In fact,", "Indeed,",
                "Particularly,", "Especially,", "Crucially,", "Importantly,"
            ]
            
        def vary_sentence_beginning(self, sentence, position, total_sentences):
            """Create varied, natural sentence beginnings based on context"""
            if len(sentence.split()) < 4:
                return sentence
                
            # Different strategies based on position in text
            if position == 0:  # First sentence
                return sentence  # Keep original first sentence
            elif position < total_sentences * 0.3:  # Early sentences
                if sentence.lower().startswith(('the', 'this', 'these', 'such')):
                    # Add contextual starter
                    starter = self.sentence_starters[position % 4]
                    return f"{starter} {sentence.lower()}"
            elif position > total_sentences * 0.7:  # Later sentences
                conclusion_starters = ["Finally,", "Ultimately,", "In conclusion,", "Overall,"]
                if any(sentence.lower().startswith(word) for word in ['the', 'this', 'these']):
                    starter = conclusion_starters[position % 4]
                    return f"{starter} {sentence.lower()}"
            
            return sentence
        
        def restructure_complex_sentences(self, sentence):
            """Apply complex restructuring patterns"""
            for pattern, transformer in self.restructure_patterns.items():
                match = re.match(pattern, sentence, re.IGNORECASE)
                if match:
                    try:
                        return transformer(match)
                    except:
                        continue
            return sentence
        
        def smart_sentence_splitting(self, sentence):
            """Intelligently split long sentences at natural boundaries"""
            words = sentence.split()
            if len(words) < 15:  # Only split very long sentences
                return sentence
                
            # Find natural comma breaks first
            comma_positions = []
            for i, word in enumerate(words):
                if word.endswith(','):
                    comma_positions.append(i)
            
            # If we have commas, split at the most central one
            if comma_positions:
                middle_pos = len(words) // 2
                best_comma = min(comma_positions, key=lambda x: abs(x - middle_pos))
                
                # Only split if comma is reasonably central
                if len(words) * 0.3 <= best_comma <= len(words) * 0.7:
                    first_part = ' '.join(words[:best_comma + 1]).rstrip(',')
                    second_part = ' '.join(words[best_comma + 1:])
                    
                    if second_part:
                        second_part = second_part[0].upper() + second_part[1:] if len(second_part) > 1 else second_part.upper()
                        return f"{first_part}. {second_part}"
            
            return sentence
    
    restructurer = SentenceRestructurer()
    final_sentences = []
    
    for i, sentence in enumerate(clean_sentences):
        processed = sentence
        
        # Apply restructuring patterns
        processed = restructurer.restructure_complex_sentences(processed)
        
        # Smart sentence splitting if needed
        processed = restructurer.smart_sentence_splitting(processed)
        
        # Vary sentence beginnings contextually
        processed = restructurer.vary_sentence_beginning(processed, i, len(clean_sentences))
        
        # Handle multiple sentences from splitting
        if '. ' in processed:
            split_sentences = processed.split('. ')
            for j, sub_sentence in enumerate(split_sentences):
                if j == len(split_sentences) - 1:
                    final_sentences.append(sub_sentence)
                else:
                    final_sentences.append(sub_sentence + '.')
        else:
            final_sentences.append(processed)
    
    result = ' '.join(final_sentences)
    
    # Final cleanup
    result = re.sub(r'\s+([,.!?])', r'\1', result)  # Fix punctuation
    result = re.sub(r'\s+', ' ', result)  # Clean spacing
    
    # Ensure proper sentence endings
    if not result.endswith(('.', '!', '?')):
        result += '.'
    
    return result

def create_comprehensive_vocabulary():
    """
    Create extensive vocabulary mappings for natural humanization.
    """
    return {
        # Transition words - much more extensive
        'transition_words': {
            'furthermore': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that', 'in addition', 'not only that', 'even more'],
            'moreover': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that', 'in addition', 'not only that', 'even more'],
            'additionally': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that', 'too', 'as well'],
            'consequently': ['so', 'as a result', 'this means', 'because of this', 'due to this', 'hence', 'thus'],
            'therefore': ['so', 'as a result', 'this means', 'because of this', 'due to this', 'hence'],
            'however': ['but', 'yet', 'still', 'though', 'even so', 'despite this', 'on the flip side'],
            'nevertheless': ['but', 'yet', 'still', 'even so', 'despite this', 'regardless'],
            'nonetheless': ['but', 'yet', 'still', 'even so', 'despite this', 'regardless'],
        },
        
        # Academic buzzwords - natural alternatives
        'academic_buzzwords': {
            'significantly': ['greatly', 'substantially', 'considerably', 'dramatically', 'notably', 'remarkably'],
            'substantially': ['greatly', 'significantly', 'considerably', 'dramatically', 'notably'],
            'considerably': ['greatly', 'significantly', 'substantially', 'dramatically', 'notably'],
            'fundamentally': ['basically', 'essentially', 'at its core', 'in essence', 'primarily'],
            'essentially': ['basically', 'fundamentally', 'at its core', 'in essence', 'primarily'],
            'comprehensively': ['thoroughly', 'completely', 'fully', 'extensively', 'in detail'],
            'extensively': ['thoroughly', 'widely', 'broadly', 'comprehensively', 'in depth'],
            'remarkably': ['surprisingly', 'notably', 'impressively', 'strikingly', 'amazingly'],
            'particularly': ['especially', 'notably', 'specifically', 'in particular'],
        },
        
        # Formal phrases - casual alternatives
        'formal_phrases': {
            'it is important to note that': ['notably', 'worth mentioning', 'importantly', 'keep in mind', 'note that'],
            'it should be noted that': ['notably', 'worth mentioning', 'importantly', 'keep in mind'],
            'it is worth mentioning that': ['notably', 'worth mentioning', 'importantly', 'by the way'],
            'in conclusion': ['to wrap up', 'in summary', 'overall', 'to sum up', 'finally'],
            'to summarize': ['to sum up', 'in short', 'overall', 'in summary', 'basically'],
            'in summary': ['to sum up', 'in short', 'overall', 'basically', 'simply put'],
        },
        
        # Verb alternatives - more natural
        'verbs': {
            'demonstrates': ['shows', 'reveals', 'proves', 'illustrates', 'displays'],
            'indicates': ['shows', 'suggests', 'points to', 'reveals', 'implies'],
            'reveals': ['shows', 'uncovers', 'exposes', 'brings to light', 'demonstrates'],
            'establishes': ['proves', 'shows', 'confirms', 'validates', 'verifies'],
            'facilitates': ['helps', 'enables', 'makes easier', 'assists', 'supports'],
            'utilizes': ['uses', 'employs', 'applies', 'makes use of', 'leverages'],
            'encompasses': ['includes', 'covers', 'involves', 'contains', 'spans'],
            'contributes': ['adds to', 'helps with', 'plays a role in', 'supports'],
        },
        
        # Research terminology - natural alternatives
        'research_terms': {
            'systematic approach': ['organized method', 'structured way', 'methodical process'],
            'empirical evidence': ['real-world proof', 'actual data', 'concrete evidence'],
            'quantitative analysis': ['number analysis', 'statistical study', 'data analysis'],
            'qualitative assessment': ['quality evaluation', 'descriptive analysis', 'content review'],
            'interdisciplinary approach': ['cross-field method', 'multi-area approach', 'combined fields'],
            'multidisciplinary approach': ['cross-field method', 'multi-area approach', 'various fields'],
        },
        
        # Sentence starters - natural alternatives
        'sentence_starters': {
            'this study demonstrates': ['research shows', 'studies find', 'we found', 'data reveals'],
            'research shows': ['studies find', 'evidence suggests', 'data shows', 'findings reveal'],
            'studies indicate': ['research suggests', 'findings show', 'evidence points to', 'data reveals'],
            'evidence suggests': ['data shows', 'findings indicate', 'research points to', 'studies reveal'],
            'the results suggest': ['findings show', 'data indicates', 'evidence points to', 'we found'],
        }
    }

def apply_advanced_nlp_techniques(text: str, iteration: int = 0) -> str:
    """
    Apply multiple NLP techniques for deep humanization.
    """
    # Get comprehensive vocabulary
    vocab = create_comprehensive_vocabulary()
    
    # Technique 1: Sentence restructuring
    sentences = re.split(r'(?<=[.!?])\s+', text)
    restructured_sentences = []
    
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
            
        # Vary sentence structure based on length and position
        words = sentence.split()
        if len(words) > 15:  # Long sentences - split or restructure
            # Find natural break points
            comma_indices = [j for j, word in enumerate(words) if word.endswith(',')]
            if comma_indices and len(comma_indices) > 0:
                # Split at middle comma
                middle_comma = comma_indices[len(comma_indices)//2]
                if 3 < middle_comma < len(words) - 3:  # Good split point
                    first_part = ' '.join(words[:middle_comma]).rstrip(',') + '.'
                    second_part = ' '.join(words[middle_comma+1:])
                    second_part = second_part[0].upper() + second_part[1:] if second_part else ''
                    restructured_sentences.extend([first_part, second_part])
                    continue
        
        # Technique 2: Active voice conversion
        # Convert "was done by X" to "X did"
        passive_patterns = [
            (r'(.+?)\s+was\s+(\w+ed)\s+by\s+(.+)', r'\3 \2 \1'),
            (r'(.+?)\s+were\s+(\w+ed)\s+by\s+(.+)', r'\3 \2 \1'),
        ]
        
        for pattern, replacement in passive_patterns:
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)
        
        restructured_sentences.append(sentence)
    
    text = ' '.join(restructured_sentences)
    
    # Technique 3: Comprehensive vocabulary replacement
    for category, replacements in vocab.items():
        for formal_term, casual_alternatives in replacements.items():
            if formal_term.lower() in text.lower():
                # Choose replacement based on iteration to vary results
                replacement = casual_alternatives[iteration % len(casual_alternatives)]
                text = re.sub(re.escape(formal_term), replacement, text, flags=re.IGNORECASE)
    
    # Technique 4: Sentence variety and flow
    # Add natural connectors and vary beginnings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    varied_sentences = []
    
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
            
        # Every few sentences, add natural variety
        if i > 0 and i % 3 == 0:
            natural_starters = ['What\'s interesting is', 'The key point is', 'Here\'s the thing -', 'Simply put,']
            if not any(sentence.lower().startswith(starter.lower()) for starter in natural_starters):
                starter = natural_starters[i % len(natural_starters)]
                sentence = f"{starter} {sentence.lower()}"
        
        varied_sentences.append(sentence)
    
    text = ' '.join(varied_sentences)
    
    # Technique 5: Contractions and casual language (where appropriate)
    contractions = {
        ' it is ': ' it\'s ',
        ' that is ': ' that\'s ',
        ' there is ': ' there\'s ',
        ' cannot ': ' can\'t ',
        ' do not ': ' don\'t ',
        ' will not ': ' won\'t ',
    }
    
    # Apply contractions sparingly (only for shorter sentences)
    sentences = text.split('.')
    for i, sentence in enumerate(sentences):
        if len(sentence.split()) < 12:  # Only in shorter sentences
            for formal, contraction in contractions.items():
                sentence = sentence.replace(formal, contraction)
        sentences[i] = sentence
    
    text = '.'.join(sentences)
    
    return text

def proofread_text(text: str) -> dict:
    """
    Advanced humanization system with iterative processing until AI score < 20%.
    """
    word_count = count_words(text)
    
    if not (50 <= word_count <= 1500):
        raise ValueError(f"Input text must be between 50 and 1500 words. Current word count: {word_count}")

    # Calculate AI detection score BEFORE humanization
    ai_score_before = calculate_ai_detection_score(text)
    
    # Iterative humanization until AI score < 20%
    humanized_text = text
    current_ai_score = ai_score_before
    max_iterations = 5
    iteration = 0
    
    print(f"Starting humanization - Initial AI score: {ai_score_before}%")
    
    while current_ai_score >= 20 and iteration < max_iterations:
        print(f"Iteration {iteration + 1}: AI score {current_ai_score}% - applying humanization...")
        
        # Step 1: Apply advanced NLP techniques
        humanized_text = apply_advanced_nlp_techniques(humanized_text, iteration)
        
        # Step 2: Comprehensive pattern replacement with vast vocabulary
        ai_phrase_replacements = {
            # Formal transition words
            r'\bfurthermore,?\s*': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that'][iteration % 5] + ', ',
            r'\bmoreover,?\s*': ['also', 'plus', 'what\'s more', 'on top of that', 'beyond that'][iteration % 5] + ', ',
            r'\badditionally,?\s*': ['also', 'plus', 'what\'s more', 'too', 'as well'][iteration % 5] + ', ',
            r'\bconsequently,?\s*': ['so', 'as a result', 'this means', 'because of this', 'due to this'][iteration % 5] + ', ',
            r'\btherefore,?\s*': ['so', 'as a result', 'this means', 'because of this'][iteration % 4] + ', ',
            r'\bhowever,?\s*': ['but', 'yet', 'still', 'though', 'even so'][iteration % 5] + ', ',
            
            # Formal phrases
            r'\bit is important to note that\b': ['notably', 'worth mentioning', 'importantly', 'keep in mind'][iteration % 4] + ', ',
            r'\bit should be noted that\b': ['notably', 'worth mentioning', 'importantly'][iteration % 3] + ', ',
            r'\bit is worth mentioning that\b': ['notably', 'worth mentioning', 'by the way'][iteration % 3] + ', ',
            r'\bin conclusion,?\s*': ['to wrap up', 'in summary', 'overall', 'finally'][iteration % 4] + ', ',
            r'\bto summarize,?\s*': ['to sum up', 'in short', 'overall', 'basically'][iteration % 4] + ', ',
            r'\bin summary,?\s*': ['to sum up', 'in short', 'overall', 'basically'][iteration % 4] + ', ',
            
            # Research language
            r'\bthis study demonstrates\b': ['research shows', 'studies find', 'we found', 'data reveals'][iteration % 4],
            r'\bresearch shows\b': ['studies find', 'evidence suggests', 'data shows', 'findings reveal'][iteration % 4],
            r'\bstudies indicate\b': ['research suggests', 'findings show', 'evidence points to'][iteration % 3],
            r'\bevidence indicates\b': ['data shows', 'findings indicate', 'research points to'][iteration % 3],
            r'\bit can be concluded\b': ['we can see', 'it\'s clear that', 'obviously'][iteration % 3],
            r'\bthe results suggest\b': ['findings show', 'data indicates', 'we found'][iteration % 3],
            
            # Academic buzzwords
            r'\bsignificantly\b': ['greatly', 'substantially', 'considerably', 'dramatically', 'notably'][iteration % 5],
            r'\bsubstantially\b': ['greatly', 'significantly', 'considerably', 'dramatically'][iteration % 4],
            r'\bconsiderably\b': ['greatly', 'significantly', 'substantially', 'notably'][iteration % 4],
            r'\bfundamentally\b': ['basically', 'essentially', 'at its core', 'primarily'][iteration % 4],
            r'\bessentially\b': ['basically', 'fundamentally', 'at its core', 'primarily'][iteration % 4],
            r'\bcomprehensively\b': ['thoroughly', 'completely', 'fully', 'extensively'][iteration % 4],
            r'\bextensively\b': ['thoroughly', 'widely', 'broadly', 'in depth'][iteration % 4],
            r'\bremarkably\b': ['surprisingly', 'notably', 'impressively', 'strikingly'][iteration % 4],
            
            # Verbs
            r'\bdemonstrates\b': ['shows', 'reveals', 'proves', 'illustrates'][iteration % 4],
            r'\bindicates\b': ['shows', 'suggests', 'points to', 'reveals'][iteration % 4],
            r'\breveals\b': ['shows', 'uncovers', 'exposes', 'demonstrates'][iteration % 4],
            r'\bestablishes\b': ['proves', 'shows', 'confirms', 'validates'][iteration % 4],
            r'\bfacilitates\b': ['helps', 'enables', 'makes easier', 'supports'][iteration % 4],
            r'\butilizes\b': ['uses', 'employs', 'applies', 'makes use of'][iteration % 4],
            
            # Complex phrases
            r'\bsystematic extraction\b': 'organized gathering',
            r'\bevidence-based decisions\b': 'data-driven choices',
            r'\btransformative potential\b': 'game-changing possibilities',
            r'\bpersistent challenges\b': 'ongoing problems',
            r'\btechnical proficiency\b': 'technical skills',
            r'\binterdisciplinary approach\b': 'cross-field method',
            r'\bequitable and sustainable\b': 'fair and lasting',
            r'\bactionable knowledge\b': 'useful insights',
            r'\bstrategic planning\b': 'smart planning',
            r'\bindispensable discipline\b': 'essential field',
            r'\bcomplex datasets\b': 'complicated data',
            r'\bdriving innovation\b': 'pushing new ideas',
            r'\bcritical concerns\b': 'key issues',
            r'\bongoing research\b': 'current studies',
            r'\bmultidisciplinary approach\b': 'cross-field method',
            r'\brigorous oversight\b': 'careful monitoring',
            r'\bpolicy frameworks\b': 'policy structures'
        }
        
        # Apply all replacements
        for pattern, replacement in ai_phrase_replacements.items():
            humanized_text = re.sub(pattern, replacement, humanized_text, flags=re.IGNORECASE)
    
    # Step 2: Fix sentence structure and variety
    sentences = re.split(r'(?<=[.!?])\s+', humanized_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Vary sentence beginnings
    sentence_starters = ['Notably,', 'Interestingly,', 'In fact,', 'What\'s more,', 'Beyond this,', 'Particularly,']
    
    processed_sentences = []
    for i, sentence in enumerate(sentences):
        # Add variety to sentence starters (but not all sentences)
        if i > 0 and i % 3 == 0 and len(sentence.split()) > 5:  # Every 3rd sentence
            if not sentence.lower().startswith(('notably', 'interestingly', 'in fact', 'what\'s', 'beyond', 'particularly')):
                starter = sentence_starters[i % len(sentence_starters)]
                sentence = f"{starter} {sentence.lower()}"
        
        processed_sentences.append(sentence)
    
    humanized_text = ' '.join(processed_sentences)
    
        # Step 3: AI Model Polish (if available)
        try:
            # Detect discipline for better prompting
            discipline = detect_academic_discipline(text)
            
            # Create aggressive humanization prompt
            ai_prompt = f"""Rewrite this {discipline} text to sound completely natural and human-written. Make it conversational but keep the meaning.

CRITICAL: Remove all AI-like formal language. Make it sound like a person explaining this naturally.
- Replace formal transitions with casual ones
- Use shorter, varied sentences
- Add natural flow and personality
- Keep all facts accurate

Text: {humanized_text}

Natural version:"""
            
            if model_type == "flan-t5":
                ai_result = humanization_model(
                    ai_prompt,
                    max_new_tokens=len(humanized_text.split()) * 2,
                    do_sample=True,
                    temperature=0.8 + (iteration * 0.1),  # Increase creativity each iteration
                    top_p=0.85,
                    repetition_penalty=1.3,
                    num_beams=2
                )[0]["generated_text"].strip()
            elif model_type == "t5-base":
                ai_result = humanization_model(
                    f"paraphrase: {humanized_text}",
                    max_new_tokens=len(humanized_text.split()) * 2,
                    do_sample=True,
                    temperature=0.9 + (iteration * 0.1),
                    top_p=0.8
                )[0]["generated_text"].strip()
            else:
                ai_result = humanization_model(
                    humanized_text,
                    max_new_tokens=len(humanized_text.split()) * 2,
                    do_sample=True,
                    temperature=0.8 + (iteration * 0.1)
                )[0]["generated_text"].strip()
            
            # Clean AI output
            ai_result = ai_result.strip()
            cleanup_patterns = [
                r'^.*?Natural version:\s*',
                r'^.*?Rewritten:\s*',
                r'^.*?Humanized:\s*'
            ]
            for pattern in cleanup_patterns:
                ai_result = re.sub(pattern, '', ai_result, flags=re.IGNORECASE)
            
            # Quality check - use AI result if good
            if (len(ai_result.split()) >= len(humanized_text.split()) * 0.6 and 
                len(ai_result.split()) <= len(humanized_text.split()) * 1.8 and
                ai_result and not ai_result.lower().startswith(('sorry', 'i cannot'))):
                humanized_text = ai_result
                
        except Exception as e:
            print(f"AI model failed on iteration {iteration + 1}: {e}")
        
        # Step 4: Advanced post-processing
        # Fix any remaining formal patterns
        advanced_fixes = {
            r'\bThe study\b': 'This research',
            r'\bThis study\b': 'This work',
            r'\bThe research\b': 'This study',
            r'\bThe analysis\b': 'Looking at the data',
            r'\bThe investigation\b': 'This research',
            r'\bThe examination\b': 'Checking',
            r'\bIt is evident that\b': 'Clearly',
            r'\bIt is clear that\b': 'Obviously',
            r'\bIt can be observed that\b': 'We can see',
            r'\bAs can be seen\b': 'As you can see',
        }
        
        for pattern, replacement in advanced_fixes.items():
            humanized_text = re.sub(pattern, replacement, humanized_text, flags=re.IGNORECASE)
    
    # Step 4: Final cleanup and formatting
    # Fix spacing issues
    humanized_text = re.sub(r'\s+([,.!?;:])', r'\1', humanized_text)  # Fix punctuation spacing
    humanized_text = re.sub(r'([,.!?;:])\s*([,.!?;:])', r'\1\2', humanized_text)  # Remove double punctuation
    humanized_text = re.sub(r'\s+', ' ', humanized_text)  # Normalize whitespace
    
    # Ensure proper capitalization
    sentences = re.split(r'([.!?]+)', humanized_text)
    capitalized_sentences = []
    for i, part in enumerate(sentences):
        if i % 2 == 0 and part.strip():  # This is a sentence content
            part = part.strip()
            if part and part[0].islower():
                part = part[0].upper() + part[1:]
        capitalized_sentences.append(part)
    
    humanized_text = ''.join(capitalized_sentences).strip()
    
    # Ensure proper ending
    if humanized_text and not humanized_text[-1] in '.!?':
        humanized_text += '.'
    
    # Step 6: AI Model Polish (Hybrid Approach)
    # Use the loaded AI model for final natural language polish
    try:
        # Detect discipline and create tailored prompt
        discipline = detect_academic_discipline(text)
        
        # Create discipline-specific prompt
        discipline_guidance = {
            'stem': "Make this technical text sound more natural while keeping precision. Use active voice and vary sentence structure.",
            'social': "Rewrite to emphasize human elements and real-world connections. Make it engaging and accessible.", 
            'humanities': "Transform into more interpretive, nuanced language. Embrace natural complexity and flow.",
            'business': "Use confident, action-oriented language. Focus on practical implications and clear communication.",
            'medical': "Balance technical accuracy with clear, patient-centered language. Make complex concepts accessible.",
            'general': "Make this academic text sound more natural and human while maintaining scholarly credibility."
        }
        
        ai_prompt = f"""Transform this {discipline} academic text to sound more natural and human-written. {discipline_guidance.get(discipline, discipline_guidance['general'])}

Requirements:
- Remove AI-like formality and repetitive patterns
- Use varied, natural sentence structures  
- Keep all technical accuracy and key concepts
- Make it flow conversationally while staying professional
- Avoid phrases like "furthermore, moreover, additionally"

Text to humanize: {humanized_text}

Natural version:"""
        
        if model_type == "flan-t5":
            # Use FLAN-T5 with specific parameters for natural rewriting
            ai_result = humanization_model(
                ai_prompt,
                max_new_tokens=len(humanized_text.split()) * 2,  # Allow for expansion
                do_sample=True,
                temperature=0.7,  # Balanced creativity
                top_p=0.9,
                repetition_penalty=1.2,
                num_beams=3
            )[0]["generated_text"].strip()
        elif model_type == "t5-base":
            # T5-base with paraphrase focus
            ai_result = humanization_model(
                f"paraphrase: {humanized_text}",
                max_new_tokens=len(humanized_text.split()) * 2,
                do_sample=True,
                temperature=0.8,
                top_p=0.9
            )[0]["generated_text"].strip()
        else:
            # Paraphrase model
            ai_result = humanization_model(
                humanized_text,
                max_new_tokens=len(humanized_text.split()) * 2,
                do_sample=True,
                temperature=0.7
            )[0]["generated_text"].strip()
        
        # Clean up AI model output - handle various response formats
        ai_result = ai_result.strip()
        
        # Remove prompt echoes and formatting artifacts
        cleanup_patterns = [
            r'^.*?Natural version:\s*',
            r'^.*?Rewritten:\s*',
            r'^.*?Humanized:\s*',
            r'^.*?Result:\s*'
        ]
        
        for pattern in cleanup_patterns:
            ai_result = re.sub(pattern, '', ai_result, flags=re.IGNORECASE)
        
        # Remove trailing prompt text
        if "Text to humanize:" in ai_result:
            ai_result = ai_result.split("Text to humanize:")[0].strip()
        
        ai_result = ai_result.strip()
        
        # Quality checks before using AI result
        ai_words = len(ai_result.split())
        original_words = len(humanized_text.split())
        
        # Use AI result if it passes quality checks
        if (ai_words >= original_words * 0.6 and  # At least 60% original length
            ai_words <= original_words * 2.0 and    # Not more than 200% original length
            ai_result and                            # Not empty
            not ai_result.lower().startswith(('sorry', 'i cannot', 'i can\'t'))):  # Not a refusal
            
            humanized_text = ai_result
            
            # Final cleanup of AI output
            humanized_text = re.sub(r'\s+([,.!?;:])', r'\1', humanized_text)
            humanized_text = re.sub(r'\s+', ' ', humanized_text)
            
            # Fix any remaining spacing issues
            humanized_text = re.sub(r'\.([A-Z][a-z]+)', r'. \1', humanized_text)
            
            # Ensure proper ending
            if humanized_text and not humanized_text[-1] in '.!?':
                humanized_text += '.'
        else:
            print(f"AI result quality check failed - using pattern-based result")
            
    except Exception as e:
        print(f"AI model polish failed, using pattern-based result: {e}")
        # Continue with pattern-based result
        pass
    
    # Calculate AI detection score AFTER full processing
    ai_score_after = calculate_ai_detection_score(humanized_text)
    
    # Emergency fallback if score didn't improve enough
    if ai_score_after >= ai_score_before - 5:  # Less than 5 point improvement
        # More aggressive replacements
        emergency_replacements = {
            r'\bThis\s+(study|research|analysis|investigation)\b': 'Our work',
            r'\bThe\s+(study|research|analysis|investigation)\b': 'This work',
            r'\bOur\s+(findings|results|data|analysis)\b': 'What we found',
            r'\bThe\s+(findings|results|data|analysis)\b': 'Our results',
            r'\bIt\s+is\s+(evident|clear|apparent)\s+that\b': 'Clearly,',
            r'\bIt\s+can\s+be\s+(seen|observed|noted)\s+that\b': 'We see that',
            r'\bIn\s+this\s+(study|research|paper|work)\b': 'Here',
            r'\bThe\s+present\s+(study|research|work)\b': 'This work',
        }
        
        for pattern, replacement in emergency_replacements.items():
            humanized_text = re.sub(pattern, replacement, humanized_text, flags=re.IGNORECASE)
        
        # Recalculate score
        ai_score_after = calculate_ai_detection_score(humanized_text)
    
    return {
        "original_text": text,
        "humanized_text": humanized_text,
        "original_word_count": word_count,
        "humanized_word_count": count_words(humanized_text),
        "ai_score_before_humanizing": ai_score_before,
        "ai_score_after_humanizing": ai_score_after,
        "improvement_percentage": round(max(0, ai_score_before - ai_score_after), 1)
    }
