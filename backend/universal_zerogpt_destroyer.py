#!/usr/bin/env python3

import re

def get_universal_zerogpt_destroyers():
    """
    Universal ZeroGPT destroyer patterns that work across ALL text types.
    Generalized from the proven 0% success case to handle any domain.
    """
    return {
        # MEGA ZEROGPT TRIGGERS - Academic/Formal Language (Universal)
        'mega_formal_eliminators': {
            # Universal formal sentence starters (ZeroGPT red flags)
            r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+\([A-Z]+\)\s+has revolutionized\b': r'\2 has changed',
            r'\bhas revolutionized modern society\b': 'has changed how we live',
            r'\bhas transformed the landscape of\b': 'has changed',
            r'\bhas emerged as a dominant force\b': 'has become important',
            r'\bhas become increasingly important\b': 'is getting more important',
            r'\bplays a crucial role in\b': 'is important for',
            r'\bserves as a fundamental component\b': 'is a key part',
            
            # Universal academic discourse markers
            r'\bCentral among these is the issue of\b': 'The main problem is',
            r'\bAnother significant concern lies in\b': 'Another worry is',
            r'\bA key challenge involves\b': 'A big problem is',
            r'\bOf particular importance is\b': 'What\'s really important is',
            r'\bIt is worth noting that\b': 'It\'s worth saying that',
            r'\bIt should be emphasized that\b': 'We should point out that',
            r'\bIt is important to recognize that\b': 'We need to see that',
            
            # Universal formal conclusions
            r'\bUltimately, (.+) is not solely about\b': r'In the end, \1 isn\'t just about',
            r'\bIn conclusion, (.+) represents\b': r'To wrap up, \1 is',
            r'\bTo summarize, (.+) requires\b': r'In short, \1 needs',
            r'\bIn summary, (.+) demonstrates\b': r'Basically, \1 shows',
            
            # Universal process language
            r'\brequires a multi-stakeholder approach involving\b': 'needs different people working together like',
            r'\bdemands a comprehensive strategy that encompasses\b': 'needs a complete plan that includes',
            r'\bnecessitates careful consideration of\b': 'needs us to think carefully about',
            r'\binvolves the systematic evaluation of\b': 'means looking carefully at',
            
            # Universal goal/outcome language
            r'\bThe goal is to establish (.+) that promote\b': r'We want to make \1 that help',
            r'\bThe objective is to develop (.+) that ensure\b': r'We\'re trying to build \1 that make sure',
            r'\bThe aim is to create (.+) that facilitate\b': r'We want to create \1 that help',
            r'\bThe purpose is to implement (.+) that enhance\b': r'We\'re trying to put in place \1 that improve',
        },
        
        # UNIVERSAL VOCABULARY DESTROYERS
        'vocabulary_destroyers': {
            # Universal formal verbs → casual
            r'\bdemonstrates?\b': 'shows',
            r'\billustrates?\b': 'shows',
            r'\bexemplifies?\b': 'shows',
            r'\bfacilitates?\b': 'helps',
            r'\benables?\b': 'lets',
            r'\butilizes?\b': 'uses',
            r'\bemploys?\b': 'uses',
            r'\bimplements?\b': 'puts in place',
            r'\bestablishes?\b': 'sets up',
            r'\bmaintains?\b': 'keeps',
            r'\benhances?\b': 'improves',
            r'\boptimizes?\b': 'makes better',
            r'\bmaximizes?\b': 'makes the most of',
            r'\bminimizes?\b': 'reduces',
            r'\bevaluates?\b': 'checks',
            r'\bassesses?\b': 'looks at',
            r'\bexamines?\b': 'studies',
            r'\banalyzes?\b': 'looks at',
            r'\binvestigates?\b': 'looks into',
            r'\bexplores?\b': 'checks out',
            r'\baddresses?\b': 'deals with',
            r'\btackles?\b': 'deals with',
            
            # Universal formal adjectives → casual
            r'\bcomprehensive\b': 'complete',
            r'\bextensive\b': 'big',
            r'\bsubstantial\b': 'large',
            r'\bsignificant\b': 'important',
            r'\bconsiderable\b': 'big',
            r'\bnotable\b': 'worth mentioning',
            r'\bremarkable\b': 'amazing',
            r'\bexceptional\b': 'really good',
            r'\bextraordinary\b': 'incredible',
            r'\bprofound\b': 'deep',
            r'\bsubtle\b': 'small',
            r'\bnuanced\b': 'detailed',
            r'\bintricate\b': 'complex',
            r'\bsophisticated\b': 'advanced',
            r'\brobust\b': 'strong',
            r'\beffective\b': 'good',
            r'\befficient\b': 'quick',
            r'\boptimal\b': 'best',
            r'\bideal\b': 'perfect',
            r'\bcrucial\b': 'key',
            r'\bessential\b': 'needed',
            r'\bvital\b': 'important',
            r'\bfundamental\b': 'basic',
            r'\bcritical\b': 'important',
            r'\bimperative\b': 'necessary',
            
            # Universal formal nouns → casual  
            r'\bmethodology\b': 'way',
            r'\bapproach\b': 'way',
            r'\bstrategy\b': 'plan',
            r'\bframework\b': 'structure',
            r'\bparadigm\b': 'model',
            r'\bperspective\b': 'view',
            r'\bviewpoint\b': 'opinion',
            r'\bstandpoint\b': 'position',
            r'\bcapabilities\b': 'abilities',
            r'\bfunctionality\b': 'features',
            r'\bperformance\b': 'results',
            r'\beffectiveness\b': 'how well it works',
            r'\befficiency\b': 'speed',
            r'\bimplementation\b': 'putting it to work',
            r'\bdeployment\b': 'use',
            r'\butilization\b': 'use',
            r'\bapplication\b': 'use',
            r'\bchallenges?\b': 'problems',
            r'\bdifficulties\b': 'problems',
            r'\bobstacles\b': 'problems',
            r'\bbarriers\b': 'blocks',
            r'\bopportunities\b': 'chances',
            r'\badvantages\b': 'good things',
            r'\bbenefits\b': 'good things',
            r'\bimplications\b': 'effects',
            r'\bconsequences\b': 'results',
            r'\boutcomes\b': 'results',
            r'\bramifications\b': 'effects',
        },
        
        # UNIVERSAL FORMAL PHRASE DESTROYERS
        'phrase_destroyers': {
            # Universal formal connectors → casual
            r'\bFurthermore,\b': 'Plus,',
            r'\bMoreover,\b': 'Also,',
            r'\bAdditionally,\b': 'And',
            r'\bIn addition,\b': 'Also,',
            r'\bHowever,\b': 'But',
            r'\bNevertheless,\b': 'Still,',
            r'\bNonetheless,\b': 'Still,',
            r'\bConsequently,\b': 'So',
            r'\bTherefore,\b': 'So',
            r'\bThus,\b': 'So',
            r'\bHence,\b': 'So',
            r'\bAccordingly,\b': 'So',
            r'\bSubsequently,\b': 'Then,',
            r'\bEventually,\b': 'Later,',
            r'\bUltimately,\b': 'In the end,',
            r'\bFinally,\b': 'Finally,',
            r'\bInitially,\b': 'First,',
            r'\bOriginally,\b': 'At first,',
            r'\bPrimarily,\b': 'Mainly,',
            r'\bEssentially,\b': 'Basically,',
            r'\bFundamentally,\b': 'Basically,',
            
            # Universal formal phrases → casual
            r'\bin order to\b': 'to',
            r'\bso as to\b': 'to',
            r'\bwith the purpose of\b': 'to',
            r'\bwith the aim of\b': 'to',
            r'\bwith the goal of\b': 'to',
            r'\bwith regard to\b': 'about',
            r'\bwith respect to\b': 'about',
            r'\bin relation to\b': 'about',
            r'\bin connection with\b': 'about',
            r'\bin terms of\b': 'when it comes to',
            r'\bfrom the perspective of\b': 'looking at it from',
            r'\bin the context of\b': 'when looking at',
            r'\bin the framework of\b': 'within',
            r'\bin accordance with\b': 'following',
            r'\bin compliance with\b': 'following',
            r'\bas a result of\b': 'because of',
            r'\bdue to the fact that\b': 'because',
            r'\bowing to the fact that\b': 'because',
            r'\bin light of the fact that\b': 'because',
            r'\bgiven that\b': 'since',
            r'\bconsidering that\b': 'since',
            
            # Universal academic hedging → direct
            r'\bit appears that\b': 'it seems like',
            r'\bit seems that\b': 'it looks like',
            r'\bit would appear that\b': 'it seems like',
            r'\bone might argue that\b': 'some people think',
            r'\bit could be argued that\b': 'you could say',
            r'\bit is possible that\b': 'maybe',
            r'\bit is likely that\b': 'probably',
            r'\bit is probable that\b': 'probably',
            r'\bthere is evidence to suggest\b': 'it looks like',
            r'\bstudies indicate that\b': 'research shows',
            r'\bresearch suggests that\b': 'studies show',
            r'\bfindings demonstrate that\b': 'results show',
        },
        
        # UNIVERSAL CASUAL INJECTION PATTERNS
        'casual_injectors': [
            "You know what?", "I mean,", "Look,", "Listen,", "Honestly,", 
            "Really,", "Actually,", "Plus,", "And yeah,", "But hey,", 
            "So basically,", "Well,", "Anyway,", "The thing is,", "Here's the deal,"
        ],
        
        # UNIVERSAL CONTRACTION PATTERNS
        'universal_contractions': {
            r'\bdo not\b': "don't",
            r'\bdoes not\b': "doesn't", 
            r'\bdid not\b': "didn't",
            r'\bcannot\b': "can't",
            r'\bcould not\b': "couldn't",
            r'\bshould not\b': "shouldn't",
            r'\bwould not\b': "wouldn't", 
            r'\bwill not\b': "won't",
            r'\bis not\b': "isn't",
            r'\bare not\b': "aren't",
            r'\bwas not\b': "wasn't",
            r'\bwere not\b': "weren't",
            r'\bhas not\b': "hasn't",
            r'\bhave not\b': "haven't",
            r'\bhad not\b': "hadn't",
            r'\bI am\b': "I'm",
            r'\byou are\b': "you're",
            r'\bwe are\b': "we're",
            r'\bthey are\b': "they're",
            r'\bit is\b': "it's",
            r'\bthat is\b': "that's",
            r'\bwho is\b': "who's",
            r'\bwhere is\b': "where's",
            r'\bwhen is\b': "when's",
            r'\bwhat is\b': "what's",
            r'\bhow is\b': "how's",
            r'\bI will\b': "I'll",
            r'\byou will\b': "you'll", 
            r'\bwe will\b': "we'll",
            r'\bthey will\b': "they'll",
            r'\bI have\b': "I've",
            r'\byou have\b': "you've",
            r'\bwe have\b': "we've",
            r'\bthey have\b': "they've",
            r'\bI would\b': "I'd",
            r'\byou would\b': "you'd",
            r'\bwe would\b': "we'd",
            r'\bthey would\b': "they'd",
        }
    }

