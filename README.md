# TalentScout-Recruitment-AI-Intelligent-Recruitment-System
🚀 TalentScout AI Hiring Assistant - Complete Assignment Solution
📋 Table of Contents

    Project Overview

    Features Implemented

    Technical Architecture

    Local Setup & Installation

    Hugging Face Integration

    Deployment Guide

    Prompt Engineering

    Code Structure

    Demo & Submission

🎯 Project Overview

TalentScout AI Hiring Assistant is an intelligent chatbot designed for initial candidate screening. It conducts structured conversations to gather essential candidate information and assesses technical proficiency through tailored questions based on the candidate's declared tech stack.
🎯 Assignment Requirements Fulfilled
Requirement	Status	Implementation
UI Framework	✅	Streamlit with custom CSS
Chatbot Capabilities	✅	Full conversation flow
Information Gathering	✅	7 key data points collected
Tech Stack Declaration	✅	Dynamic skill parsing
Technical Questions	✅	3-5 tailored questions
Context Handling	✅	State management
Fallback Mechanism	✅	Input validation
End Conversation	✅	Graceful exit
Hugging Face Integration	✅	Free API usage
✨ Features Implemented
🎯 Core Features (Required)

    Smart Greeting & Introduction - Professional onboarding

    Structured Data Collection - 7-step information gathering

    Tech Stack Parsing - Intelligent skill categorization

    Dynamic Question Generation - 3-5 tailored technical questions

    Conversation State Management - Context-aware interactions

    Input Validation - Email, phone, experience validation

    Graceful Exit - Professional conversation ending

🚀 Bonus Features (Optional Enhancements)

    Advanced UI/UX - Professional gradient design with animations

    Real-time Progress Tracking - Visual progress indicators

    Session Statistics - Message counts and metrics

    Responsive Design - Mobile-friendly interface

    Export-Ready Data - Structured candidate profiles

    Input Sanitization - Security measures

    Error Handling - Comprehensive error management

🏗️ Technical Architecture
🔧 Tech Stack
python

Frontend: Streamlit + Custom CSS
Backend: Python 3.8+
AI Model: Hugging Face Inference API (Free)
State Management: Streamlit Session State
Deployment: Streamlit Community Cloud

📁 Project Structure
text

talentscout-assistant/
├── app.py                 # Main Streamlit application
├── chatbot.py            # Core chatbot logic & conversation flow
├── utils.py              # Utility functions & input validation
├── config.py             # Configuration constants & prompts
├── requirements.txt      # Python dependencies
├── .gitignore           # Git exclusion rules
├── README.md            # This documentation
└── .streamlit/          # Streamlit config (if needed)
    └── config.toml

🛠️ Local Setup & Installation
Step 1: Environment Setup
bash

# Create project directory
mkdir talentscout-assistant
cd talentscout-assistant

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

Step 2: Install Dependencies
bash

pip install streamlit huggingface_hub python-dotenv pyyaml

Step 3: Get Hugging Face API Key (FREE)

    Go to Hugging Face

    Create account/login

    Go to Access Tokens

    Click "New token"

    Name: talentscout-assistant

    Role: read (free tier)

    Copy the token

Step 4: Environment Configuration

Create .env file:
env

HUGGINGFACEHUB_API_TOKEN=your_hugging_face_token_here

Step 5: Run Application
bash

streamlit run app.py

🔐 Hugging Face Integration
🤖 Model Selection

We use Hugging Face Inference API with microsoft/DialoGPT-medium for conversational AI:

Why Hugging Face?

    ✅ Free tier available - No credit card required

    ✅ Multiple model options - DialoGPT, GPT-2, etc.

    ✅ Easy API integration - Simple REST calls

    ✅ Good for conversation - Dialog-optimized models

🔑 API Setup Code
python

import os
from huggingface_hub import InferenceClient

class HiringAssistantChatbot:
    def __init__(self):
        self.client = InferenceClient(
            token=os.getenv('HUGGINGFACEHUB_API_TOKEN')
        )
    
    def generate_response(self, prompt):
        response = self.client.conversational(
            text=prompt,
            model="microsoft/DialoGPT-medium"
        )
        return response

