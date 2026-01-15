#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.proof_ai import proofread_text

def test_integrated_system():
    """Test the integrated ZeroGPT-beating system with various academic texts."""
    
    test_cases = [
        {
            "name": "Data Ethics Text (Original 99% AI)",
            "text": """In the contemporary landscape of ubiquitous data proliferation, data science has emerged as a dominant force in shaping organizational decision-making processes across diverse sectors including healthcare, finance, education, and governance. However, the same analytical capabilities that facilitate unprecedented insights also raise profound ethical considerations that demand rigorous examination. The implementation of sophisticated algorithms to process and interpret vast datasets introduces inherent biases that can potentially reinforce existing social inequities if not adequately addressed through comprehensive oversight mechanisms. Data scientists must therefore adopt robust ethical frameworks that emphasize transparency, accountability, and fairness in algorithmic development and deployment. Furthermore, ethical data collection practices are equally critical, as individual privacy rights and informed consent remain foundational elements in maintaining public trust in data-driven systems. Moreover, explainability in artificial intelligence systems is essential to ensure that automated decision-making processes can be understood, challenged, and improved by relevant stakeholders. The emergence of data ethics as a distinct academic discipline highlights the imperative need for interdisciplinary collaboration, bringing together technologists, ethicists, policymakers, and domain experts to establish comprehensive standards that protect human dignity while enabling continued innovation and progress."""
        },
        {
            "name": "Machine Learning Research Text",
            "text": """This study demonstrates the effectiveness of novel machine learning methodologies in addressing complex optimization challenges within computational frameworks. The research employs comprehensive analytical approaches to evaluate the performance of sophisticated algorithms across diverse datasets. Furthermore, the investigation reveals significant improvements in predictive accuracy through the implementation of advanced feature engineering techniques. The methodology encompasses rigorous statistical validation procedures to ensure the robustness and generalizability of the proposed solutions."""
        },
        {
            "name": "Academic Medical Text", 
            "text": """The clinical investigation examined the efficacy of therapeutic interventions in patients with chronic conditions across multiple healthcare institutions. Moreover, the comprehensive analysis demonstrated significant improvements in patient outcomes through evidence-based treatment protocols and systematic care coordination. Furthermore, the study utilized rigorous methodological approaches to validate the effectiveness of innovative medical procedures across diverse patient populations. The research encompassed longitudinal data collection, standardized assessment protocols, and comprehensive statistical analysis to ensure reliable and generalizable findings that contribute to evidence-based clinical practice guidelines."""
        }
    ]
    
    print("🧪 INTEGRATED ZEROGPT-BEATING SYSTEM TEST")
    print("=" * 60)
    print("Testing the integrated nuclear humanization system...")
    print()
    
    results = []
    for i, case in enumerate(test_cases, 1):
        print(f"📝 TEST CASE {i}: {case['name']}")
        print("-" * 40)
        print(f"Original text: {case['text'][:100]}...")
        print()
        
        # Apply integrated humanization
        result = proofread_text(case['text'])
        
        print(f"✅ RESULTS:")
        print(f"   AI Score Before: {result['ai_score_before_humanizing']}%")
        print(f"   AI Score After:  {result['ai_score_after_humanizing']}%")
        print(f"   Improvement:     {result['improvement_percentage']} points")
        print(f"   Target Achieved: {'✅ YES' if result['target_achieved'] else '❌ NO'}")
        print(f"   Iterations Used: {result['iterations_used']}")
        print()
        print(f"📄 HUMANIZED TEXT:")
        print(f"{result['humanized_text'][:200]}...")
        print()
        
        results.append(result)
        print("=" * 60)
        print()
    
    # Summary statistics
    print("📊 SUMMARY STATISTICS:")
    print("-" * 30)
    successful_cases = sum(1 for r in results if r['target_achieved'])
    average_improvement = sum(r['improvement_percentage'] for r in results) / len(results)
    average_final_score = sum(r['ai_score_after_humanizing'] for r in results) / len(results)
    
    print(f"✅ Success Rate: {successful_cases}/{len(results)} ({successful_cases/len(results)*100:.1f}%)")
    print(f"📈 Average Improvement: {average_improvement:.1f} points")
    print(f"🎯 Average Final AI Score: {average_final_score:.1f}%")
    print(f"🏆 ZeroGPT Target (<20%): {'ACHIEVED' if average_final_score < 20 else 'NOT ACHIEVED'}")
    
    if successful_cases == len(results):
        print()
        print("🎉 PERFECT SUCCESS! All test cases achieved <20% AI detection!")
        print("🚀 The integrated system is ready for ZeroGPT deployment!")
    elif successful_cases > len(results) * 0.8:
        print()
        print("✅ EXCELLENT! Most cases achieved the target. System is highly effective!")
    else:
        print()
        print("⚠️ Some improvements needed. Consider additional optimization.")

if __name__ == "__main__":
    test_integrated_system()
    