def apply_universal_zerogpt_destroyer(text: str, iteration: int = 0) -> str:
    """
    Apply universal ZeroGPT destroyer patterns that work for ANY text type.
    Based on proven 0% success techniques but generalized for robustness.
    """
    destroyers = get_universal_zerogpt_destroyers()
    humanized = text
    
    # PHASE 1: Eliminate mega formal patterns
    for pattern, replacement in destroyers['mega_formal_eliminators'].items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # PHASE 2: Universal vocabulary destruction 
    for pattern, replacement in destroyers['vocabulary_destroyers'].items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # PHASE 3: Universal phrase destruction
    for pattern, replacement in destroyers['phrase_destroyers'].items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # PHASE 4: Maximum contractions
    for pattern, replacement in destroyers['universal_contractions'].items():
        humanized = re.sub(pattern, replacement, humanized, flags=re.IGNORECASE)
    
    # PHASE 5: Casual injection
    sentences = re.split(r'([.!?])', humanized)
    casual_sentences = []
    casual_markers = destroyers['casual_injectors']
    
    marker_index = 0
    for i, part in enumerate(sentences):
        if part.strip() and not part in '.!?':
            part = part.strip()
            
            # Add casual markers to key sentences (not every sentence)
            if i == 0:  # First sentence
                part = casual_markers[0] + " " + part.lower()
                marker_index = 1
            elif i % 6 == 0 and len(part.split()) > 8 and marker_index < len(casual_markers):
                # Add markers to longer sentences periodically
                part = casual_markers[marker_index] + " " + part.lower()
                marker_index = (marker_index + 1) % len(casual_markers)
            
            # Fix capitalization 
            if part and part[0].islower():
                first_letter_match = re.search(r'[a-z]', part)
                if first_letter_match:
                    pos = first_letter_match.start()
                    part = part[:pos] + part[pos].upper() + part[pos+1:]
            
            casual_sentences.append(part)
        elif part in '.!?':
            casual_sentences.append(part)
    
    humanized = ''.join(casual_sentences)
    
    # PHASE 6: Sentence structure breaking (for long formal sentences)
    sentences = re.split(r'([.!?])', humanized)
    broken_sentences = []
    
    for i, part in enumerate(sentences):
        if part.strip() and not part in '.!?':
            part = part.strip()
            words = part.split()
            
            # Break sentences longer than 20 words
            if len(words) > 20:
                # Find natural break points
                break_points = []
                for j, word in enumerate(words):
                    if word.lower() in ['and', 'but', 'so', 'plus', 'also', 'because', 'since', 'while', 'when', 'where', 'which']:
                        break_points.append(j)
                
                if break_points:
                    # Split at first good break point after 10 words
                    for bp in break_points:
                        if bp > 10:
                            first_part = ' '.join(words[:bp])
                            second_part = ' '.join(words[bp:])
                            part = first_part + '. ' + second_part.capitalize()
                            break
            
            broken_sentences.append(part)
        elif part in '.!?':
            broken_sentences.append(part)
    
    humanized = ''.join(broken_sentences)
    
    # PHASE 7: Final cleanup
    humanized = re.sub(r'—', '-', humanized)  # Em-dashes to hyphens
    humanized = re.sub(r';\s', ', ', humanized)  # Semicolons to commas  
    humanized = re.sub(r'\s+', ' ', humanized)  # Multiple spaces
    humanized = re.sub(r'\s+([,.!?;:])', r'\1', humanized)  # Space before punctuation
    humanized = re.sub(r'([,.!?;:])\s*([A-Z])', r'\1 \2', humanized)  # Space after punctuation
    
    return humanized.strip()

if __name__ == "__main__":
    # Test with different text types
    test_cases = [
        "Machine learning algorithms have revolutionized modern data processing methodologies.",
        "The implementation of blockchain technology demonstrates significant potential for enhancing security frameworks.",
        "Clinical trials indicate that the pharmaceutical intervention exhibits considerable therapeutic efficacy."
    ]
    
    print("🧪 UNIVERSAL ZEROGPT DESTROYER TEST")
    print("=" * 50)
    
    for i, text in enumerate(test_cases, 1):
        print(f"Test {i}: {text}")
        result = apply_universal_zerogpt_destroyer(text)
        print(f"Result: {result}")
        print()