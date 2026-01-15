#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re
from utils.proof_ai import count_words

def ultra_zerogpt_humanizer(text: str) -> str:
    """
    ULTRA AGGRESSIVE humanization specifically designed to beat ZeroGPT.
    Applies massive vocabulary replacement and casualization techniques.
    """
    humanized = text
    
    # PHASE 1: ULTRA AGGRESSIVE FORMAL WORD REPLACEMENT
    # ZeroGPT heavily penalizes these specific words
    ultra_formal_replacements = {
        # Core ZeroGPT triggers - MUST BE ELIMINATED
        r'\bubiquitous\b': 'everywhere',
        r'\bprofound\b': 'deep',
        r'\bmultifaceted\b': 'many-sided',  
        r'\bparadigm\b': 'model',
        r'\bholistic\b': 'complete',
        r'\bintricate\b': 'complex',
        r'\bnuanced\b': 'subtle',
        r'\bencompasses\b': 'includes',
        r'\bleverage\b': 'use',
        r'\boptimization\b': 'improvement',
        
        # Academic discourse markers
        r'\bfurthermore\b': 'also',
        r'\bmoreover\b': 'also', 
        r'\bnevertheless\b': 'still',
        r'\bconsequently\b': 'so',
        r'\btherefore\b': 'so',
        r'\bhowever\b': 'but',
        r'\badditionally\b': 'also',
        r'\bnotwithstanding\b': 'despite',
        
        # Method/process language
        r'\bmethodology\b': 'approach',
        r'\bframework\b': 'structure',
        r'\bimplementation\b': 'putting it to work',
        r'\bcomprehensive\b': 'complete',
        r'\bsubstantial\b': 'big',
        r'\bsignificant\b': 'important',
        
        # Action verbs
        r'\bfacilitate\b': 'help',
        r'\butilize\b': 'use',
        r'\bdemonstrate\b': 'show',
        r'\bestablish\b': 'set up',
        r'\bexamine\b': 'look at',
        r'\banalyze\b': 'study',
        r'\bevaluate\b': 'check',
        r'\bassess\b': 'look at',
        r'\bvalidate\b': 'prove',
        r'\bsubstantiate\b': 'back up',
        r'\bcorroborate\b': 'support',
        
        # Quality descriptors
        r'\boptimal\b': 'best',
        r'\brobust\b': 'strong',
        r'\binnovative\b': 'new',
        r'\bsophisticated\b': 'advanced',
        r'\beffective\b': 'good',
        r'\befficient\b': 'quick',
        r'\bcrucial\b': 'key',
        r'\bessential\b': 'needed',
        r'\bfundamental\b': 'basic',
        r'\bcritical\b': 'important',
        
        # Technical terms
        r'\balgorithm(s)?\b': 'computer program',
        r'\bdata science\b': 'working with data',
        r'\bmachine learning\b': 'AI systems',
        r'\bartificial intelligence\b': 'AI',
        r'\bpredictive analytics\b': 'predicting trends',
        
        # Formal phrases
        r'\bin order to\b': 'to',
        r'\bwith respect to\b': 'about',
        r'\bin terms of\b': 'when it comes to', 
        r'\baccording to\b': 'based on',
        r'\bin reference to\b': 'about',
        r'\bpertaining to\b': 'about',
        r'\bin the context of\b': 'when looking at',
        r'\bin the realm of\b': 'in the area of',
        r'\bwith regard to\b': 'about',
        
        # Research language
        r'\bThis study\b': 'This work',
        r'\bThe study\b': 'The work', 
        r'\bOur research\b': 'Our work',
        r'\bThe research\b': 'The work',
        r'\bThis analysis\b': 'This look',
        r'\bThe analysis\b': 'The look',
        
        # Data/information terms
        r'\bgathering information\b': 'collecting data',
        r'\bdata collection\b': 'getting data',
        r'\binformation gathering\b': 'data collection',
        r'\bdata acquisition\b': 'getting data',
    }
    
    # Apply formal replacements
    for pattern, replacement in ultra_formal_replacements.items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # PHASE 2: FORCE CONTRACTIONS (ZeroGPT heavily penalizes lack of contractions)
    contraction_map = {
        r'\bdo not\b': "don't",
        r'\bcannot\b': "can't", 
        r'\bwill not\b': "won't",
        r'\bis not\b': "isn't",
        r'\bare not\b': "aren't",
        r'\bhas not\b': "hasn't",
        r'\bhave not\b': "haven't",
        r'\bdoes not\b': "doesn't",
        r'\bwas not\b': "wasn't",
        r'\bwere not\b': "weren't", 
        r'\bshould not\b': "shouldn't",
        r'\bcould not\b': "couldn't",
        r'\bwould not\b': "wouldn't",
        r'\blet us\b': "let's",
        r'\bwe will\b': "we'll",
        r'\bthey will\b': "they'll",
        r'\byou will\b': "you'll",
        r'\bI will\b': "I'll",
        r'\bit will\b': "it'll",
        r'\bwe are\b': "we're",
        r'\bthey are\b': "they're",
        r'\byou are\b': "you're",
        r'\bI am\b': "I'm",
        r'\bit is\b': "it's",
        r'\bthat is\b': "that's",
        r'\bwhat is\b': "what's",
        r'\bwhere is\b': "where's",
        r'\bwhen is\b': "when's",
        r'\bwho is\b': "who's",
        r'\bhow is\b': "how's",
    }
    
    for pattern, replacement in contraction_map.items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # PHASE 3: INJECT CASUAL LANGUAGE 
    # Add casual words and phrases that ZeroGPT associates with human writing
    sentences = re.split(r'([.!?])', humanized)
    casual_sentences = []
    
    for i, part in enumerate(sentences):
        if part.strip() and not part in '.!?':
            part = part.strip()
            
            # Add casual starters to some sentences
            if i == 0:  # First sentence
                casual_starts = ["Actually, ", "Really, ", "Honestly, ", "Look, "]
                if len(part.split()) > 8:  # Only for longer sentences
                    part = casual_starts[0] + part.lower()
            elif i % 4 == 0 and len(part.split()) > 6:  # Every 4th sentence
                mid_casual = ["Plus, ", "Also, ", "And yeah, ", "But really, "]
                part = mid_casual[i % len(mid_casual)] + part.lower()
            
            # Fix capitalization after casual additions
            if part and part[0].islower():
                # Find the first letter and capitalize it
                first_letter_match = re.search(r'[a-z]', part)
                if first_letter_match:
                    pos = first_letter_match.start()
                    part = part[:pos] + part[pos].upper() + part[pos+1:]
            
            casual_sentences.append(part)
        elif part in '.!?':
            casual_sentences.append(part)
    
    humanized = ''.join(casual_sentences)
    
    # PHASE 4: SENTENCE VARIATION (ZeroGPT detects uniform structures)
    # Add varied sentence starters and connectors
    sentence_variations = {
        r'^The use of\b': 'Using',
        r'^The emergence of\b': 'The rise of',
        r'^The practice of\b': 'Doing',
        r'^The development of\b': 'Building',
        r'^The implementation of\b': 'Putting in place',
        r'^The establishment of\b': 'Setting up',
    }
    
    for pattern, replacement in sentence_variations.items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE | re.MULTILINE)
    
    # PHASE 5: FINAL CLEANUP AND CASUALIZATION
    # Replace remaining formal connectors
    final_cleanup = {
        r'\bUltimately,\b': 'In the end,',
        r'\bFundamentally,\b': 'Basically,',
        r'\bEssentially,\b': 'Basically,',
        r'\bPrimarily,\b': 'Mainly,',
        r'\bPredominantly,\b': 'Mostly,',
        r'\bSubsequently,\b': 'Then,',
        r'\bInitially,\b': 'First,',
        r'\bEventually,\b': 'Later,',
        r' — ': ' - ',  # Replace em-dashes with regular hyphens
        r';\s': ', ',   # Replace semicolons with commas
    }
    
    for pattern, replacement in final_cleanup.items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # Clean up spacing
    humanized = re.sub(r'\s+', ' ', humanized)
    humanized = re.sub(r'\s+([,.!?;:])', r'\1', humanized)  
    humanized = re.sub(r'([,.!?;:])\s*([A-Z])', r'\1 \2', humanized)
    
    return humanized.strip()

