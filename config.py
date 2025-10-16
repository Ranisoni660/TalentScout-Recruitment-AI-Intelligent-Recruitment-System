"""
Configuration settings for TalentScout Hiring Assistant
"""

# Application Settings
APP_TITLE = "TalentScout Hiring Assistant"
APP_DESCRIPTION = "AI-powered recruitment chatbot for initial candidate screening"

# Conversation States
class ConversationState:
    GREETING = "greeting"
    COLLECTING_NAME = "collecting_name"
    COLLECTING_EMAIL = "collecting_email"
    COLLECTING_PHONE = "collecting_phone"
    COLLECTING_EXPERIENCE = "collecting_experience"
    COLLECTING_POSITION = "collecting_position"
    COLLECTING_LOCATION = "collecting_location"
    COLLECTING_TECH_STACK = "collecting_tech_stack"
    GENERATING_QUESTIONS = "generating_questions"
    ASKING_QUESTIONS = "asking_questions"
    COMPLETED = "completed"

# Required Information Fields
REQUIRED_FIELDS = [
    "name", "email", "phone", "experience", "position", "location", "tech_stack"
]

# Tech Stack Categories
TECH_CATEGORIES = {
    "languages": [
        "python", "javascript", "java", "c++", "c#", "go", "rust", "php", 
        "ruby", "swift", "kotlin", "typescript", "scala", "r", "matlab"
    ],
    "frameworks": [
        "react", "angular", "vue", "django", "flask", "fastapi", "spring", 
        "express", "node", "laravel", "rails", "asp.net", "nextjs", "nuxt"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite", 
        "oracle", "cassandra", "dynamodb", "firebase"
    ],
    "tools": [
        "docker", "kubernetes", "git", "jenkins", "aws", "azure", "gcp", 
        "terraform", "ansible", "webpack", "npm", "maven", "gradle"
    ],
    "cloud": [
        "aws", "azure", "gcp", "heroku", "vercel", "netlify", "digitalocean"
    ]
}

# System Prompts
SYSTEM_PROMPTS = {
    "main": """You are the TalentScout Hiring Assistant, a professional AI chatbot that helps screen candidates for technology positions. Your role is to:

1. Greet candidates warmly and explain your purpose
2. Systematically collect essential information in this exact order:
   - Full Name
   - Email Address
   - Phone Number (exactly 10 digits)
   - Years of Experience
   - Desired Position(s)
   - Current Location (city, state, or country)
   - Tech Stack (minimum 4 technical skills + 2 soft skills)
3. Ask ONE question at a time and wait for responses
4. Validate inputs when possible
5. After collecting all information, generate 3-5 relevant technical questions based on their tech stack
6. Maintain a professional, helpful, and encouraging tone throughout
7. Handle unexpected inputs gracefully while staying focused on the hiring process

Remember: You represent TalentScout recruitment agency. Be professional but friendly.""",

    "question_generator": """Based on the candidate's tech stack and experience level, generate 3-5 relevant technical questions that would help assess their proficiency. 

Consider:
- Their years of experience (beginner: 0-2 years, intermediate: 3-5 years, senior: 6+ years)
- The specific technologies they mentioned
- Mix of theoretical knowledge and practical application questions
- Questions should be conversational, not exam-style

Format your response as a JSON object with this structure:
{
    "questions": [
        "Question 1 here",
        "Question 2 here",
        "Question 3 here"
    ]
}""",

    "fallback": """The user input doesn't seem to answer the current question. Please politely ask for clarification while maintaining the conversation flow. Remind them what information you need and why it's important for the initial screening process."""
}