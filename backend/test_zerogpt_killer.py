#!/usr/bin/env python3

from utils.proof_ai import proofread_text

def test_zerogpt_beating():
    """Test the enhanced system against ZeroGPT-style detection."""
    
    # Your original text that ZeroGPT rated as 100% AI
    test_text = """In the era of ubiquitous data, data science has become a dominant force shaping decisions across healthcare, finance, education, and governance. However, the same analytical power that enables insight also raises profound ethical concerns. The use of algorithms to process and interpret data introduces biases that can reinforce social inequities if not properly addressed. Data scientists must therefore adopt frameworks that emphasize transparency, accountability, and fairness in model development. Ethical data collection practices are equally critical, as individuals' privacy and consent remain foundational to trust in data systems. Moreover, explainability in artificial intelligence is essential to ensure that automated decisions can be understood, challenged, and improved. The emergence of data ethics as a discipline highlights the need for interdisciplinary collaboration, bringing together technologists, ethicists, and policymakers to establish standards that protect human dignity while enabling innovation. Ultimately, the ethical practice of data science demands not only technical excellence but also moral responsibility — a commitment to ensuring that data-driven insights serve humanity rather than exploit it."""
    
    print("🎯 ENHANCED SYSTEM - ZEROGPT KILLER MODE")
    print("=" * 80)
    print("Testing against ZeroGPT-style detection patterns")
    print("Original ZeroGPT score: 100% AI")
    print("Our previous score: 65% AI → 6% AI")
    print("Target: Beat ZeroGPT's 73% score on humanized text")
    print("=" * 80)
    
    try:
        result = proofread_text(test_text)
        
        print("\n" + "=" * 80)
        print("📊 ENHANCED RESULTS")
        print("=" * 80)
        print(f"Original AI Score (Our System): {result['ai_score_before_humanizing']}%")
        print(f"Final AI Score (Our System): {result['ai_score_after_humanizing']}%")
        print(f"Target <20% Achieved: {'✅ YES' if result['target_achieved'] else '❌ NO'}")
        print(f"Iterations Used: {result['iterations_used']}")
        print(f"Improvement: {result['improvement_percentage']}%")
        print(f"Word Count: {result['original_word_count']} → {result['humanized_word_count']}")
        
        print("\n" + "=" * 80)
        print("📝 ZEROGPT-OPTIMIZED HUMANIZED TEXT")
        print("=" * 80)
        print(result['humanized_text'])
        
        print("\n" + "=" * 80)
        print("🔍 ANALYSIS FOR ZEROGPT")
        print("=" * 80)
        
        # Check for ZeroGPT-beating features
        text = result['humanized_text']
        contractions = ["don't", "can't", "won't", "isn't", "aren't", "hasn't", "haven't", "doesn't"]
        contraction_count = sum(1 for c in contractions if c in text.lower())
        
        casual_words = ['plus', 'also', 'but', 'so', 'well', 'now', 'actually', 'really']
        casual_count = sum(1 for c in casual_words if c in text.lower())
        
        formal_triggers = ['furthermore', 'moreover', 'consequently', 'therefore', 'ubiquitous', 'profound']
        formal_count = sum(1 for f in formal_triggers if f in text.lower())
        
        print(f"✅ Contractions added: {contraction_count}")
        print(f"✅ Casual words: {casual_count}")
        print(f"✅ Formal triggers removed: {len([f for f in formal_triggers if f in test_text.lower()]) - formal_count}")
        print(f"✅ Word reduction: {result['original_word_count']} → {result['humanized_word_count']}")
        
        if result['ai_score_after_humanizing'] < 15:
            print("\n🎉 LIKELY TO BEAT ZEROGPT! Score under 15%")
        elif result['ai_score_after_humanizing'] < 25:
            print("\n👍 GOOD CHANCE TO BEAT ZEROGPT! Score under 25%")
        else:
            print("\n⚠️ May still trigger ZeroGPT - needs more humanization")
            
        print(f"\n📋 COPY THIS TEXT TO TEST ON ZEROGPT:")
        print("-" * 40)
        print(result['humanized_text'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_zerogpt_beating()