💰 Cost Analysis

    Hugging Face Inference: FREE for limited requests

    No credit card required

    Perfect for internship projects

🚀 Deployment Guide
GitHub Repository Setup

Step 1: Create .gitignore
gitignore

# API Keys
.env
*.env

# Virtual Environment
venv/
env/

# Python
__pycache__/
*.pyc

# Streamlit
.streamlit/

# OS
.DS_Store
Thumbs.db

Step 2: Create requirements.txt
txt

streamlit>=1.28.0
huggingface_hub>=0.19.0
python-dotenv>=1.0.0
PyYAML>=6.0

Step 3: Initialize Git
bash

git init
git add .
git commit -m "feat: Complete TalentScout AI Hiring Assistant"

Streamlit Cloud Deployment

Step 1: Create GitHub Repository

    Go to GitHub

    Create new repository: talentscout-hiring-assistant

    Push your code

Step 2: Deploy to Streamlit

    Go to share.streamlit.io

    Sign in with GitHub

    Click "New app"

    Configure:

        Repository: yourusername/talentscout-hiring-assistant

        Branch: main

        Main file: app.py

Step 3: Add Hugging Face Token

    In Streamlit app settings → "Secrets"

    Add:

toml

HUGGINGFACEHUB_API_TOKEN = "your_hugging_face_token_here"

Step 4: Update Code for Streamlit Secrets
In app.py, add:
python

import streamlit as st

# Load Hugging Face token from Streamlit secrets or .env
if 'HUGGINGFACEHUB_API_TOKEN' in st.secrets:
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = st.secrets['HUGGINGFACEHUB_API_TOKEN']
else:
    from dotenv import load_dotenv
    load_dotenv()

🎯 Prompt Engineering
Conversation Flow Design

1. Greeting Prompt
python

GREETING_PROMPT = """
You are TalentScout AI Hiring Assistant. Greet the candidate professionally and explain you'll conduct a screening process. 
Keep it warm but professional. Mention it will take 5-10 minutes.
"""

2. Information Gathering Prompts
python

NAME_PROMPT = "Ask for the candidate's full name in a professional manner."
EMAIL_PROMPT = "Request email address and mention it's for official communication."
EXPERIENCE_PROMPT = "Ask about years of professional experience in the tech industry."

3. Tech Stack Processing
python

TECH_STACK_PROMPT = """
Analyze this tech stack: {tech_stack}
Categorize into: programming_languages, frameworks, databases, tools, soft_skills
Return structured JSON.
"""

4. Question Generation
python

QUESTION_PROMPT = """
Generate 3-5 technical questions for a {level} level candidate with these skills: {skills}
Focus on: {category}
Make questions practical and interview-relevant.
Difficulty: {difficulty}
"""

Context Management Strategy

State Tracking
python

CONVERSATION_STATES = {
    'greeting': 'Initial welcome',
    'collecting_name': 'Getting candidate name',
    'collecting_email': 'Email collection',
    'collecting_phone': 'Phone verification',
    'collecting_experience': 'Experience assessment',
    'collecting_position': 'Position preferences',
    'collecting_location': 'Location info',
    'collecting_tech_stack': 'Skills evaluation',
    'asking_questions': 'Technical assessment',
    'completed': 'Screening finished'
}

📊 Code Structure Deep Dive
app.py - Main Application
python

class TalentScoutApp:
    """
    Main Streamlit application with:
    - Session state management
    - UI rendering
    - User input handling
    - Progress tracking
    """

chatbot.py - AI Logic
python

class HiringAssistantChatbot:
    """
    Core chatbot functionality:
    - Hugging Face API integration
    - Conversation state management
    - Technical question generation
    - Input validation
    """

utils.py - Utilities
python

# Input validation functions
def validate_email(email): ...
def validate_phone(phone): ...
def sanitize_input(text): ...

# Data formatting
def format_candidate_info(data): ...

config.py - Configuration
python

# All prompts, constants, and configurations
APP_CONFIG = {
    'model': 'microsoft/DialoGPT-medium',
    'max_tokens': 500,
    'temperature': 0.7
    
