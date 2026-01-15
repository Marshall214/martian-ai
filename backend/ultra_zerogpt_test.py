#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.proof_ai import proofread_text

# Test text that scored 76.66% on ZeroGPT
test_text = """In the era of ubiquitous data, working with data has become a dominant force shaping decisions across healthcare, finance, education, and governance. but the same analytical power that enables insight also raises profound ethical concerns. The use of computer programs to steps and interpret data introduces biases that can reinforce social inequities if not properly addressed. Data scientists must so adopt frameworks that emphasize transparency, accountability, and fairness in model development. Ethical gathering information practices are equally critical, as individuals' privacy and consent remain foundational to trust in data systems. what's more explainability in artificial intelligence is essential to ensure that automated decisions can be understood, challenged, and improved. The emergence of data ethics as a discipline highlights the need for interdisciplinary collaboration, bringing together technologists, ethicists, and policymakers to show standards that protect human dignity while enabling innovation. Ultimately, the ethical practice of working with data demands not only technical excellence but also moral responsibility — a commitment to ensuring that data-driven insights serve humanity rather than exploit it."""

print("🤖 ULTRA ZEROGPT HUMANIZATION TEST")
print("=" * 50)
print(f"Original Text (ZeroGPT: 76.66%):")
print(f"'{test_text[:100]}...'")
print()

# Apply ultra-aggressive humanization
result = proofread_text(test_text)

print("🎯 ULTRA-HUMANIZED RESULT:")
print("=" * 30)
print(f"Final AI Score: {result['ai_score_after_humanizing']:.1f}%")
print(f"Iterations Used: {result['iterations_used']}")
print(f"Improvement: {76.66 - result['ai_score_after_humanizing']:.1f} points")
print()
print("HUMANIZED TEXT:")
print(result['humanized_text'])
print()
print("🔍 KEY CHANGES MADE:")
print("- Ultra-casual vocabulary injection")
print("- Maximum contraction usage") 
print("- Academic jargon elimination")
print("- Sentence structure variation")
print("- Informal connector words")
print("- Personal touch additions")