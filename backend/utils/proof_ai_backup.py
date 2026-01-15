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
        r'\b\d+\.?\d*[°℃℉]\b',  # Temperature/degree measurements
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
        'multidisciplinary approach', 'rigorous oversight', 'policy frameworks'
    ]
    
    # Count AI phrases with penalty
    ai_phrase_count = sum(1 for phrase in strong_ai_phrases if phrase in text.lower())
    ai_indicators += ai_phrase_count * 8  # Reduced penalty
    
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
    
    # More reasonable base score
    base_score = 30 + (abs(hash(text[:30])) % 20)  # 30-50 base range
    total_score = min(base_score + ai_indicators, 95)
    
    return round(total_score, 1)

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

def proofread_text(text: str) -> dict:
    """
    Simplified but effective humanization system focused on reducing AI patterns.
    """
    word_count = count_words(text)
    
    if not (50 <= word_count <= 1500):
        raise ValueError(f"Input text must be between 50 and 1500 words. Current word count: {word_count}")

    # Calculate AI detection score BEFORE humanization
    ai_score_before = calculate_ai_detection_score(text)
    
    # Direct pattern replacement (most effective approach)
    humanized_text = text
    
    # Step 1: Replace common AI phrases with more natural alternatives
    ai_phrase_replacements = {
        r'\bit is important to note that\b': 'notably,',
        r'\bit should be noted that\b': 'worth mentioning,',
        r'\bit is worth mentioning that\b': 'importantly,',
        r'\bfurthermore,?\s*': 'also, ',
        r'\bmoreover,?\s*': 'what\'s more, ',
        r'\badditionally,?\s*': 'plus, ',
        r'\bconsequently,?\s*': 'as a result, ',
        r'\btherefore,?\s*': 'so ',
        r'\bin conclusion,?\s*': 'ultimately, ',
        r'\bto summarize,?\s*': 'in short, ',
        r'\bin summary,?\s*': 'overall, ',
        r'\bthis study demonstrates\b': 'research reveals',
        r'\bresearch shows\b': 'studies find',
        r'\bstudies indicate\b': 'evidence suggests',
        r'\bit can be concluded\b': 'we can see',
        r'\bthe results suggest\b': 'findings show',
        r'\bevidence indicates\b': 'data shows',
        r'\bsignificantly transformed\b': 'greatly changed',
        r'\bcritical concerns\b': 'key issues',
        r'\bongoing research\b': 'current studies',
        r'\bmultidisciplinary approach\b': 'interdisciplinary method',
        r'\brigorous oversight\b': 'careful monitoring',
        r'\bpolicy frameworks\b': 'policy structures'
    }
    
    # Apply replacements
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
    
    # Step 3: Replace academic buzzwords with simpler alternatives
    buzzword_replacements = {
        r'\bsignificantly\b': 'notably',
        r'\bsubstantially\b': 'considerably', 
        r'\bfundamentally\b': 'basically',
        r'\bcomprehensively\b': 'thoroughly',
        r'\bextensively\b': 'widely',
        r'\bremarkably\b': 'surprisingly',
        r'\bdemonstrates\b': 'shows',
        r'\bindicates\b': 'suggests',
        r'\breveals\b': 'shows',
        r'\bestablishes\b': 'proves'
    }
    
    for pattern, replacement in buzzword_replacements.items():
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
    
    # Calculate AI detection score AFTER humanization
    ai_score_after = calculate_ai_detection_score(humanized_text)
    
    # If still too AI-like, apply emergency fixes
    if ai_score_after >= ai_score_before:
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
            def __init__(self, text):
                self.text = text
                self.used_replacements = set()
                self.context_memory = {}
                self.sentence_count = len(re.split(r'[.!?]+', text))
                
            def get_contextual_replacement(self, category, options, context_key):
                """Get replacement based on context and avoid repetition"""
                # Create unique context key
                full_key = f"{category}_{context_key}_{len(self.used_replacements)}"
                
                # Filter out recently used options
                available_options = [opt for opt in options if opt not in self.used_replacements]
                if not available_options:
                    available_options = options  # Reset if all used
                    self.used_replacements.clear()
                
                # Use hash of context for consistent but varied selection
                hash_input = f"{full_key}_{self.sentence_count}"
                selected = available_options[hash(hash_input) % len(available_options)]
                
                self.used_replacements.add(selected)
                self.context_memory[category] = selected
                
                return selected
            
            def smart_transition_replacement(self, match, sentence_position):
                """Context-aware transition word replacement"""
                matched_text = match.group().lower().strip(' ,')
                
                # Different replacements based on sentence position
                if sentence_position == 0:  # First sentence
                    options = {
                        'furthermore': ['To begin with,', 'Initially,', 'First,', 'To start,'],
                        'moreover': ['Additionally,', 'Furthermore,', 'What\'s more,', 'Beyond this,'],
                        'however': ['Yet', 'But', 'Still,', 'Nevertheless,'],
                        'additionally': ['Also,', 'Furthermore,', 'Plus,', 'Moreover,'],
                    }
                elif sentence_position < self.sentence_count * 0.3:  # Early sentences
                    options = {
                        'furthermore': ['Additionally,', 'Also,', 'Beyond that,', 'What\'s more,'],
                        'moreover': ['Furthermore,', 'In addition,', 'Additionally,', 'Plus,'],
                        'however': ['Yet', 'But', 'Still,', 'On the other hand,'],
                        'additionally': ['Moreover,', 'Furthermore,', 'Also,', 'Plus,'],
                    }
                elif sentence_position > self.sentence_count * 0.7:  # Late sentences
                    options = {
                        'furthermore': ['Finally,', 'Ultimately,', 'In conclusion,', 'Lastly,'],
                        'moreover': ['Ultimately,', 'Finally,', 'In the end,', 'Overall,'],
                        'however': ['Nevertheless,', 'Despite this,', 'Even so,', 'Yet'],
                        'additionally': ['Finally,', 'Lastly,', 'To conclude,', 'Overall,'],
                    }
                else:  # Middle sentences
                    options = {
                        'furthermore': ['Additionally,', 'Moreover,', 'Also,', 'Beyond that,'],
                        'moreover': ['Furthermore,', 'Additionally,', 'What\'s more,', 'Plus,'],
                        'however': ['Yet', 'But', 'Still,', 'Nevertheless,'],
                        'additionally': ['Also,', 'Furthermore,', 'Moreover,', 'Plus,'],
                    }
                
                return self.get_contextual_replacement('transition', 
                                                    options.get(matched_text, ['Additionally,']), 
                                                    f"{matched_text}_{sentence_position}")
        
        replacer = AdvancedReplacer(result3)
        
        # Advanced pattern-based replacements with context awareness
        advanced_patterns = {
            # Sophisticated transition handling
            r'\b(furthermore|moreover|additionally|however|nevertheless)\s*,?\s*': {
                'type': 'transition',
                'handler': lambda m, pos: replacer.smart_transition_replacement(m, pos) + ' '
            },
            
            # Academic formality patterns with natural alternatives
            r'\b(it is important to note that|it should be noted that|it is worth mentioning that)\s*': {
                'type': 'formality',
                'options': [
                    'Notably,', 'Worth noting:', 'Importantly,', 'Keep in mind:',
                    'Interestingly,', 'Note that', 'Crucially,', 'Significantly,',
                    'What\'s important:', 'Consider this:', 'Bear in mind:', 'Remarkably,'
                ]
            },
            
            # Research language with disciplinary variation
            r'\b(research shows|studies indicate|evidence suggests|data reveals|findings demonstrate)\s+that\s*': {
                'type': 'research',
                'options': [
                    'Studies reveal', 'Research indicates', 'Evidence points to', 'Data shows',
                    'Findings suggest', 'Analysis reveals', 'Investigation shows', 'Results indicate',
                    'Examination demonstrates', 'Observations suggest', 'Inquiry reveals', 'Assessment shows'
                ]
            },
            
            # Quantifier sophistication
            r'\b(significantly|considerably|substantially|markedly|notably)\s+': {
                'type': 'quantifier',
                'options': [
                    'dramatically', 'substantially', 'considerably', 'markedly',
                    'notably', 'significantly', 'profoundly', 'extensively',
                    'meaningfully', 'distinctly', 'observably', 'measurably'
                ]
            },
            
            # Causation and conclusion patterns
            r'\b(as a result|consequently|therefore|thus|hence)\s*,?\s*': {
                'type': 'causation',
                'options': [
                    'As a result,', 'Consequently,', 'Therefore,', 'This means',
                    'Hence,', 'Thus,', 'Given this,', 'In response,',
                    'Accordingly,', 'For this reason,', 'Because of this,', 'Subsequently,'
                ]
            },
            
            # Academic hedging language
            r'\b(it appears that|it seems that|it is likely that|it is possible that)\s*': {
                'type': 'hedging',
                'options': [
                    'Apparently,', 'Seemingly,', 'Likely,', 'Possibly,',
                    'Presumably,', 'Evidently,', 'Ostensibly,', 'Conceivably,',
                    'Probably,', 'Potentially,', 'Perhaps', 'Maybe'
                ]
            },
            
            # Emphasis and importance markers
            r'\b(critically|crucially|essentially|fundamentally|primarily)\s+': {
                'type': 'emphasis',
                'options': [
                    'critically', 'crucially', 'essentially', 'fundamentally',
                    'primarily', 'chiefly', 'mainly', 'principally',
                    'predominantly', 'largely', 'mostly', 'generally'
                ]
            }
        }
        
        # Apply advanced patterns with position awareness
        sentences = re.split(r'([.!?]+)', result3)
        processed_sentences = []
        
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i]
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ''
            
            sentence_position = i // 2
            
            for pattern, config in advanced_patterns.items():
                if config['type'] == 'transition':
                    # Use position-aware handler
                    sentence = re.sub(pattern, 
                                    lambda m: config['handler'](m, sentence_position), 
                                    sentence, flags=re.IGNORECASE)
                else:
                    # Use contextual replacement
                    def contextual_replace(match):
                        return replacer.get_contextual_replacement(
                            config['type'], 
                            config['options'], 
                            f"{match.group()}_{sentence_position}"
                        ) + ' '
                    
                    sentence = re.sub(pattern, contextual_replace, sentence, flags=re.IGNORECASE)
            
            processed_sentences.append(sentence + punctuation)
        
        result3 = ''.join(processed_sentences)
        
        # Advanced sentence variation post-processing
        result3 = re.sub(r'\s+', ' ', result3)  # Clean up spacing
        result3 = re.sub(r'\s+([,.!?])', r'\1', result3)  # Fix punctuation spacing
        
        result3 = restore_academic_elements(result3, preserved_elements)
        humanized_versions.append(result3)
        
    except Exception as e:
        print(f"Strategy 3 failed: {e}")
    
    # Advanced version selection with multi-criteria scoring
    def evaluate_version_quality(version, original):
        """Comprehensive quality evaluation"""
        if not version or len(version.split()) < word_count * 0.6:
            return -1000  # Reject too-short versions
        
        ai_score = calculate_ai_detection_score(version)
        
        # Semantic preservation check
        original_words = set(re.findall(r'\b\w+\b', original.lower()))
        version_words = set(re.findall(r'\b\w+\b', version.lower()))
        
        # Key term preservation (important academic concepts should remain)
        key_terms_preserved = len(original_words & version_words) / len(original_words) if original_words else 0
        
        # Length appropriateness (not too short or too long)
        length_ratio = len(version.split()) / word_count
        length_penalty = abs(1 - length_ratio) * 10 if length_ratio < 0.8 or length_ratio > 1.3 else 0
        
        # Sentence variety (avoid uniform lengths)
        sentences = [s.strip() for s in re.split(r'[.!?]+', version) if s.strip()]
        if len(sentences) > 1:
            sentence_lengths = [len(s.split()) for s in sentences]
            avg_len = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((l - avg_len) ** 2 for l in sentence_lengths) / len(sentence_lengths)
            variety_bonus = min(variance / 10, 5)  # Reward sentence variety
        else:
            variety_bonus = 0
        
        # Academic vocabulary retention
        academic_terms = ['research', 'study', 'analysis', 'investigation', 'examination', 
                         'methodology', 'findings', 'results', 'conclusion', 'evidence']
        academic_retention = sum(1 for term in academic_terms if term in version.lower()) * 2
        
        # Calculate composite score (lower is better for AI detection, but we want balanced quality)
        quality_score = (
            -ai_score * 2 +  # Primary: minimize AI detection (negative because lower is better)
            key_terms_preserved * 30 +  # Preserve meaning
            variety_bonus +  # Reward sentence variety
            academic_retention +  # Keep academic tone
            -length_penalty  # Penalize inappropriate length
        )
        
        return quality_score
    
    # Evaluate all versions
    version_scores = []
    for i, version in enumerate(humanized_versions):
        score = evaluate_version_quality(version, text)
        ai_detection = calculate_ai_detection_score(version) if version else 999
        version_scores.append((version, score, ai_detection, i))
    
    # Sort by quality score (higher is better)
    version_scores.sort(key=lambda x: x[1], reverse=True)
    
    best_result = text  # Fallback
    best_score = ai_score_before
    
    if version_scores and version_scores[0][1] > -500:  # Has acceptable quality
        best_result = version_scores[0][0]
        best_score = version_scores[0][2]
    
    # Multi-pass refinement for optimal results
    def final_polish(text_input):
        """Final polishing pass with micro-improvements"""
        result = text_input
        
        # Ensure natural flow between sentences
        sentences = re.split(r'([.!?]+)', result)
        polished = []
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i].strip()
            punctuation = sentences[i+1] if i+1 < len(sentences) else ''
            
            if sentence:
                # Micro-adjustments for natural flow
                
                # Avoid starting consecutive sentences the same way
                if i > 0 and len(polished) >= 2:
                    prev_sentence = polished[-2]
                    if (sentence.split()[0].lower() == prev_sentence.split()[0].lower() 
                        and len(sentence.split()) > 2):
                        # Rephrase beginning slightly
                        words = sentence.split()
                        if words[0].lower() in ['the', 'this', 'these', 'such']:
                            alternatives = {'the': 'Such', 'this': 'The', 'these': 'Such', 'such': 'These'}
                            sentence = f"{alternatives.get(words[0].lower(), words[0])} {' '.join(words[1:])}"
                
                # Ensure proper capitalization
                if not sentence[0].isupper():
                    sentence = sentence[0].upper() + sentence[1:]
                
                # Natural contractions where appropriate (but keep academic tone)
                if 'it is' in sentence and len(sentence.split()) < 10:
                    sentence = sentence.replace(' it is ', " it's ")
                
                polished.append(sentence)
                polished.append(punctuation)
        
        result = ''.join(polished)
        
        # Final cleanup passes
        result = re.sub(r'\s+([,.!?;:])', r'\1', result)  # Fix punctuation spacing
        result = re.sub(r'([,.!?;:])\s*([,.!?;:])', r'\1\2', result)  # Remove double punctuation
        result = re.sub(r'\s+', ' ', result)  # Normalize whitespace
        result = re.sub(r'^[^A-Z]*', lambda m: m.group().capitalize(), result)  # Ensure capitalized start
        
        # Ensure proper ending
        if result and not result[-1] in '.!?':
            result += '.'
        
        return result.strip()
    
    # Apply final polish
    final_result = final_polish(best_result)
    
    # One final check - if still too AI-like, apply emergency humanization
    preliminary_score = calculate_ai_detection_score(final_result)
    
    if preliminary_score > 50:  # Still too AI-like
        # Emergency pattern replacement
        emergency_fixes = {
            r'\bsignificantly\b': 'notably',
            r'\bconsiderably\b': 'substantially', 
            r'\bfundamentally\b': 'essentially',
            r'\bprimarily\b': 'mainly',
            r'\badditionally\b': 'also',
            r'\bconsequently\b': 'as a result',
            r'\btherefore\b': 'so',
        }
        
        for pattern, replacement in emergency_fixes.items():
            final_result = re.sub(pattern, replacement, final_result, count=1, flags=re.IGNORECASE)
    
    # Calculate final AI detection score
    ai_score_after = calculate_ai_detection_score(final_result)
    
    return {
        "original_text": text,
        "humanized_text": final_result,
        "original_word_count": word_count,
        "humanized_word_count": count_words(final_result),
        "ai_score_before_humanizing": ai_score_before,
        "ai_score_after_humanizing": ai_score_after,
        "improvement_percentage": round(max(0, ai_score_before - ai_score_after), 1)
    }
