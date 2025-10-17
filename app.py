"""
TalentScout Hiring Assistant - Main Streamlit Application
"""

import streamlit as st
import os
from dotenv import load_dotenv
# Load Hugging Face API Key from Streamlit Secrets
if 'HUGGING_FACE_API_KEY' in st.secrets:
    os.environ['HUGGING_FACE_API_KEY'] = st.secrets['HUGGING_FACE_API_KEY']
    st.success("✅ API Key Loaded from Secrets!")
else:
    st.error("❌ API Key not found in Secrets!")
    
# Load environment variables from .env file
load_dotenv()

from chatbot import HiringAssistantChatbot
from utils import sanitize_input, format_candidate_info
from config import APP_TITLE, APP_DESCRIPTION

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Enhanced Professional CSS with WIDER MAIN CONTAINERS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* WIDER PROGRESS CONTAINER */
    .progress-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border: 1px solid #e1e5eb;
        width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* WIDER CHAT CONTAINER */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #e1e5eb;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* WIDER USER MESSAGE */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 22px 22px 6px 22px;
        margin: 1.2rem 0;
        margin-left: 2rem; /* Reduced margin for more width */
        margin-right: 1rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        position: relative;
        animation: slideInRight 0.4s ease-out;
        max-width: 90%; /* Increased width */
    }
    
    /* WIDER BOT MESSAGE */
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333;
        padding: 1.2rem 1.8rem;
        border-radius: 22px 22px 22px 6px;
        margin: 1.2rem 0;
        margin-right: 2rem; /* Reduced margin for more width */
        margin-left: 1rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        position: relative;
        animation: slideInLeft 0.4s ease-out;
        max-width: 90%; /* Increased width */
    }
    
    /* WIDER INFO BOX */
    .info-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 18px;
        padding: 2.5rem;
        margin: 2rem auto;
        color: #155724;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.15);
        width: 95%;
    }
    
    /* WIDER INPUT CONTAINER */
    .input-container {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        border: 2px solid #e9ecef;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    
    .input-container:focus-within {
        border-color: #667eea;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        font-size: 1rem;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    .sidebar-section {
        background: white;
        border-radius: 18px;
        padding: 1.8rem;
        margin-bottom: 1.8rem;
        border: 1px solid #e1e5eb;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HiringAssistantChatbot()
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

def display_header():
    """Display application header"""
    st.markdown(f'<div class="main-header">{APP_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{APP_DESCRIPTION}</div>', unsafe_allow_html=True)

def display_progress():
    """Display conversation progress"""
    if hasattr(st.session_state, 'conversation_state'):
        current_step, total_steps = st.session_state.chatbot.get_conversation_progress()
        
        with st.container():
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 4, 1])
            
            with col1:
                st.markdown("## 📊 **Progress**")
            
            with col2:
                progress_percentage = (current_step - 1) / (total_steps - 1) if total_steps > 1 else 0
                st.progress(progress_percentage)
                st.markdown(f"**Step {current_step} of {total_steps} completed**")
            
            with col3:
                st.markdown(f"## **{int(progress_percentage * 100)}%**")
            
            st.markdown('</div>', unsafe_allow_html=True)

