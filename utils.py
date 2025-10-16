"""
Utility functions for TalentScout Hiring Assistant
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from config import TECH_CATEGORIES

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email address format"""
    if not email:
        return False, "Email address is required"
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email.strip()):
        return True, ""
    else:
        return False, "Please provide a valid email address (e.g., john@example.com)"

def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate phone number format - EXACTLY 10 DIGITS"""
    if not phone:
        return False, "Phone number is required"
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's exactly 10 digits
    if len(digits_only) == 10:
        return True, ""
    else:
        return False, "Please provide a valid 10-digit phone number"

def validate_experience(experience: str) -> Tuple[bool, str, Optional[int]]:
    """Validate and extract years of experience"""
    if not experience:
        return False, "Years of experience is required", None
    
    # Extract number from string
    numbers = re.findall(r'\d+', experience)
    if numbers:
        years = int(numbers[0])
        if 0 <= years <= 50:
            return True, "", years
        else:
            return False, "Please provide a realistic number of years (0-50)", None
    else:
        return False, "Please provide the number of years of experience", None

def validate_location(location: str) -> Tuple[bool, str]:
    """Validate location input - More flexible"""
    if not location or len(location.strip()) < 2:
        return False, "Please provide a location"
    
    location_clean = location.strip()
    
    if len(location_clean) > 100:
        return False, "Location seems too long. Please provide a shorter location."
    
    return True, ""

def validate_tech_stack(tech_stack: str) -> Tuple[bool, str, Dict[str, List[str]]]:
    """
    Validate tech stack input - More flexible approach
    """
    if not tech_stack:
        return False, "Please provide your skills", {}
    
    # Split and clean tech stack
    tech_items = re.split(r'[,;|\n]+', tech_stack.lower())
    tech_items = [item.strip() for item in tech_items if item.strip()]
    
    if len(tech_items) < 3:
        return False, "Please provide at least 3 skills (mix of technical and soft skills)", {}
    
    # Categorize technologies
    categorized = {category: [] for category in TECH_CATEGORIES.keys()}
    soft_skills = []
    technical_skills = []
    
    # Common soft skills keywords
    soft_skill_keywords = [
        'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
        'adaptability', 'time management', 'creativity', 'collaboration', 'analytical',
        'interpersonal', 'presentation', 'negotiation', 'mentoring', 'training',
        'documentation', 'project management', 'agile', 'scrum', 'kanban'
    ]
    
    for item in tech_items:
        is_soft_skill = any(skill in item for skill in soft_skill_keywords)
        
        if is_soft_skill:
            soft_skills.append(item)
        else:
            technical_skills.append(item)
            
            # Categorize technical skills
            categorized_item = False
            for category, technologies in TECH_CATEGORIES.items():
                for tech in technologies:
                    if tech in item or item in tech:
                        if item not in categorized[category]:
                            categorized[category].append(item)
                        categorized_item = True
                        break
                if categorized_item:
                    break
            
            if not categorized_item:
                if 'other' not in categorized:
                    categorized['other'] = []
                categorized['other'].append(item)
    
    # More flexible validation - just ensure we have some skills
    if len(technical_skills) + len(soft_skills) < 3:
        return False, "Please provide at least 3 different skills", {}
    
    # Add soft skills to categorized result
    if soft_skills:
        categorized['soft_skills'] = soft_skills
    
    return True, "", categorized

def parse_tech_stack(tech_stack: str) -> Dict[str, List[str]]:
    """
    Parse and categorize tech stack from user input
    """
    if not tech_stack:
        return {}
    
    # Convert to lowercase and split by common separators
    tech_items = re.split(r'[,;|\n]+', tech_stack.lower())
    tech_items = [item.strip() for item in tech_items if item.strip()]
    
    categorized = {category: [] for category in TECH_CATEGORIES.keys()}
    soft_skills = []
    uncategorized = []
    
    # Common soft skills keywords
    soft_skill_keywords = [
        'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
        'adaptability', 'time management', 'creativity', 'collaboration', 'analytical'
    ]
    
    for item in tech_items:
        is_soft_skill = any(skill in item for skill in soft_skill_keywords)
        
        if is_soft_skill:
            soft_skills.append(item)
        else:
            categorized_item = False
            for category, technologies in TECH_CATEGORIES.items():
                for tech in technologies:
                    if tech in item or item in tech:
                        if item not in categorized[category]:
                            categorized[category].append(item)
                        categorized_item = True
                        break
                if categorized_item:
                    break
            
            if not categorized_item:
                uncategorized.append(item)
    
    # Add soft skills and uncategorized items
    if soft_skills:
        categorized["soft_skills"] = soft_skills
    if uncategorized:
        categorized["other"] = uncategorized
    
    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}

def format_candidate_info(candidate_data: Dict) -> str:
    """Format candidate information for display"""
    info_lines = []
    info_lines.append("**Candidate Information:**")
    info_lines.append(f"• **Name:** {candidate_data.get('name', 'N/A')}")
    info_lines.append(f"• **Email:** {candidate_data.get('email', 'N/A')}")
    info_lines.append(f"• **Phone:** {candidate_data.get('phone', 'N/A')}")
    info_lines.append(f"• **Experience:** {candidate_data.get('experience', 'N/A')} years")
    info_lines.append(f"• **Position:** {candidate_data.get('position', 'N/A')}")
    info_lines.append(f"• **Location:** {candidate_data.get('location', 'N/A')}")
    
    if candidate_data.get('tech_stack_parsed'):
        info_lines.append("• **Skills:**")
        tech_skills = []
        for category, technologies in candidate_data['tech_stack_parsed'].items():
            if technologies and category != 'soft_skills':
                tech_skills.extend(technologies)
        
        if tech_skills:
            info_lines.append(f"  - Technical: {', '.join(tech_skills)}")
        
        if 'soft_skills' in candidate_data['tech_stack_parsed']:
            soft_skills_list = ', '.join(candidate_data['tech_stack_parsed']['soft_skills'])
            info_lines.append(f"  - Soft Skills: {soft_skills_list}")
    
    return '\n'.join(info_lines)

def is_conversation_ending(message: str) -> bool:
    """Check if user wants to end the conversation"""
    ending_keywords = [
        'bye', 'goodbye', 'quit', 'exit', 'stop', 'end', 'finish', 
        'thank you', 'thanks', 'done', 'complete'
    ]
    
    message_lower = message.lower().strip()
    return any(keyword in message_lower for keyword in ending_keywords)

def extract_name_from_input(user_input: str) -> str:
    """Extract name from user input, handling common formats"""
    # Remove common prefixes
    prefixes_to_remove = ['my name is', 'i am', 'i\'m', 'call me', 'name:', 'name is']
    
    cleaned_input = user_input.lower().strip()
    for prefix in prefixes_to_remove:
        if cleaned_input.startswith(prefix):
            cleaned_input = cleaned_input[len(prefix):].strip()
            break
    
    # Return the cleaned input, but preserve original capitalization
    if cleaned_input != user_input.lower().strip():
        # Find where the prefix ended in original string
        original_without_prefix = user_input[len(user_input) - len(cleaned_input):].strip()
        return original_without_prefix
    
    return user_input.strip()

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent potential security issues"""
    if not user_input:
        return ""
    
    # Remove excessive whitespace
    sanitized = re.sub(r'\s+', ' ', user_input.strip())
    
    # Remove potentially harmful characters but keep normal punctuation
    sanitized = re.sub(r'[<>\"\'`]', '', sanitized)
    
    # Limit length
    max_length = 500
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized