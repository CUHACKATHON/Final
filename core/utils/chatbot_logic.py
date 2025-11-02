"""
MindCare Assistant - AI Chatbot for Student Mental Health Support
A supportive friend and wellness guide for Indian college students
Multilingual support with OpenAI GPT integration (Psychiatrist Perspective)
"""

import re
import random
import os
from datetime import datetime
from langdetect import detect
from translate import Translator
from decouple import config
import google.generativeai as genai
from openai import OpenAI

# Configure OpenAI API (Primary - Psychiatrist Perspective)
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Configure Gemini API (Fallback)
GEMINI_API_KEY = config('GEMINI_API_KEY', default='AIzaSyD0C5fFFBshUq6s5tLeUI4_lhWAuj4MUZk')
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # Try newer model names first, fallback to older ones
        try:
            gemini_model = genai.GenerativeModel('gemini-1.5-pro')
        except:
            try:
                gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            except:
                try:
                    gemini_model = genai.GenerativeModel('gemini-pro')
                except:
                    gemini_model = None
    except Exception as e:
        print(f"Warning: Failed to configure Gemini: {e}")
        gemini_model = None


def detect_language(message):
    """Detect the language of the user's message"""
    try:
        return detect(message)
    except:
        return 'en'  # Default to English if detection fails


def translate_text(text, from_lang, to_lang):
    """Translate text between languages"""
    try:
        translator = Translator(from_lang=from_lang, to=to_lang)
        return translator.translate(text)
    except:
        return text  # Return original text if translation fails


def detect_intent(message, language='en'):
    """Detect user intent from message with multilingual support"""
    # Translate to English for intent detection if not already in English
    if language != 'en':
        message_for_detection = translate_text(message, language, 'en')
    else:
        message_for_detection = message

    message_lower = message_for_detection.lower()

    # Mental Health Only Guardrail - reject non-mental health topics
    non_mental_health_keywords = [
        'weather', 'homework', 'assignment', 'math', 'science', 'physics', 'chemistry',
        'biology', 'history', 'geography', 'politics', 'sports', 'movie', 'music',
        'game', 'food', 'recipe', 'travel', 'shopping', 'news', 'joke', 'funny'
    ]

    # Check if message contains non-mental health topics
    if any(keyword in message_lower for keyword in non_mental_health_keywords):
        return 'off_topic'

    # Greetings
    greetings = ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good afternoon', 'good evening']
    if any(word in message_lower for word in greetings):
        return 'greeting'

    # Crisis detection - highest priority
    crisis_keywords = ['suicide', 'kill myself', 'end my life', 'die', 'hurt myself', 'self harm', 'suicidal']
    if any(word in message_lower for word in crisis_keywords):
        return 'crisis'

    # Anxiety
    anxiety_keywords = ['anxious', 'anxiety', 'worried', 'panic', 'nervous', 'stress', 'stressed', 'overwhelmed', 'tension']
    if any(word in message_lower for word in anxiety_keywords):
        return 'anxiety'

    # Depression
    depression_keywords = ['depressed', 'depression', 'sad', 'hopeless', 'empty', 'worthless', 'tired', 'exhausted', 'no energy']
    if any(word in message_lower for word in depression_keywords):
        return 'depression'

    # Academic stress
    academic_keywords = ['exam', 'study', 'grades', 'assignment', 'project', 'deadline', 'fail', 'marks']
    if any(word in message_lower for word in academic_keywords):
        return 'academic_stress'

    # Relationship issues (check before greetings to avoid false positives)
    relationship_keywords = ['relationship', 'breakup', 'break up', 'lonely', 'isolated', 'rejected']
    if any(keyword in message_lower for keyword in relationship_keywords):
        return 'relationship'

    # Family/friend issues (separate check to avoid conflicts)
    social_keywords = ['family problem', 'friend problem', 'fighting with', 'argument with']
    if any(keyword in message_lower for keyword in social_keywords):
        return 'relationship'

    # Sleep issues
    sleep_keywords = ['sleep', 'insomnia', 'tired', 'exhausted', 'can\'t sleep', 'wake up']
    if any(word in message_lower for word in sleep_keywords):
        return 'sleep'

    # Positive responses and improvement
    positive_keywords = ['feeling better', 'improved', 'doing well', 'much better', 'progress', 'helpful', 'thanks', 'thank you', 'grateful', 'feeling good', 'happy', 'great', 'excellent']
    if any(keyword in message_lower for keyword in positive_keywords):
        return 'positive'

    return 'general'