def display_chat_history():
    """Display chat conversation history"""
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for chat in st.session_state.chat_history:
            if chat['role'] == 'user':
                st.markdown(
                    f'<div class="user-message">'
                    f'<div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 600;">👤 YOU</div>'
                    f'{chat["message"]}'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="bot-message">'
                    f'<div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 600;">🤖 TALENTSCOUT ASSISTANT</div>'
                    f'{chat["message"]}'
                    f'</div>', 
                    unsafe_allow_html=True
                )
        
        # Auto-scroll to bottom
        st.markdown("""
        <script>
            var chatContainer = window.parent.document.querySelector('.chat-container');
            if (chatContainer) {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        </script>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with ALL candidate information and controls"""
    with st.sidebar:
        # Session Information
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 📋 **Session Information**")
        
        if 'candidate_data' in st.session_state and st.session_state.candidate_data:
            st.markdown("### 🧑‍💼 Candidate Details")
            candidate_info = format_candidate_info(st.session_state.candidate_data)
            st.markdown(candidate_info)
            
            # Additional candidate stats
            if st.session_state.candidate_data.get('experience'):
                exp = st.session_state.candidate_data['experience']
                st.markdown(f"**Experience Level:** {'Junior' if exp < 3 else 'Mid-level' if exp < 6 else 'Senior'}")
            
            if st.session_state.candidate_data.get('tech_stack_parsed'):
                tech_data = st.session_state.candidate_data['tech_stack_parsed']
                tech_count = sum(len(skills) for category, skills in tech_data.items() if category != 'soft_skills')
                soft_count = len(tech_data.get('soft_skills', []))
                st.markdown(f"**Technical Skills:** {tech_count}")
                st.markdown(f"**Soft Skills:** {soft_count}")
        else:
            st.markdown("### 🧑‍💼 Candidate Details")
            st.info("No candidate information collected yet. Start the screening process to begin.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress Tracking
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 📈 **Progress Tracking**")
        
        if hasattr(st.session_state, 'conversation_state'):
            current_step, total_steps = st.session_state.chatbot.get_conversation_progress()
            
            progress_percentage = (current_step - 1) / (total_steps - 1) if total_steps > 1 else 0
            st.progress(progress_percentage)
            
            st.markdown(f"**Current Progress:** {current_step}/{total_steps} steps")
            st.markdown(f"**Completion:** {int(progress_percentage * 100)}%")
            
            # Detailed phase information
            state_details = {
                'greeting': '**Phase:** Initial Welcome\n**Status:** Introduction and setup',
                'collecting_name': '**Phase:** Personal Information\n**Status:** Collecting candidate name',
                'collecting_email': '**Phase:** Contact Details\n**Status:** Email verification',
                'collecting_phone': '**Phase:** Phone Verification\n**Status:** 10-digit number validation',
                'collecting_experience': '**Phase:** Professional Background\n**Status:** Years of experience',
                'collecting_position': '**Phase:** Career Interests\n**Status:** Desired positions',
                'collecting_location': '**Phase:** Location Info\n**Status:** Work location preferences',
                'collecting_tech_stack': '**Phase:** Skills Assessment\n**Status:** Technical & soft skills',
                'asking_questions': '**Phase:** Technical Evaluation\n**Status:** Skill-based questions',
                'completed': '**Phase:** Screening Complete\n**Status:** Final assessment done'
            }
            
            current_state_detail = state_details.get(st.session_state.conversation_state, '**Phase:** Starting\n**Status:** Initializing session')
            st.markdown(current_state_detail)
            
            # Next steps preview
            if current_step < total_steps:
                next_steps_info = {
                    1: "**Next:** Contact information collection",
                    2: "**Next:** Phone number verification", 
                    3: "**Next:** Professional experience assessment",
                    4: "**Next:** Career position preferences",
                    5: "**Next:** Location information",
                    6: "**Next:** Technical skills evaluation",
                    7: "**Next:** Soft skills assessment",
                    8: "**Next:** Technical questions session",
                    9: "**Next:** Final review and completion"
                }
                if current_step in next_steps_info:
                    st.markdown(next_steps_info[current_step])
        else:
            st.info("Start the screening process to track your progress.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Session Statistics
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 📊 **Session Statistics**")
        
        if 'chat_history' in st.session_state:
            total_messages = len(st.session_state.chat_history)
            user_messages = len([m for m in st.session_state.chat_history if m['role'] == 'user'])
            bot_messages = len([m for m in st.session_state.chat_history if m['role'] == 'assistant'])
            
            st.markdown(f"**Total Messages:** {total_messages}")
            st.markdown(f"**Your Responses:** {user_messages}")
            st.markdown(f"**Assistant Messages:** {bot_messages}")
            
            if 'technical_questions' in st.session_state:
                st.markdown(f"**Technical Questions:** {len(st.session_state.technical_questions)}")
            
            if 'current_question_index' in st.session_state:
                st.markdown(f"**Questions Answered:** {st.session_state.current_question_index}")
        else:
            st.markdown("**Total Messages:** 0")
            st.markdown("**Your Responses:** 0")
            st.markdown("**Assistant Messages:** 0")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Requirements & Validation
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## ✅ **Requirements & Validation**")
        
        st.markdown("""
        ### 📧 Email Requirements
        - Valid format: name@example.com
        - Must contain @ symbol
        - Proper domain extension
        
        ### 📞 Phone Requirements  
        - Exactly 10 digits
        - Country code not required
        - Format: 1234567890 or (123) 456-7890
        
        ### 🛠️ Skills Requirements
        - Minimum 3 skills required
        - Mix of technical and soft skills
        - Separate with commas
        - Examples: Python, JavaScript, Communication
        
        ### 📍 Location Requirements
        - City, State, or Country
        - Meaningful location names
        - No special characters only
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Controls & Actions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## ⚙️ **Session Controls**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 New Session", use_container_width=True, help="Start a completely new screening session"):
                for key in ['conversation_state', 'candidate_data', 'technical_questions', 
                           'current_question_index', 'chat_history', 'conversation_started', 'input_key']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.chatbot = HiringAssistantChatbot()
                st.rerun()
        
        with col2:
            if st.button("📊 Export Data", use_container_width=True, help="Export session data (Feature)"):
                st.info("Export feature coming soon!")
        
        if st.button("🆘 Get Help", use_container_width=True, help="Display help information"):
            st.info("Type your answers clearly. Follow the format requirements. Contact support if needed.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Tips
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("## 💡 **Quick Tips & Guide**")
        
        st.markdown("""
        ### Best Practices:
        - **Answer promptly** - Keep the conversation flowing
        - **Be specific** - Detailed answers get better assessment
        - **Follow formats** - Use proper email and phone formats
        - **List skills clearly** - Separate with commas for best parsing
        
        ### Session Flow:
        1. **Personal Info** → Name, Contact details
        2. **Professional** → Experience, Positions
        3. **Location** → Work preferences  
        4. **Skills** → Technical & soft skills assessment
        5. **Technical Q&A** → Skill verification
        6. **Completion** → Final review
        
        ### Need Help?
        - Ensure stable internet connection
        - Reload if session freezes
        - Use proper input formats
        - Contact: support@talentscout.ai
        """)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    init_session_state()
    
    # Display header
    display_header()
    
    # Create main layout - 80% main, 20% sidebar
    main_col, sidebar_col = st.columns([4, 1])
    
    with main_col:
        # Display progress
        display_progress()
        
        # Start conversation if not started
        if not st.session_state.conversation_started:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("## 🚀 Ready to Begin Your Professional Screening?")
            st.markdown("""
            Start your comprehensive screening process by clicking the button below. 
            This AI-powered assessment will evaluate your qualifications through a structured conversation.
            
            **What to expect during screening:**
            - Personal & contact information collection
            - Professional background assessment  
            - Technical skills evaluation
            - Career preference discussion
            - Location preferences
            - Final technical assessment
            - Comprehensive review
            
            **Time required:** 5-10 minutes
            **All data is handled securely and privately**
            """)
            
            if st.button("🎯 Start Professional Screening", type="primary", use_container_width=True):
                greeting = st.session_state.chatbot.generate_greeting()
                st.session_state.chatbot.add_to_chat_history("assistant", greeting)
                st.session_state.conversation_started = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display chat history
        if st.session_state.conversation_started:
            display_chat_history()
            
            # Input area - FIXED SESSION STATE ISSUE
            if hasattr(st.session_state, 'conversation_state') and st.session_state.conversation_state != 'completed':
                st.markdown("## 💬 Your Response")
                
                st.markdown('<div class="input-container">', unsafe_allow_html=True)
                
                # Use dynamic key to avoid session state conflicts
                user_input = st.text_area(
                    "Type your response here:",
                    value="",
                    height=130,
                    key=f"user_input_{st.session_state.input_key}",
                    placeholder="💡 Type your detailed answer here...\n\nBe specific and provide comprehensive responses for better assessment of your qualifications.",
                    label_visibility="collapsed"
                )
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("📤 Submit Response", type="primary", use_container_width=True, key="submit_btn"):
                        if user_input.strip():
                            # Add user message to chat history
                            st.session_state.chatbot.add_to_chat_history("user", user_input.strip())
                            
                            # Generate bot response
                            bot_response = st.session_state.chatbot.process_user_input(user_input.strip())
                            
                            # Add bot response to chat history
                            st.session_state.chatbot.add_to_chat_history("assistant", bot_response)
                            
                            # Change input key to clear the input for next question
                            st.session_state.input_key += 1
                            st.rerun()
                
                with col2:
                    if st.button("❌ End Session", use_container_width=True, key="end_btn"):
                        ending_message = st.session_state.chatbot.handle_conversation_end()
                        st.session_state.chatbot.add_to_chat_history("assistant", ending_message)
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            elif hasattr(st.session_state, 'conversation_state') and st.session_state.conversation_state == 'completed':
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("""
                ## ✅ Screening Successfully Completed!
                
                **Thank you for completing the comprehensive TalentScout screening process!**
                
                ### Next Steps:
                - **Technical Review:** Our team will review your responses (2-3 business days)
                - **Email Notification:** You'll receive application status updates
                - **Possible Interview:** Selected candidates will be contacted for technical interviews
                - **Career Matching:** Your profile will be matched with suitable opportunities
                
                ### Your Information:
                All your details have been recorded securely. You'll hear back from us soon regarding next steps in the recruitment process.
                
                **For any queries, contact: recruitment@talentscout.ai**
                """)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with sidebar_col:
        display_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #6c757d; font-size: 0.9rem; padding: 2rem;">'
        '🤖 **TalentScout AI Hiring Assistant** v2.0 | Powered by Advanced AI | '
        'Secure & Confidential Screening | '
        '<a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">Privacy Policy</a> | '
        '<a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">Contact Support</a>'
        '</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
