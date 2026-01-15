#!/usr/bin/env python3

from utils.proof_ai import proofread_text

def test_user_text():
    """Test the user's provided text about data ethics."""
    
    test_text = """In the era of ubiquitous data, data science has become a dominant force shaping decisions across healthcare, finance, education, and governance. However, the same analytical power that enables insight also raises profound ethical concerns. The use of algorithms to process and interpret data introduces biases that can reinforce social inequities if not properly addressed. Data scientists must therefore adopt frameworks that emphasize transparency, accountability, and fairness in model development. Ethical data collection practices are equally critical, as individuals' privacy and consent remain foundational to trust in data systems. Moreover, explainability in artificial intelligence is essential to ensure that automated decisions can be understood, challenged, and improved. The emergence of data ethics as a discipline highlights the need for interdisciplinary collaboration, bringing together technologists, ethicists, and policymakers to establish standards that protect human dignity while enabling innovation. Ultimately, the ethical practice of data science demands not only technical excellence but also moral responsibility — a commitment to ensuring that data-driven insights serve humanity rather than exploit it."""
    
    print("🔍 PROCESSING YOUR DATA ETHICS TEXT")
    print("=" * 70)
    print(f"Input length: {len(test_text.split())} words")
    print("=" * 70)
    
    try:
        result = proofread_text(test_text)
        
        print("\n" + "=" * 70)
        print("📊 RESULTS SUMMARY")
        print("=" * 70)
        print(f"Original AI Score: {result['ai_score_before_humanizing']}%")
        print(f"Final AI Score: {result['ai_score_after_humanizing']}%")
        print(f"Target <20% Achieved: {'✅ YES' if result['target_achieved'] else '❌ NO'}")
        print(f"Iterations Used: {result['iterations_used']}")
        print(f"Improvement: {result['improvement_percentage']}%")
        print(f"Word Count: {result['original_word_count']} → {result['humanized_word_count']}")
        
        print("\n" + "=" * 70)
        print("📝 HUMANIZED TEXT")
        print("=" * 70)
        print(result['humanized_text'])
        
        print("\n" + "=" * 70)
        print("🎯 COMPARISON")
        print("=" * 70)
        print("BEFORE:", result['ai_score_before_humanizing'], "%")
        print("AFTER: ", result['ai_score_after_humanizing'], "%")
        if result['target_achieved']:
            print("🎉 SUCCESS! Achieved <20% target!")
        else:
            print("⚠️ Target not achieved, but significant improvement made.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_text()