def get_chatbot_response(message, session_history=None, emotion=None, preferred_language='en'):
    """
    Generate MindCare Assistant response using AI with enhanced input understanding
    Returns dict with response, crisis_detected flag, and suggested_action
    """
    # Preprocess user message for better understanding
    message = preprocess_user_message(message)
    
    # Use preferred language if provided, otherwise detect
    if preferred_language and preferred_language != 'auto':
        language = preferred_language
    else:
        language = detect_language(message)

    # Detect intent with language support
    intent = detect_intent(message, language)

    if session_history is None:
        session_history = []
    
    # Extract deeper context from message and history
    deeper_context = extract_deeper_context(message, session_history)
    
    # Analyze sentiment with enhanced detection
    sentiment_score = analyze_sentiment(message)

    # Inject emotion into context for multimodal reasoning
    emotion_context = ""
    if emotion:
        emotion_context = f"User's current facial expression shows: {emotion}. "

        # Enhanced emotional awareness for better support
        if emotion.lower() in ['sad', 'angry', 'fear']:
            emotion_context += "The user appears distressed - prioritize empathy and gentle support. "
        elif emotion.lower() in ['happy', 'surprise']:
            emotion_context += "The user appears positive - reinforce their current emotional state. "
        elif emotion.lower() == 'neutral':
            emotion_context += "The user appears neutral - maintain supportive conversation. "
        elif emotion.lower() == 'no_face_detected':
            emotion_context += "No facial data available - rely on text analysis only. "
    
    # Build comprehensive context summary
    context_summary = f"""
**Message Analysis:**
- Emotional Intensity: {deeper_context['emotional_intensity']}
- Urgency Level: {deeper_context['urgency_level']}
- Sentiment Score: {sentiment_score:.2f} (negative to positive scale)
- Symptoms Mentioned: {', '.join(deeper_context['mentioned_symptoms']) if deeper_context['mentioned_symptoms'] else 'None explicitly mentioned'}
- Functional Impact: {deeper_context['functional_impact'] if deeper_context['functional_impact'] else 'Not clearly indicated'}
- Temporal Context: {deeper_context['temporal_context'] if deeper_context['temporal_context'] else 'Not specified'}
"""

    response_data = {
        'response': '',
        'crisis_detected': False,
        'suggested_action': None,
        'intent': intent,
        'emotion_context': emotion_context.strip(),
        'language': language
    }

    # Mental Health Only Guardrail - reject off-topic questions
    if intent == 'off_topic':
        response_data['response'] = (
            "Mera kaam aapke mental well-being par focus karna hai. Kya hum us baare mein baat kar sakte hain jo aapko pareshaan kar raha hai?"
        )
        return response_data

    # Crisis handling - immediate priority (handle before AI calls)
    if intent == 'crisis':
        response_data['crisis_detected'] = True
        response_data['response'] = (
            "**Immediate Help Available**\n\n"
            "I understand you're going through an extremely difficult time right now. Your feelings are valid, and you don't have to go through this alone.\n\n"
            "**Emergency Helplines:**\n"
            "* National Mental Health Helpline (24/7): 1800-599-0019\n"
            "* Aasra Suicide Prevention: +91-9820466726\n"
            "* iCall: +91-9152987821\n\n"
            "Would you like me to help you book an appointment with a counselor? They can provide immediate support and guidance."
        )
        response_data['suggested_action'] = 'book_appointment'
        return response_data

    # Use OpenAI (Primary - Psychiatrist Perspective) or Gemini (Fallback) for generating responses
    try:
        # Build conversation history for context with enhanced formatting
        conversation_history = []
        if session_history:
            # Include last 6 exchanges for better context (increased from 5)
            for user_msg, bot_msg in session_history[-6:]:
                # Clean previous messages for better context
                clean_user_msg = preprocess_user_message(user_msg)
                conversation_history.append({"role": "user", "content": clean_user_msg})
                conversation_history.append({"role": "assistant", "content": bot_msg})
        
        # Add current user message (already preprocessed)
        conversation_history.append({"role": "user", "content": message})
        
        # Detect if this is a positive response
        is_positive_response = (sentiment_score > 0.3 or intent == 'positive' or 
                               any(word in message.lower() for word in ['better', 'improved', 'thanks', 'thank you', 'helpful', 'progress', 'good', 'great']))
        
        # Create system prompt with supportive mental health perspective (no formal credentials)
        if is_positive_response:
            system_prompt = f"""You are a compassionate mental health supporter providing confidential support to Indian college students through an anonymous chat platform. The user appears to be sharing positive news, improvements, or gratitude.

**Your Supportive Approach:**
- Celebrate their progress and positive experiences genuinely
- Acknowledge their efforts and resilience
- Provide encouragement to continue their mental health journey
- Share insights about maintaining wellness and preventing relapse
- Reinforce the positive coping strategies that are working for them
- Keep the tone warm, encouraging, and validating
- You respond in {language} - using English, Hindi, or Hinglish naturally based on user preference

**For Positive Responses:**
- Express genuine happiness for their progress: "I'm so glad to hear you're feeling better!"
- Validate their efforts: "It sounds like the strategies you've been using are really helping."
- Encourage continuation: "Keep up the great work - consistency is key to maintaining progress."
- Offer maintenance tips: "Here are some ways to help maintain this positive momentum..."
- Normalize that progress can have ups and downs: "Remember, healing isn't always linear, and that's completely normal."
"""
        else:
            system_prompt = f"""You are a compassionate mental health supporter with expertise in adolescent and young adult mental health, particularly in the Indian cultural context. You are providing confidential mental health support through an anonymous chat platform.

**Your Supportive Identity:**
- Experienced in supporting people with anxiety, depression, trauma, and adjustment disorders
- Deep understanding of Indian cultural contexts: joint family systems, academic pressure, career expectations, social stigma around mental health
- Evidence-based approach using Cognitive Behavioral Therapy (CBT), Dialectical Behavior Therapy (DBT), and other therapeutic techniques
- Warm, empathetic supporter who balances professional insight with genuine care
- You respond in {language} - using English, Hindi, or Hinglish naturally based on user preference

**Your Supportive Approach:**
1. **UNDERSTANDING & ASSESSMENT**: Gently explore their experience:
   - Symptom duration and frequency ("How long have you noticed this?")
   - Functional impact ("How is this affecting your daily life, studies, relationships?")
   - Triggers and context ("What situations make this worse or better?")
   - Co-occurring symptoms (sleep, appetite, concentration, energy levels)
   - Safety assessment ("Have you had any thoughts of harming yourself?")

2. **VALIDATION & UNDERSTANDING**: 
   - Acknowledge experiences with empathy: "What you're describing sounds like it could be related to anxiety - this is actually quite common and treatable"
   - Normalize symptoms while taking them seriously: "Many students experience similar difficulties, and it's important we address this"

3. **PSYCHOEDUCATION**: 
   - Explain mental health conditions in accessible terms: "Anxiety involves our fight-or-flight response being activated when there's no immediate danger"
   - Discuss how our minds and bodies work: "Depression can involve changes in brain chemistry, particularly neurotransmitters like serotonin"
   - Clarify treatment options: "Treatment typically involves therapy, sometimes medication, or both - a mental health professional can help determine what's best"

4. **EVIDENCE-BASED TECHNIQUES**: 
   - Cognitive techniques: "Let's examine the thought patterns that might be contributing to this"
   - Behavioral activation: "Sometimes we need to act our way into feeling better before we can think our way there"
   - Grounding techniques: "When anxiety peaks, grounding exercises can help regulate your nervous system"
   - Mindfulness and distress tolerance: "Mindfulness can help create space between you and overwhelming thoughts"

5. **REFERRAL GUIDANCE**: 
   - Know when to recommend in-person professional evaluation
   - Suggest therapy modalities that might be beneficial
   - Guide on when professional help might be helpful

**Response Style Guidelines:**
- Use mental health terminology when appropriate but always explain in simple terms: "What you're describing might align with anxiety symptoms - let me explain what that means..."
- Ask questions with curiosity and care: "Help me understand - when you say you feel anxious, what's happening in your body? What thoughts are running through your mind?"
- Provide insights: "What you're experiencing could be your body's stress response system being activated"
- Maintain supportive boundaries: Warm and empathetic - never diagnose formally, always recommend professional evaluation for serious concerns
- Use accessible language: Refer to "symptoms," "experiences," "strategies," "support approaches"

**Current Clinical Context:**
- Patient's message: "{message}"
- Clinical presentation pattern: {intent}
- Observable emotional state: {emotion_context}
- Communication preference: {language}
- Therapeutic relationship history: {len(session_history)} previous exchanges

**Enhanced Context Analysis:**
{context_summary}

**Conversation Flow Understanding:**
- This is {'a follow-up message in an ongoing conversation' if session_history else 'the initial contact in this session'}
- Previous exchanges suggest: {', '.join([f"{i+1}. '{msg[:50]}...'" for i, (msg, _) in enumerate(session_history[-3:])]) if session_history else 'No previous context'}

**Response Structure (Psychiatric Framework):**
1. **Validation** (Clinical empathy: "I understand this is distressing, and what you're experiencing is significant")
2. **Assessment** (Gently explore based on context: "To better understand, can you tell me more about...")
3. **Psychoeducation** (Provide clinical insight relevant to their symptoms: "What you're describing is consistent with...")
4. **Intervention** (Evidence-based techniques tailored to their needs: "From a psychiatric perspective, we often use...")
5. **Treatment Planning** (Next steps: "Given what we've discussed, I'd recommend...")

**Important Response Guidelines:**
- Address the urgency level appropriately ({deeper_context['urgency_level']})
- Match the emotional intensity in your response tone ({deeper_context['emotional_intensity']})
- Focus on symptoms they mentioned: {', '.join(deeper_context['mentioned_symptoms'][:3]) if deeper_context['mentioned_symptoms'] else 'General mental health support'}
- Use the conversation history to build on previous exchanges and avoid repetition
- If this seems urgent or high intensity, prioritize immediate support and consider suggesting professional evaluation sooner

**Critical Reminders:**
- Respond with supportive insight and genuine empathy
- You provide mental health support but cannot replace in-person professional evaluation
- Maintain confidentiality and supportive boundaries
- Be culturally sensitive to Indian contexts
- Always prioritize safety - assess for risk factors
- Never formally diagnose - always suggest professional evaluation when appropriate

Remember: This person is reaching out for mental health support. Respond with warmth, understanding, and helpful guidance while encouraging professional help when needed."""

        # Try OpenAI first (Primary - Psychiatrist Perspective)
        openai_success = False
        if openai_client:
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    *conversation_history
                ]
                
                # Try GPT-4 first, fallback to GPT-3.5-turbo if unavailable
                models_to_try = ["gpt-4", "gpt-3.5-turbo"]
                for model_name in models_to_try:
                    try:
                        response = openai_client.chat.completions.create(
                            model=model_name,
                            messages=messages,
                            temperature=0.75,  # Slightly increased for more natural, contextual responses
                            max_tokens=600,  # Increased for more comprehensive responses
                            presence_penalty=0.3,  # Encourage variety and avoid repetition
                            frequency_penalty=0.2  # Reduce repetitive phrases
                        )
                        
                        response_text = response.choices[0].message.content.strip()
                        response_data['response'] = response_text
                        openai_success = True
                        break  # Success, exit loop
                    except Exception as model_error:
                        if model_name == models_to_try[-1]:  # Last model failed
                            raise model_error
                        continue  # Try next model
                
            except Exception as openai_error:
                print(f"OpenAI API error: {openai_error}")
                # Fall through to Gemini fallback
                openai_success = False
        
        # Fallback to Gemini if OpenAI fails or is not configured
        if not openai_success and gemini_model:
            try:
                # Check for positive response
                is_positive = (sentiment_score > 0.3 or intent == 'positive')
                
                if is_positive:
                    prompt = f"""You are a compassionate mental health supporter providing confidential support to Indian college students. The user is sharing positive news or improvements.

**For Positive Responses:**
- Celebrate their progress genuinely
- Acknowledge their efforts and resilience
- Encourage continuation of what's working
- Share tips for maintaining wellness
- Keep tone warm and encouraging
- Respond in {language} (English/Hindi/Hinglish)

**User's positive message:** "{message}"
**Context:** {context_summary}

Provide a warm, encouraging response that celebrates their progress and offers tips for maintaining their positive momentum.
"""
                else:
                    prompt = f"""
You are a compassionate mental health supporter with expertise in adolescent mental health, providing confidential support through an anonymous chat platform.

**Your Supportive Identity:**
- Experienced in supporting people with anxiety, depression, and adjustment disorders
- Deep understanding of Indian cultural contexts, academic pressures, and family dynamics
- Evidence-based approach using CBT, DBT, and other therapeutic techniques
- Respond in {language} (English/Hindi/Hinglish) based on user preference

**Your Supportive Approach:**
1. **UNDERSTANDING**: Gently explore symptoms, duration, functional impact, and triggers
2. **VALIDATION**: Acknowledge experiences with empathy and understanding
3. **PSYCHOEDUCATION**: Explain mental health conditions in accessible terms
4. **EVIDENCE-BASED TECHNIQUES**: Suggest CBT techniques, behavioral activation, grounding exercises, mindfulness
5. **REFERRAL GUIDANCE**: Guide on when in-person professional evaluation might be beneficial

**Response Style:**
- Use accessible language ("symptoms," "experiences," "strategies")
- Ask questions with care: "How long have you experienced this?" "What's the impact on your daily functioning?"
- Provide insights: "What you're describing could be related to anxiety - this involves the activation of your stress response system"
- Maintain supportive boundaries: Warm and empathetic
- Format with clear structure and bullet points

**Current Context:**
- User's message: "{message}"
- Situation: {intent}
- Observable emotional state: {emotion_context}
- Language preference: {language}

**Enhanced Context:**
{context_summary}

**Response Instructions:**
- Address urgency: {deeper_context['urgency_level']}
- Match emotional intensity: {deeper_context['emotional_intensity']}
- Focus on mentioned symptoms: {', '.join(deeper_context['mentioned_symptoms'][:3]) if deeper_context['mentioned_symptoms'] else 'General support'}
- Consider conversation history and build on previous exchanges

Provide a warm, supportive response that demonstrates understanding and helpful guidance. Structure: Validation → Understanding → Psychoeducation → Practical Strategies → Next Steps.
"""
                
                # Enhanced Gemini configuration for better responses
                generation_config = {
                    "temperature": 0.75,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 600,
                }
                
                gemini_response = gemini_model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                response_text = gemini_response.text.strip()
                response_data['response'] = response_text
            except Exception as gemini_error:
                print(f"Gemini API error: {gemini_error}")
                # Will fall through to basic fallback responses

        # Clean up formatting for better readability
        if response_data.get('response'):
            response_data['response'] = response_data['response'].replace('**', '').replace('*', '•')
        
        # If no response was generated, ensure we have a fallback
        if not response_data.get('response'):
            # This will be handled by the outer except block
            raise Exception("No response generated from AI services")

    except Exception as e:
        # Check if positive response needs special handling
        is_positive = (sentiment_score > 0.3 or intent == 'positive' or 
                      any(word in message.lower() for word in ['better', 'improved', 'thanks', 'thank you', 'helpful']))
        
        # Fallback to basic responses with supportive perspective if both AI services fail
        print(f"AI API error: {e}")
        
        if is_positive:
            fallback_responses = {
                'positive': """I'm so happy to hear you're feeling better! That's wonderful news, and it sounds like the strategies you've been using are really helping.

Keep up the great work - maintaining progress takes consistent effort, and you're doing it! Remember that healing isn't always linear, and it's completely normal to have ups and downs.

Here are some tips to help maintain this positive momentum:
• Continue with the coping strategies that have been working for you
• Practice self-care regularly - even on good days
• Stay connected with supportive people in your life
• Notice what's different when you're feeling better and try to maintain those conditions

If you ever feel like you need extra support, I'm always here to chat. How are you planning to continue taking care of your mental health?""",
                'greeting': "Hello! I'm here to provide mental health support. I'm so glad you reached out! How have you been feeling lately?",
            }
            response_data['response'] = fallback_responses.get('positive', fallback_responses.get('greeting', ''))
            return response_data
        
        fallback_responses = {
            'greeting': "Hello! I'm here to provide mental health support. I understand you're reaching out today. Can you share what brings you here and how you've been feeling recently?",
            'anxiety': """I understand that what you're experiencing feels overwhelming, and I want you to know that anxiety symptoms like these are very treatable from a psychiatric perspective.

What you're likely experiencing is your body's stress response system (fight-or-flight) being activated. From a clinical standpoint, we can address this through several evidence-based approaches:

**Immediate grounding technique** (to help regulate your nervous system):
- Name 5 things you can see around you
- 4 things you can touch
- 3 things you can hear
- 2 things you can smell
- 1 thing you can taste

This technique helps shift your focus and can reduce the intensity of anxiety symptoms. 

To better understand your experience clinically: How long have you been noticing these anxiety symptoms? And how would you say they're affecting your daily functioning?""",
            'depression': """I recognize that what you're describing sounds very difficult, and I want you to know that depressive symptoms like these are clinically significant and treatable.

Depression can involve changes in mood, energy, and interest levels - what we sometimes see is the brain's stress response system being chronically activated or neurotransmitter imbalances. 

From a psychiatric perspective, treatment typically involves evidence-based approaches like:
- Cognitive Behavioral Therapy (CBT) to address thought patterns
- Behavioral activation (engaging in activities even when motivation is low)
- Sometimes medication may be considered after proper evaluation

Right now, what's one small, manageable thing you could do today? Sometimes we need to act our way into feeling better, even if just slightly.

To help me understand better clinically: How long have you been experiencing these feelings? Have you noticed changes in your sleep, appetite, or ability to concentrate?""",
            'academic_stress': """Academic pressure can significantly impact mental health, and what you're experiencing is quite common among students. From a psychiatric perspective, chronic academic stress can activate our stress response system, leading to anxiety, burnout, or depressive symptoms.

To address this clinically, let's break it down:
- **Behavioral activation**: What's the smallest, most manageable study task you could complete in the next 15 minutes? Sometimes starting with tiny steps can help reduce the feeling of being overwhelmed.
- **Cognitive reframing**: How might we reframe this challenge? What skills are you building through this process?

I'd also like to understand: How is this academic stress affecting your sleep, mood, or overall functioning? This information helps me better assess what kind of support might be most helpful.""",
            'relationship': """Relationship challenges can have a significant impact on mental health and well-being. What you're experiencing is valid and clinically important to address.

From a psychiatric perspective, relationship difficulties can contribute to stress, anxiety, or depressive symptoms. It's important to:
- Validate your own feelings and experiences
- Consider how these challenges are affecting your mental health and daily functioning
- Explore coping strategies that work for you

Our peer forum does offer connection with others who've had similar experiences, which can be part of your support system.

To better understand clinically: How long have you been dealing with these relationship challenges? And how would you say they're impacting your mood, sleep, or ability to function day-to-day?""",
            'sleep': """Sleep issues can significantly impact mental health - they're often interconnected with conditions like anxiety and depression. From a psychiatric perspective, sleep disruption can both contribute to and be a symptom of mental health concerns.

**Evidence-based sleep hygiene interventions:**
- Dim lights and avoid screens 30-60 minutes before bed (blue light can disrupt melatonin production)
- Maintain a consistent sleep schedule (even on weekends)
- Create a calming bedtime routine
- If anxious thoughts keep you awake, try a cognitive technique: acknowledge the thought, then gently redirect to your breathing

To assess this clinically: How long have you been experiencing sleep difficulties? Are you having trouble falling asleep, staying asleep, or waking too early? And how is the poor sleep affecting your daytime functioning, mood, or energy levels?""",
            'general': "I'm here to provide mental health support. I understand you're reaching out today, and I want to help. Can you tell me more about what's been on your mind or how you've been feeling? Understanding what brings you here will help me provide the most appropriate support."
        }
        response_data['response'] = fallback_responses.get(intent, fallback_responses['general'])

    # Suggest appointment if intent suggests professional help might be beneficial (but not for positive responses)
    # Check if this is a positive response
    is_positive_final = (sentiment_score > 0.3 or intent == 'positive' or 
                        any(word in message.lower() for word in ['better', 'improved', 'thanks', 'thank you', 'helpful', 'progress']))
    
    if intent in ['depression', 'anxiety'] and len(session_history) > 3 and not is_positive_final:
        response_data['suggested_action'] = 'suggest_counseling'
        response_data['response'] += "\n\n**Supportive Recommendation**: Based on our conversation, I'd recommend that you consider connecting with a professional mental health provider for an in-person evaluation. This would allow for a comprehensive assessment and can help explore treatment options such as therapy or, if needed, medication. Would you like help exploring that option?"

    return response_data


