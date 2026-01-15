#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.proof_ai import proofread_text, calculate_ai_detection_score

# Test the specific text that's failing
failing_text = """Title: Ethical Challenges in the Age of Artificial Intelligence

Artificial Intelligence (AI) has revolutionized modern society by enabling machines to learn, reason, and make decisions with minimal human intervention. While these capabilities offer immense benefits—from precision medicine to autonomous systems—they also introduce complex ethical dilemmas. Central among these is the issue of algorithmic bias, where AI systems reproduce or amplify existing social prejudices embedded in training data. Additionally, the opacity of many machine learning models, often referred to as the "black box" problem, undermines transparency and accountability. Ethical AI demands that models be explainable, auditable, and aligned with human values. Another concern lies in the potential misuse of AI technologies for surveillance, manipulation, and disinformation, threatening privacy and democratic integrity. Addressing these challenges requires a multi-stakeholder approach involving ethicists, policymakers, engineers, and the public. The goal is to establish governance frameworks that promote fairness, responsibility, and inclusivity in AI deployment. Ultimately, ethical AI is not solely about preventing harm but about designing systems that actively enhance human well-being, ensuring that technological progress serves collective good rather than narrow interests."""

print("🚨 ZEROGPT CALIBRATION TEST")
print("=" * 50)
print("Testing text that ZeroGPT rates as 100% AI but Martian AI rates as 51%")
print()

# Test current detection
current_score = calculate_ai_detection_score(failing_text)
print(f"❌ Current Martian AI Detection: {current_score}%")
print(f"🎯 ZeroGPT Detection: 100%")
print(f"📊 Gap: {100 - current_score} points TOO LOW")
print()

# Test humanization
print("🔄 Testing Current Humanization System...")
result = proofread_text(failing_text)

print(f"Results:")
print(f"  Before: {result['ai_score_before_humanizing']}%")  
print(f"  After:  {result['ai_score_after_humanizing']}%")
print(f"  ZeroGPT After: 98.37% (FAILED!)")
print()

print("🔍 ISSUES IDENTIFIED:")
print("1. Detection algorithm 49 points too lenient vs ZeroGPT")
print("2. Humanization only reduced ZeroGPT by 1.63% (should be 80%+)")
print("3. Need ULTRA-AGGRESSIVE ZeroGPT-specific calibration")
print()

print("📄 FAILED HUMANIZED TEXT:")
print(result['humanized_text'][:300] + "...")