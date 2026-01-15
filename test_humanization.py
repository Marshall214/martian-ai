import sys
sys.path.append(r'c:\Users\HP\work projects\martian ai\backend')

from utils.proof_ai import proofread_text

# Test academic text with high AI detection likelihood
test_text = """
Data science has significantly transformed the way organizations approach decision-making processes. This study demonstrates the implementation of machine learning algorithms in business intelligence applications. The methodology employed in this research indicates that systematic extraction of actionable knowledge from complex datasets drives innovation in various industries.

Furthermore, the comprehensive analysis reveals that evidence-based decisions substantially improve organizational performance. It is important to note that technical proficiency in data science requires a multidisciplinary approach. Moreover, the transformative potential of artificial intelligence creates new opportunities while simultaneously presenting persistent challenges that require rigorous oversight and policy frameworks.

Research shows that the integration of advanced analytics facilitates better understanding of market dynamics. Consequently, organizations that utilize data-driven strategies demonstrate remarkably superior performance compared to traditional approaches. The findings essentially establish that modern businesses must fundamentally embrace data science to remain competitive in today's market environment.
"""

print("Testing iterative humanization system...")
print("=" * 60)
print(f"Input text ({len(test_text.split())} words):")
print(test_text[:200] + "...")
print("\n" + "=" * 60)

try:
    result = proofread_text(test_text)
    print("\nRESULTS:")
    print(f"AI Score Before: {result['ai_score_before_humanizing']}%")
    print(f"AI Score After: {result['ai_score_after_humanizing']}%") 
    print(f"Improvement: {result['improvement_percentage']}%")
    print(f"Target Achieved: {'✓ YES' if result['ai_score_after_humanizing'] < 20 else '✗ NO'}")
    
    print(f"\nWord Count: {result['original_word_count']} → {result['humanized_word_count']}")
    
    print("\n" + "=" * 60)
    print("HUMANIZED OUTPUT:")
    print(result['humanized_text'][:500] + "..." if len(result['humanized_text']) > 500 else result['humanized_text'])
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()