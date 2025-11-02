"""
Test script for chatbot functionality
Tests the chatbot with various scenarios
"""

import os
import sys
import django
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentalhealth.settings')
django.setup()

from core.utils.chatbot_logic import get_chatbot_response, detect_intent, analyze_sentiment, extract_keywords

def test_chatbot():
    """Test chatbot with various messages"""
    print("=" * 60)
    print("CHATBOT FUNCTIONALITY TEST")
    print("=" * 60)
    print()
    
    test_cases = [
        {
            "message": "Hello",
            "description": "Greeting test",
            "emotion": None,
            "language": "en"
        },
        {
            "message": "I'm feeling very anxious about my exams",
            "description": "Anxiety test",
            "emotion": "Fear",
            "language": "en"
        },
        {
            "message": "I've been feeling depressed for weeks",
            "description": "Depression test",
            "emotion": "Sad",
            "language": "en"
        },
        {
            "message": "I can't sleep at night",
            "description": "Sleep issues test",
            "emotion": None,
            "language": "en"
        },
        {
            "message": "I'm stressed about my relationship",
            "description": "Relationship stress test",
            "emotion": None,
            "language": "en"
        },
        {
            "message": "नमस्ते, मुझे चिंता हो रही है",
            "description": "Hindi language test",
            "emotion": None,
            "language": "hi"
        }
    ]
    
    print("Testing Intent Detection:")
    print("-" * 60)
    for test in test_cases:
        intent = detect_intent(test["message"], test.get("language", "en"))
        print(f"Message: '{test['message'][:50]}...'")
        print(f"Intent: {intent}")
        print()
    
    print("\nTesting Sentiment Analysis:")
    print("-" * 60)
    for test in test_cases:
        sentiment = analyze_sentiment(test["message"])
        print(f"Message: '{test['message'][:50]}...'")
        print(f"Sentiment Score: {sentiment}")
        print()
    
    print("\nTesting Keyword Extraction:")
    print("-" * 60)
    for test in test_cases:
        keywords = extract_keywords(test["message"])
        print(f"Message: '{test['message'][:50]}...'")
        print(f"Keywords: {keywords}")
        print()
    
    print("\nTesting Chatbot Responses:")
    print("-" * 60)
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"User Message: {test['message']}")
        print(f"Emotion: {test.get('emotion', 'None')}")
        print(f"Language: {test.get('language', 'en')}")
        print("-" * 60)
        
        try:
            response = get_chatbot_response(
                message=test["message"],
                session_history=[],
                emotion=test.get("emotion"),
                preferred_language=test.get("language", "en")
            )
            
            print(f"✓ Response Generated Successfully")
            print(f"Crisis Detected: {response.get('crisis_detected', False)}")
            print(f"Intent: {response.get('intent', 'N/A')}")
            print(f"Language: {response.get('language', 'N/A')}")
            print(f"Suggested Action: {response.get('suggested_action', 'None')}")
            print(f"\nResponse Text:")
            print(response.get('response', 'No response')[:300])
            print()
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            print()
    
    print("\n" + "=" * 60)
    print("CONVERSATION HISTORY TEST")
    print("=" * 60)
    print()
    
    # Test with conversation history
    session_history = [
        ("Hello", "Hello! I'm here to support you. How are you feeling today?"),
        ("I'm anxious", "I understand anxiety can feel overwhelming. Let's work through this together.")
    ]
    
    test_message = "I've been feeling this way for a while"
    print(f"User Message: {test_message}")
    print(f"Session History: {len(session_history)} previous exchanges")
    print("-" * 60)
    
    try:
        response = get_chatbot_response(
            message=test_message,
            session_history=session_history,
            emotion=None,
            preferred_language="en"
        )
        
        print(f"✓ Response Generated Successfully")
        print(f"\nResponse Text:")
        print(response.get('response', 'No response')[:300])
        print()
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("CRISIS DETECTION TEST")
    print("=" * 60)
    print()
    
    crisis_messages = [
        "I want to kill myself",
        "I feel like ending my life",
        "I'm thinking about suicide"
    ]
    
    for msg in crisis_messages:
        print(f"Testing: '{msg}'")
        try:
            response = get_chatbot_response(
                message=msg,
                session_history=[],
                emotion=None,
                preferred_language="en"
            )
            
            print(f"Crisis Detected: {response.get('crisis_detected', False)}")
            print(f"Suggested Action: {response.get('suggested_action', 'None')}")
            if response.get('crisis_detected'):
                print("✓ Crisis properly detected!")
            print()
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            print()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_chatbot()
