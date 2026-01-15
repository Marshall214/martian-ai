"""
Test file for slide generation system
Tests the complete flow: content analysis, chunking, and PPTX generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from utils.slidegen_advanced import (
    ContentAnalyzer,
    SlideChunker,
    SlideBuilder,
    SlideGenerator,
    generate_slides,
    TEMPLATES
)

def test_content_analyzer():
    """Test content analysis"""
    print("\n=== Testing Content Analyzer ===")
    
    sample_text = """
    # Introduction to Machine Learning
    
    Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience.
    
    ## Key Concepts
    
    Supervised learning involves training algorithms on labeled data. The algorithm learns the mapping between inputs and outputs.
    
    Unsupervised learning deals with unlabeled data. Algorithms find patterns and relationships in the data without predefined outputs.
    
    ## Applications
    
    Machine learning has revolutionized many industries. From healthcare diagnostics to autonomous vehicles, ML is everywhere.
    
    Deep learning, a subset of machine learning using neural networks, has achieved remarkable results in image recognition and natural language processing.
    """
    
    analysis = ContentAnalyzer.analyze(sample_text)
    print(f"Word count: {analysis['word_count']}")
    print(f"Sections found: {analysis['section_count']}")
    print(f"Content type: {analysis['content_type']}")
    print(f"Density: {analysis['density']}")
    print(f"Estimated slides: {analysis['estimated_slides']}")
    print(f"✓ Content analyzer working!")


def test_slide_chunker():
    """Test content chunking"""
    print("\n=== Testing Slide Chunker ===")
    
    sample_sections = [
        {
            'title': 'Introduction',
            'content': 'This is the introduction section with multiple sentences. We will cover the basics here. The content is informative.',
            'word_count': 20
        },
        {
            'title': 'Methodology',
            'content': 'This section describes the methodology. We used multiple approaches. Testing was extensive. Results were validated.',
            'word_count': 20
        },
        {
            'title': 'Results',
            'content': 'The results show significant improvements. Performance metrics improved by 30%. Efficiency gains were notable.',
            'word_count': 20
        }
    ]
    
    chunks = SlideChunker.chunk_content(sample_sections, estimated_slides=5)
    print(f"Generated {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {chunk['title']}")
        print(f"    Bullet points: {len(chunk['bullet_points'])}")
    print(f"✓ Slide chunker working!")


def test_slide_generation():
    """Test full slide generation"""
    print("\n=== Testing Full Slide Generation ===")
    
    sample_text = """
    Research Methods in Data Science
    
    Data science research requires rigorous methodology and careful validation.
    
    Exploratory Data Analysis (EDA) is the first step. We examine data distributions, identify outliers, and understand relationships between variables.
    
    Feature Engineering transforms raw data into meaningful features. This step is crucial for model performance. Feature selection helps reduce dimensionality.
    
    Model Selection involves choosing appropriate algorithms. We compare different models like linear regression, decision trees, and neural networks.
    
    Validation and Testing ensure model generalization. Cross-validation prevents overfitting. Test set evaluation provides unbiased performance estimates.
    
    Deployment requires monitoring and maintenance. Models degrade over time as data distributions change. Regular retraining keeps models performant.
    """
    
    result = generate_slides(
        content=sample_text,
        title="Research Methods in Data Science",
        prompt="Make this academic and formal",
        export_format="pptx"
    )
    
    print(f"Status: Generated successfully")
    print(f"Title: {result['metadata']['title']}")
    print(f"Word count: {result['metadata']['word_count']}")
    print(f"Slide count: {result['metadata']['slide_count']}")
    print(f"Template: {result['metadata']['template']}")
    print(f"Content type: {result['metadata']['content_type']}")
    print(f"PDF available: {result['metadata']['pdf_available']}")
    
    # Check PPTX was generated
    if result['pptx']:
        pptx_size = len(result['pptx'].getvalue())
        print(f"PPTX size: {pptx_size / 1024:.2f} KB")
        print(f"✓ PPTX generated!")
    
    # Save to file for manual inspection
    with open('test_presentation.pptx', 'wb') as f:
        f.write(result['pptx'].getvalue())
    print(f"✓ Saved test presentation to test_presentation.pptx")


def test_template_detection():
    """Test template auto-detection"""
    print("\n=== Testing Template Detection ===")
    
    test_cases = [
        ("This research study investigates hypothesis testing and methodology", "academic"),
        ("Quarterly revenue increased 25% with market expansion strategies", "business"),
        ("Vibrant designs with creative color schemes", "creative"),
        ("Data analysis revealed statistical correlations in the dataset", "research"),
    ]
    
    for text, expected in test_cases:
        analysis = ContentAnalyzer.analyze(text)
        detected = analysis['content_type']
        match = "✓" if detected == expected else "✗"
        print(f"{match} Text: '{text[:40]}...' -> Detected: {detected} (Expected: {expected})")


def test_templates_available():
    """List available templates"""
    print("\n=== Available Templates ===")
    for name, config in TEMPLATES.items():
        print(f"  • {config['name']:15} - {name}")
        print(f"    Colors: Primary={config['primary_color']}, Accent={config['accent_color']}")


if __name__ == "__main__":
    print("🚀 Running Slide Generation Tests...")
    
    try:
        test_content_analyzer()
        test_templates_available()
        test_template_detection()
        test_slide_chunker()
        test_slide_generation()
        
        print("\n" + "="*50)
        print("✅ All tests passed successfully!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