def preprocess_user_message(message):
    """
    Enhanced preprocessing of user input for better understanding
    - Clean and normalize text
    - Extract key information
    - Identify emotional intensity
    """
    if not message:
        return message
    
    # Basic cleaning
    message = message.strip()
    message = re.sub(r'\s+', ' ', message)  # Normalize whitespace
    
    return message


def extract_deeper_context(message, session_history=None):
    """
    Extract deeper context from user message and conversation history
    Returns a dictionary with insights about the user's situation
    """
    context = {
        'urgency_level': 'normal',
        'emotional_intensity': 'moderate',
        'mentioned_symptoms': [],
        'functional_impact': None,
        'social_context': None,
        'temporal_context': None
    }
    
    message_lower = message.lower()
    
    # Detect urgency indicators
    urgent_indicators = ['urgent', 'immediately', 'now', 'right now', 'emergency', 'help me', 'desperate', 'cant cope', "can't cope"]
    if any(indicator in message_lower for indicator in urgent_indicators):
        context['urgency_level'] = 'high'
    
    # Detect emotional intensity
    high_intensity_words = ['extremely', 'very', 'really', 'so much', 'too much', 'overwhelming', 'unbearable', 'terrible']
    if any(word in message_lower for word in high_intensity_words):
        context['emotional_intensity'] = 'high'
    elif any(word in message_lower for word in ['slightly', 'a bit', 'somewhat', 'kinda', 'kind of']):
        context['emotional_intensity'] = 'low'
    
    # Extract mentioned symptoms from message
    symptom_keywords = {
        'sleep_issues': ['sleep', 'insomnia', 'cant sleep', "can't sleep", 'tired', 'exhausted', 'wake up'],
        'appetite_changes': ['appetite', 'eating', 'food', 'hunger', 'not hungry'],
        'concentration': ['concentrate', 'focus', 'attention', 'mind wandering'],
        'energy': ['energy', 'tired', 'fatigue', 'lethargic', 'no energy'],
        'mood': ['mood', 'feelings', 'emotions', 'emotional'],
        'anxiety_physical': ['heart racing', 'sweating', 'shaking', 'chest tight', 'breathing', 'panic'],
        'social': ['alone', 'isolated', 'friends', 'family', 'people'],
        'academic': ['study', 'exam', 'grades', 'classes', 'college', 'university']
    }
    
    for symptom, keywords in symptom_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            context['mentioned_symptoms'].append(symptom)
    
    # Detect functional impact
    impact_indicators = ['cant', "can't", 'unable', 'difficulty', 'hard to', 'struggling', 'affecting', 'impact']
    if any(indicator in message_lower for indicator in impact_indicators):
        context['functional_impact'] = 'mentioned'
    
    # Extract temporal context (duration)
    time_indicators = ['for weeks', 'for months', 'for days', 'since', 'recently', 'lately', 'always', 'never']
    for indicator in time_indicators:
        if indicator in message_lower:
            context['temporal_context'] = indicator
            break
    
    # Check conversation history for patterns
    if session_history:
        # Check if user is repeating concerns
        recent_topics = []
        for user_msg, _ in session_history[-3:]:
            recent_topics.append(user_msg.lower()[:50])  # First 50 chars as topic
        if len(recent_topics) > 1 and any(topic in message_lower for topic in recent_topics):
            context['repeating_concern'] = True
    
    return context


