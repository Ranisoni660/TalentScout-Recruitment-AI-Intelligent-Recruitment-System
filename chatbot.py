"""
LLM integration and conversation management for TalentScout Hiring Assistant
"""

import json
import os
import requests
import re
from typing import Dict, List, Optional, Tuple
import streamlit as st

from config import SYSTEM_PROMPTS, ConversationState, REQUIRED_FIELDS
from utils import (
    validate_email, validate_phone, validate_experience, parse_tech_stack,
    is_conversation_ending, extract_name_from_input, sanitize_input,
    validate_location, validate_tech_stack
)

class HiringAssistantChatbot:
    """
    Main chatbot class for handling conversations with candidates
    """
    
    def __init__(self):
        """Initialize the chatbot with Hugging Face API"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            self.api_key = os.getenv("HUGGING_FACE_API_KEY", "").strip()
            
            # If no API key found, check if we can get it from Streamlit secrets
            if not self.api_key and hasattr(st, 'secrets'):
                self.api_key = st.secrets.get("HUGGING_FACE_API_KEY", "").strip()
            
            self.use_llm = bool(self.api_key and len(self.api_key) > 10)
            
            if self.use_llm:
                self.api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
                self.headers = {"Authorization": f"Bearer {self.api_key}"}
                st.success("✅ Hugging Face API connected!")
            else:
                st.info("🔧 Using enhanced fallback mode. For AI features, add HUGGING_FACE_API_KEY to .env file")
        
        except Exception as e:
            st.info("🔧 Fallback mode activated")
            self.use_llm = False
        
        self.reset_conversation()
    
    def reset_conversation(self):
        """Reset conversation state for new candidate"""
        if 'conversation_state' not in st.session_state:
            st.session_state.conversation_state = ConversationState.GREETING
        
        if 'candidate_data' not in st.session_state:
            st.session_state.candidate_data = {}
        
        if 'technical_questions' not in st.session_state:
            st.session_state.technical_questions = []
        
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
    
    def add_to_chat_history(self, role: str, message: str):
        """Add message to chat history"""
        st.session_state.chat_history.append({
            "role": role,
            "message": message,
            "timestamp": None
        })
    
    def get_llm_response(self, messages: List[Dict], use_json: bool = False) -> str:
        """Get response from Hugging Face LLM with better error handling"""
        try:
            # If no API key, use fallback immediately
            if not self.use_llm:
                return self._get_fallback_response(messages)
                
            prompt = self._format_messages_for_mistral(messages, use_json)
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 256,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    return self._clean_llm_response(generated_text.strip())
            
            # If API fails, use fallback
            return self._get_fallback_response(messages)
            
        except Exception as e:
            return self._get_fallback_response(messages)
    
    def _get_fallback_response(self, messages: List[Dict]) -> str:
        """Provide fallback responses when LLM is unavailable"""
        last_user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                last_user_message = msg.get('content', '')
                break
        
        if "greeting" in last_user_message.lower():
            return "👋 Hello! I'm TalentScout Hiring Assistant. I'm here to conduct your initial screening and technical assessment. Let's start by getting to know you better. What's your full name?"
        
        return "I'm here to assist with your screening process. Please continue with your response."
    
    def _clean_llm_response(self, text: str) -> str:
        """Clean up LLM response"""
        # Remove any trailing incomplete sentences or special tokens
        text = re.sub(r'\[INST\].*|\[/INST\].*', '', text)
        text = re.sub(r'<s>|</s>', '', text)
        return text.strip()
    
   def _format_messages_for_mistral(self, messages: List[Dict], use_json: bool = False) -> str:
    """Simple prompt formatting that works with DialoGPT"""
    last_user_message = ""
    for msg in reversed(messages):
        if msg.get('role') == 'user':
            last_user_message = msg.get('content', '')
            break
    
    # Simple prompt that works with DialoGPT
    return f"User: {last_user_message}\nAssistant:"
    
    def generate_greeting(self) -> str:
        """Generate initial greeting message - using simple fallback to avoid API issues"""
        return "👋 Hello! I'm TalentScout Hiring Assistant. I'm here to conduct your initial screening and technical assessment. Let's start by getting to know you better. What's your full name?"
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input based on current conversation state
        
        Args:
            user_input (str): Sanitized user input
            
        Returns:
            str: Bot response
        """
        if is_conversation_ending(user_input):
            return self.handle_conversation_end()
        
        state = st.session_state.conversation_state
        
        if state == ConversationState.GREETING:
            return self.start_information_collection()
        
        elif state == ConversationState.COLLECTING_NAME:
            return self.collect_name(user_input)
        
        elif state == ConversationState.COLLECTING_EMAIL:
            return self.collect_email(user_input)
        
        elif state == ConversationState.COLLECTING_PHONE:
            return self.collect_phone(user_input)
        
        elif state == ConversationState.COLLECTING_EXPERIENCE:
            return self.collect_experience(user_input)
        
        elif state == ConversationState.COLLECTING_POSITION:
            return self.collect_position(user_input)
        
        elif state == ConversationState.COLLECTING_LOCATION:
            return self.collect_location(user_input)
        
        elif state == ConversationState.COLLECTING_TECH_STACK:
            return self.collect_tech_stack(user_input)
        
        elif state == ConversationState.ASKING_QUESTIONS:
            return self.handle_technical_question_response(user_input)
        
        else:
            return self.generate_fallback_response(user_input)
    
    def start_information_collection(self) -> str:
        """Start collecting candidate information"""
        st.session_state.conversation_state = ConversationState.COLLECTING_NAME
        return "Great! Let's get started with the initial screening. First, could you please tell me your full name?"
    
    def collect_name(self, user_input: str) -> str:
        """Collect candidate's full name"""
        name = extract_name_from_input(user_input)
        if len(name.split()) >= 2:  # Expect at least first and last name
            st.session_state.candidate_data['name'] = name
            st.session_state.conversation_state = ConversationState.COLLECTING_EMAIL
            return f"Nice to meet you, {name}! Now, could you please provide your email address?"
        else:
            return "I'd like to get your full name (first and last name). Could you please provide that?"
    
    def collect_email(self, user_input: str) -> str:
        """Collect and validate candidate's email"""
        is_valid, error_message = validate_email(user_input)
        if is_valid:
            st.session_state.candidate_data['email'] = user_input.strip()
            st.session_state.conversation_state = ConversationState.COLLECTING_PHONE
            return "Perfect! Now I need your phone number for our records. Please provide a 10-digit phone number."
        else:
            return f"I need a valid email address. {error_message}"
    
    def collect_phone(self, user_input: str) -> str:
        """Collect and validate candidate's phone number - EXACTLY 10 DIGITS"""
        is_valid, error_message = validate_phone(user_input)
        if is_valid:
            # Format the phone number nicely
            digits_only = re.sub(r'\D', '', user_input)
            formatted_phone = f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
            st.session_state.candidate_data['phone'] = formatted_phone
            st.session_state.conversation_state = ConversationState.COLLECTING_EXPERIENCE
            return "Thank you! How many years of professional experience do you have in technology/software development?"
        else:
            return f"❌ {error_message} Please provide a valid 10-digit phone number (e.g., 123-456-7890 or (123) 456-7890)."
    
    def collect_experience(self, user_input: str) -> str:
        """Collect and validate years of experience"""
        is_valid, error_message, years = validate_experience(user_input)
        if is_valid:
            st.session_state.candidate_data['experience'] = years
            st.session_state.conversation_state = ConversationState.COLLECTING_POSITION
            return "Excellent! What position or role are you interested in applying for? (You can mention multiple if applicable)"
        else:
            return f"{error_message}"
    
    def collect_position(self, user_input: str) -> str:
        """Collect desired position(s)"""
        if user_input.strip():
            st.session_state.candidate_data['position'] = user_input.strip()
            st.session_state.conversation_state = ConversationState.COLLECTING_LOCATION
            return "Great choice! What's your current location or preferred work location? (Please provide city, state, or country)"
        else:
            return "Please let me know what position or role you're interested in."
    
    def collect_location(self, user_input: str) -> str:
        """Collect current/preferred location with validation"""
        is_valid, error_message = validate_location(user_input)
        if is_valid:
            st.session_state.candidate_data['location'] = user_input.strip()
            st.session_state.conversation_state = ConversationState.COLLECTING_TECH_STACK
            return """Perfect! Now, let's talk about your skills.

**Please provide your tech stack including:**
- At least **4 technical skills** (programming languages, frameworks, tools, databases)
- At least **2 soft skills** (communication, teamwork, problem-solving, etc.)

**Examples:**
- **Technical:** Python, JavaScript, React, Node.js, MongoDB, Docker, AWS
- **Soft Skills:** Communication, Teamwork, Problem Solving

You can separate them with commas."""
        else:
            return f"❌ {error_message} Please provide a valid location (city, state, or country)."
    
    def collect_tech_stack(self, user_input: str) -> str:
        """Collect and validate tech stack with minimum requirements"""
        is_valid, error_message, categorized_tech = validate_tech_stack(user_input)
        if is_valid:
            st.session_state.candidate_data['tech_stack'] = user_input.strip()
            st.session_state.candidate_data['tech_stack_parsed'] = categorized_tech
            
            # Show summary of what was collected
            tech_summary = "Great! I've recorded your skills:\n\n"
            
            # Technical skills summary
            technical_count = 0
            for category, skills in categorized_tech.items():
                if category != 'soft_skills' and skills:
                    technical_count += len(skills)
            
            soft_skills = categorized_tech.get('soft_skills', [])
            
            tech_summary += f"✅ **Technical Skills ({technical_count}):** {', '.join([skill for category in categorized_tech if category != 'soft_skills' for skill in categorized_tech[category]])}\n\n"
            tech_summary += f"✅ **Soft Skills ({len(soft_skills)}):** {', '.join(soft_skills)}\n\n"
            
            # Generate technical questions
            questions_response = self.generate_technical_questions()
            return tech_summary + questions_response
        else:
            return f"""❌ {error_message}

**Please provide:**
- At least **4 technical skills** (programming languages, frameworks, tools, databases)
- At least **2 soft skills** (communication, teamwork, problem-solving, etc.)

**Format:** Separate with commas
**Example:** Python, JavaScript, React, AWS, Communication, Teamwork"""
    
    def generate_technical_questions(self) -> str:
        """Generate technical questions based on tech stack"""
        try:
            tech_stack = st.session_state.candidate_data.get('tech_stack', '')
            experience = st.session_state.candidate_data.get('experience', 0)
            
            # Simpler prompt that works better with open-source models
            experience_level = "beginner" if experience < 3 else "intermediate" if experience < 6 else "senior"
            
            if self.use_llm:
                messages = [
                    {"role": "system", "content": "You are a technical interviewer. Generate 3-5 relevant technical questions based on the candidate's tech stack and experience level. List each question on a new line starting with 'Q:'."},
                    {"role": "user", "content": f"Generate technical questions for a {experience_level} level candidate with {experience} years of experience.\nTech stack: {tech_stack}\n\nProvide 3-5 questions, each on a new line starting with 'Q:'."}
                ]
                
                response = self.get_llm_response(messages, use_json=False)
                
                # Parse questions from response
                questions = []
                for line in response.split('\n'):
                    line = line.strip()
                    # Look for lines starting with Q: or numbered questions
                    if line.startswith('Q:') or line.startswith('Question'):
                        # Remove Q: or Question prefix
                        question = line.replace('Q:', '').replace('Question', '').strip()
                        question = question.lstrip('0123456789.:) ').strip()
                        if question and len(question) > 10:
                            questions.append(question)
                
                # If parsing failed, try to extract any question-like sentences
                if not questions:
                    potential_questions = re.findall(r'[^.!?]*\?', response)
                    questions = [q.strip() for q in potential_questions if len(q.strip()) > 20][:5]
            else:
                questions = []
            
            # Use fallback to predefined questions if LLM fails or not available
            if not questions:
                questions = self._get_fallback_questions(tech_stack, experience)
            
            if questions:
                st.session_state.technical_questions = questions
                st.session_state.current_question_index = 0
                st.session_state.conversation_state = ConversationState.ASKING_QUESTIONS
                
                return f"Now, I have {len(questions)} technical questions to help assess your skills. Let's start with the first one:\n\n**Question 1:** {questions[0]}"
            else:
                return "I've gathered all your information! However, I'm having trouble generating technical questions at the moment. Our team will review your profile and get back to you soon."
                
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            # Use fallback questions
            questions = self._get_fallback_questions(
                st.session_state.candidate_data.get('tech_stack', ''),
                st.session_state.candidate_data.get('experience', 0)
            )
            if questions:
                st.session_state.technical_questions = questions
                st.session_state.current_question_index = 0
                st.session_state.conversation_state = ConversationState.ASKING_QUESTIONS
                return f"Now, I have {len(questions)} technical questions to help assess your skills. Let's start with the first one:\n\n**Question 1:** {questions[0]}"
            return "I've gathered all your information! Our technical team will review your profile and prepare appropriate questions for the next round."
    
    def _get_fallback_questions(self, tech_stack: str, experience: int) -> List[str]:
        """Generate fallback questions when LLM fails"""
        tech_lower = tech_stack.lower()
        questions = []
        
        # Generic questions that apply to most tech stacks
        if experience < 3:
            questions.append("Can you explain the difference between a variable and a constant in programming?")
            questions.append("What is version control and why is it important in software development?")
        elif experience < 6:
            questions.append("Can you describe your approach to debugging complex issues in production?")
            questions.append("How do you ensure code quality and maintainability in your projects?")
        else:
            questions.append("How do you approach system design for scalable applications?")
            questions.append("Can you discuss a challenging technical problem you solved and your approach?")
        
        # Tech-specific questions
        if 'python' in tech_lower:
            questions.append("What are Python decorators and how have you used them in your projects?")
        if 'javascript' in tech_lower or 'react' in tech_lower or 'node' in tech_lower:
            questions.append("Can you explain the concept of asynchronous programming in JavaScript?")
        if 'django' in tech_lower or 'flask' in tech_lower:
            questions.append("How do you handle database migrations in Django/Flask applications?")
        if 'sql' in tech_lower or 'database' in tech_lower or 'postgresql' in tech_lower or 'mysql' in tech_lower:
            questions.append("How would you optimize a slow database query?")
        if 'docker' in tech_lower or 'kubernetes' in tech_lower:
            questions.append("Can you explain the benefits of containerization in your development workflow?")
        
        # Return up to 5 questions
        return questions[:5] if len(questions) <= 5 else questions[:5]
    
    def handle_technical_question_response(self, user_input: str) -> str:
        """Handle responses to technical questions"""
        current_index = st.session_state.current_question_index
        questions = st.session_state.technical_questions
        
        # Store the answer
        if 'technical_answers' not in st.session_state.candidate_data:
            st.session_state.candidate_data['technical_answers'] = []
        
        st.session_state.candidate_data['technical_answers'].append({
            'question': questions[current_index],
            'answer': user_input
        })
        
        # Move to next question or complete
        st.session_state.current_question_index += 1
        
        if st.session_state.current_question_index < len(questions):
            next_question = questions[st.session_state.current_question_index]
            question_num = st.session_state.current_question_index + 1
            return f"Thank you for that response! Here's the next question:\n\n**Question {question_num}:** {next_question}"
        else:
            st.session_state.conversation_state = ConversationState.COMPLETED
            return self.complete_screening()
    
    def complete_screening(self) -> str:
        """Complete the screening process"""
        candidate_name = st.session_state.candidate_data.get('name', 'Candidate')
        return f"""🎉 **Screening Complete!**

Thank you {candidate_name} for completing our initial screening process. 

**Summary of Information Collected:**
• Personal Details: Name, Contact Information
• Professional Background: {st.session_state.candidate_data.get('experience', 0)} years experience
• Position Interest: {st.session_state.candidate_data.get('position', 'N/A')}
• Location: {st.session_state.candidate_data.get('location', 'N/A')}
• Technical Assessment: {len(st.session_state.technical_questions)} questions answered

**Next Steps:**
• Our technical team will review your responses within 2-3 business days
• You'll receive an email update about your application status
• If selected, we'll schedule a more detailed technical interview

We appreciate your interest in opportunities through TalentScout, and we'll be in touch soon!

Is there anything else you'd like to know about our process?"""
    
    def handle_conversation_end(self) -> str:
        """Handle when user wants to end conversation"""
        return """Thank you for your time! If you'd like to complete the screening process later, please feel free to return. 

We're here whenever you're ready to continue. Have a great day! 👋"""
    
    def generate_fallback_response(self, user_input: str) -> str:
        """Generate fallback response for unexpected inputs"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPTS["fallback"]},
            {"role": "user", "content": f"User input: {user_input}"}
        ]
        
        return self.get_llm_response(messages)
    
    def get_conversation_progress(self) -> Tuple[int, int]:
        """Get conversation progress for display"""
        state_order = [
            ConversationState.GREETING,
            ConversationState.COLLECTING_NAME,
            ConversationState.COLLECTING_EMAIL,
            ConversationState.COLLECTING_PHONE,
            ConversationState.COLLECTING_EXPERIENCE,
            ConversationState.COLLECTING_POSITION,
            ConversationState.COLLECTING_LOCATION,
            ConversationState.COLLECTING_TECH_STACK,
            ConversationState.ASKING_QUESTIONS,
            ConversationState.COMPLETED
        ]
        
        current_state = st.session_state.conversation_state
        try:
            current_step = state_order.index(current_state) + 1
        except ValueError:
            current_step = 1
        
        return current_step, len(state_order)
