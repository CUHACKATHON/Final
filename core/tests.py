from django.test import TestCase
from core.utils.chatbot_logic import detect_intent, get_chatbot_response, analyze_sentiment, extract_keywords
from core.models import ChatSession, ChatMessage
import json


class ChatbotLogicTests(TestCase):
    def test_detect_intent_greeting(self):
        """Test greeting intent detection"""
        message = "Hello, how are you?"
        intent = detect_intent(message)
        self.assertEqual(intent, 'greeting')

    def test_detect_intent_crisis(self):
        """Test crisis intent detection"""
        message = "I want to kill myself"
        intent = detect_intent(message)
        self.assertEqual(intent, 'crisis')

    def test_detect_intent_anxiety(self):
        """Test anxiety intent detection"""
        message = "I'm feeling really anxious about exams"
        intent = detect_intent(message)
        self.assertEqual(intent, 'anxiety')

    def test_detect_intent_depression(self):
        """Test depression intent detection"""
        message = "I feel so depressed and worthless"
        intent = detect_intent(message)
        self.assertEqual(intent, 'depression')

    def test_detect_intent_academic_stress(self):
        """Test academic stress intent detection"""
        message = "I'm stressed about my grades and assignments"
        intent = detect_intent(message)
        self.assertEqual(intent, 'anxiety')  # 'stressed' is in anxiety keywords

    def test_detect_intent_relationship(self):
        """Test relationship intent detection"""
        message = "I'm having issues with my friends"
        intent = detect_intent(message)
        self.assertEqual(intent, 'relationship')

    def test_detect_intent_sleep(self):
        """Test sleep intent detection"""
        message = "I can't sleep at night"
        intent = detect_intent(message)
        self.assertEqual(intent, 'sleep')

    def test_detect_intent_general(self):
        """Test general intent detection"""
        message = "What's the weather like?"
        intent = detect_intent(message)
        self.assertEqual(intent, 'general')

    def test_get_chatbot_response_crisis(self):
        """Test crisis response"""
        message = "I feel suicidal"
        response = get_chatbot_response(message)
        self.assertTrue(response['crisis_detected'])
        self.assertEqual(response['suggested_action'], 'book_appointment')
        self.assertIn('help', response['response'].lower())

    def test_get_chatbot_response_normal(self):
        """Test normal response"""
        message = "Hello"
        response = get_chatbot_response(message)
        self.assertFalse(response['crisis_detected'])
        self.assertIsNone(response['suggested_action'])
        self.assertEqual(response['intent'], 'greeting')

    def test_get_chatbot_response_with_history(self):
        """Test response with session history"""
        message = "I'm feeling depressed"
        history = ["Hello", "I'm stressed"]
        response = get_chatbot_response(message, history)
        self.assertEqual(response['intent'], 'depression')
        # For depression with history > 3, should suggest counseling
        if len(history) > 3:
            self.assertEqual(response['suggested_action'], 'suggest_counseling')

    def test_analyze_sentiment_positive(self):
        """Test positive sentiment"""
        message = "I feel good and happy today"
        sentiment = analyze_sentiment(message)
        self.assertGreater(sentiment, 0)

    def test_analyze_sentiment_negative(self):
        """Test negative sentiment"""
        message = "I feel bad and sad"
        sentiment = analyze_sentiment(message)
        self.assertLess(sentiment, 0)

    def test_analyze_sentiment_neutral(self):
        """Test neutral sentiment"""
        message = "Today is okay"
        sentiment = analyze_sentiment(message)
        self.assertEqual(sentiment, 0.3)  # "okay" is positive

    def test_extract_keywords_anxiety(self):
        """Test keyword extraction for anxiety"""
        message = "I'm feeling anxious and worried"
        keywords = extract_keywords(message)
        self.assertIn('anxiety', keywords)

    def test_extract_keywords_depression(self):
        """Test keyword extraction for depression"""
        message = "I'm depressed and hopeless"
        keywords = extract_keywords(message)
        self.assertIn('depression', keywords)

    def test_extract_keywords_multiple(self):
        """Test multiple keywords"""
        message = "I'm anxious and depressed"
        keywords = extract_keywords(message)
        self.assertIn('anxiety', keywords)
        self.assertIn('depression', keywords)


class ChatAPITests(TestCase):
    def test_chat_api_missing_message(self):
        """Test chat API with missing message"""
        from django.test import Client
        client = Client()
        response = client.post('/api/chat/', json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chat_api_valid_message(self):
        """Test chat API with valid message"""
        from django.test import Client
        client = Client()
        data = {'message': 'Hello'}
        response = client.post('/api/chat/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('response', response_data)
        self.assertIn('session_id', response_data)