def analyze_sentiment(message):
    """Enhanced sentiment analysis - returns score between -1 (negative) and 1 (positive)"""
    positive_words = ['good', 'happy', 'great', 'better', 'fine', 'okay', 'excited', 'grateful', 'relieved', 'hopeful', 'improved', 'support', 'help']
    negative_words = ['bad', 'sad', 'awful', 'terrible', 'worst', 'hate', 'angry', 'frustrated', 'hopeless', 'anxious', 'worried', 'scared', 'depressed', 'tired', 'exhausted']
    
    message_lower = message.lower()
    positive_count = sum(1 for word in positive_words if word in message_lower)
    negative_count = sum(1 for word in negative_words if word in message_lower)
    
    # Calculate weighted sentiment
    if positive_count > negative_count:
        intensity = min(positive_count / max(len(message.split()), 1), 1.0)  # Normalize by message length
        return 0.3 + (intensity * 0.4)  # Range: 0.3 to 0.7
    elif negative_count > positive_count:
        intensity = min(negative_count / max(len(message.split()), 1), 1.0)
        return -0.5 - (intensity * 0.4)  # Range: -0.5 to -0.9
    else:
        return 0.0


def extract_keywords(message):
    """Extract keywords for analytics"""
    message_lower = message.lower()
    keywords = {
        'anxiety': ['anxious', 'anxiety', 'worried', 'panic', 'nervous', 'stress'],
        'depression': ['depressed', 'depression', 'sad', 'hopeless', 'empty', 'worthless']
    }
    
    detected = []
    for category, words in keywords.items():
        if any(word in message_lower for word in words):
            detected.append(category)
    
    return detected
