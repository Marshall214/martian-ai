#!/usr/bin/env python3

from utils.proof_ai import proofread_text

def test_enhanced_humanization():
    """Test the enhanced humanization system with comprehensive vocabulary."""
    
    # Test with a highly academic text
    test_text = """This study demonstrates that artificial intelligence significantly impacts modern educational frameworks. Furthermore, the comprehensive analysis reveals that systematic implementation of machine learning methodologies facilitates substantial improvements in student performance metrics. Moreover, evidence indicates that the transformative potential of AI-driven educational technologies establishes new paradigms for personalized learning experiences. Consequently, institutions must fundamentally reconsider their pedagogical approaches to effectively utilize these innovative tools. The research comprehensively examines various algorithmic approaches, demonstrating that sophisticated natural language processing capabilities enable more nuanced assessment methodologies. Additionally, this investigation reveals that robust data analytics frameworks substantially enhance the precision of educational outcome predictions."""
    
    print("🧪 TESTING ENHANCED HUMANIZATION SYSTEM")
    print("=" * 60)
    print(f"Input text length: {len(test_text.split())} words")
    print(f"Input preview: {test_text[:100]}...")
    print("\n" + "=" * 60)
    
    try:
        result = proofread_text(test_text)
        
        print("\n" + "=" * 60)
        print("🎯 FINAL RESULTS")
        print("=" * 60)
        print(f"Original AI Score: {result['ai_score_before_humanizing']}%")
        print(f"Final AI Score: {result['ai_score_after_humanizing']}%") 
        print(f"Target <20% Achieved: {'✅ YES' if result['target_achieved'] else '❌ NO'}")
        print(f"Iterations Used: {result['iterations_used']}")
        print(f"Improvement: {result['improvement_percentage']}%")
        print(f"Word Count Change: {result['original_word_count']} → {result['humanized_word_count']}")
        
        print("\n" + "=" * 60)
        print("📝 HUMANIZED TEXT")
        print("=" * 60)
        print(result['humanized_text'])
        
        if result['target_achieved']:
            print("\n🎉 SUCCESS! AI detection score successfully reduced below 20%!")
        else:
            print(f"\n⚠️ Target not fully achieved. Score: {result['ai_score_after_humanizing']}%")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_humanization()