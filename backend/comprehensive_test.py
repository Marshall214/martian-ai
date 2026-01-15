#!/usr/bin/env python3

from utils.proof_ai import proofread_text
import time

def test_comprehensive_scenarios():
    """Test various academic text scenarios to verify consistent <20% performance."""
    
    test_cases = [
        {
            "name": "STEM Research Paper",
            "text": """This study demonstrates that machine learning algorithms significantly improve data processing efficiency. Furthermore, the systematic implementation of deep learning methodologies facilitates substantial enhancements in pattern recognition capabilities. Moreover, evidence indicates that artificial neural networks establish robust frameworks for complex computational tasks. Consequently, researchers must comprehensively evaluate these sophisticated technologies to optimize their practical applications."""
        },
        {
            "name": "Business Analysis",
            "text": """Organizations increasingly utilize comprehensive data analytics frameworks to optimize performance metrics and drive strategic decision-making processes. Furthermore, the strategic implementation of artificial intelligence technologies facilitates substantial improvements in operational efficiency and customer satisfaction outcomes. Moreover, evidence demonstrates that systematic approaches to digital transformation establish competitive advantages in contemporary market environments and enhance long-term sustainability. Consequently, businesses must fundamentally reconsider their technological infrastructures to remain competitive in evolving markets."""
        },
        {
            "name": "Educational Research",
            "text": """This comprehensive analysis demonstrates that innovative pedagogical methodologies significantly enhance student learning outcomes. Furthermore, the systematic integration of technology-based educational tools facilitates substantial improvements in academic performance metrics. Moreover, research indicates that personalized learning approaches establish optimal conditions for diverse student populations. Consequently, educational institutions must rigorously evaluate these transformative technologies."""
        },
        {
            "name": "Medical Research",
            "text": """Clinical studies demonstrate that advanced diagnostic technologies significantly improve patient outcomes. Furthermore, the systematic implementation of artificial intelligence in healthcare settings facilitates substantial enhancements in treatment efficacy. Moreover, evidence indicates that machine learning algorithms establish robust frameworks for medical decision-making processes. Consequently, healthcare professionals must comprehensively evaluate these innovative methodologies."""
        }
    ]
    
    print("🧪 COMPREHENSIVE HUMANIZATION TESTING")
    print("=" * 80)
    print("Testing various academic domains for consistent <20% AI detection...")
    print("=" * 80)
    
    results_summary = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 TEST {i}/4: {test_case['name']}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            result = proofread_text(test_case['text'])
            
            processing_time = time.time() - start_time
            
            # Store results
            test_result = {
                'name': test_case['name'],
                'original_score': result['ai_score_before_humanizing'],
                'final_score': result['ai_score_after_humanizing'],
                'target_achieved': result['target_achieved'],
                'iterations': result['iterations_used'],
                'improvement': result['improvement_percentage'],
                'processing_time': round(processing_time, 2),
                'word_count_change': f"{result['original_word_count']} → {result['humanized_word_count']}"
            }
            results_summary.append(test_result)
            
            # Display results
            status = "✅ SUCCESS" if result['target_achieved'] else "❌ FAILED"
            print(f"Status: {status}")
            print(f"AI Score: {result['ai_score_before_humanizing']}% → {result['ai_score_after_humanizing']}%")
            print(f"Iterations: {result['iterations_used']}")
            print(f"Processing: {processing_time:.2f}s")
            print(f"Words: {test_result['word_count_change']}")
            
            if result['target_achieved']:
                print(f"🎯 Target achieved! Score reduced by {result['improvement_percentage']}%")
            else:
                print(f"⚠️ Target missed by {result['ai_score_after_humanizing'] - 20}%")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results_summary.append({
                'name': test_case['name'],
                'error': str(e)
            })
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 FINAL SUMMARY")
    print("=" * 80)
    
    successful_tests = [r for r in results_summary if 'error' not in r and r['target_achieved']]
    failed_tests = [r for r in results_summary if 'error' not in r and not r['target_achieved']]
    error_tests = [r for r in results_summary if 'error' in r]
    
    print(f"✅ Successful (< 20%): {len(successful_tests)}/{len(test_cases)}")
    print(f"❌ Failed (≥ 20%): {len(failed_tests)}/{len(test_cases)}")
    print(f"🔧 Errors: {len(error_tests)}/{len(test_cases)}")
    
    if successful_tests:
        avg_improvement = sum(r['improvement'] for r in successful_tests) / len(successful_tests)
        avg_final_score = sum(r['final_score'] for r in successful_tests) / len(successful_tests)
        avg_iterations = sum(r['iterations'] for r in successful_tests) / len(successful_tests)
        avg_time = sum(r['processing_time'] for r in successful_tests) / len(successful_tests)
        
        print(f"\n📈 Performance Metrics (Successful Tests):")
        print(f"Average Final AI Score: {avg_final_score:.1f}%")
        print(f"Average Improvement: {avg_improvement:.1f}%")
        print(f"Average Iterations: {avg_iterations:.1f}")
        print(f"Average Processing Time: {avg_time:.2f}s")
    
    if failed_tests:
        print(f"\n⚠️ Failed Tests:")
        for result in failed_tests:
            print(f"- {result['name']}: {result['final_score']}% (missed by {result['final_score'] - 20}%)")
    
    if error_tests:
        print(f"\n🔧 Error Tests:")
        for result in error_tests:
            print(f"- {result['name']}: {result['error']}")
    
    success_rate = len(successful_tests) / len(test_cases) * 100
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🎉 EXCELLENT! System consistently achieves <20% AI detection target!")
    elif success_rate >= 50:
        print("👍 GOOD! System achieves target in most cases.")
    else:
        print("⚠️ NEEDS IMPROVEMENT! System requires further optimization.")

if __name__ == "__main__":
    test_comprehensive_scenarios()