if __name__ == "__main__":
    # Test the ultra humanizer
    test_text = """In the era of ubiquitous data, working with data has become a dominant force shaping decisions across healthcare, finance, education, and governance. but the same analytical power that enables insight also raises profound ethical concerns. The use of computer programs to steps and interpret data introduces biases that can reinforce social inequities if not properly addressed. Data scientists must so adopt frameworks that emphasize transparency, accountability, and fairness in model development. Ethical gathering information practices are equally critical, as individuals' privacy and consent remain foundational to trust in data systems. what's more explainability in artificial intelligence is essential to ensure that automated decisions can be understood, challenged, and improved. The emergence of data ethics as a discipline highlights the need for interdisciplinary collaboration, bringing together technologists, ethicists, and policymakers to show standards that protect human dignity while enabling innovation. Ultimately, the ethical practice of working with data demands not only technical excellence but also moral responsibility — a commitment to ensuring that data-driven insights serve humanity rather than exploit it."""
    
    print("🎯 ULTRA ZEROGPT HUMANIZER TEST")
    print("=" * 50)
    print("Original (ZeroGPT: 76.66%):")
    print(f"{test_text[:100]}...")
    print()
    
    # Apply ultra humanization
    ultra_humanized = ultra_zerogpt_humanizer(test_text)
    
    print("🚀 ULTRA HUMANIZED RESULT:")
    print("=" * 30)
    print(ultra_humanized)
    print()
    print("🔍 KEY TRANSFORMATIONS:")
    print("- 'ubiquitous' → 'everywhere'")
    print("- 'profound' → 'deep'")
    print("- 'computer programs' → already casual")
    print("- 'gathering information' → 'collecting data'") 
    print("- 'what's more' → added casual connector")
    print("- 'Ultimately' → 'In the end'")
    print("- Added contractions and casual starters")
    print("- Removed formal academic language")
    print()
    print("📊 Word count:", count_words(ultra_humanized))
    print("🎯 This should score MUCH lower on ZeroGPT!")
    