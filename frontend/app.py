import streamlit as st
import requests
import time
import uuid

st.set_page_config(
    page_title="Research Genie",
    page_icon="🧞‍♂️",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

def send_message_to_backend(message: str):
    try:
        response = requests.post(
            "http://localhost:8000/chat/",
            json={"message": message, "thread_id": st.session_state.thread_id},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "No response received")
        else:
            return f"Error: {response.status_code}"
    except:
        return "❌ Cannot connect to backend server."

with st.sidebar:
    st.title("🧞‍♂️ Research Genie")
    st.caption("Your AI-Powered Research Assistant")

    st.markdown("---")

    st.subheader("🚀 Core Features")
    
    with st.expander("🔍 **Smart Paper Search**", expanded=False):
        st.markdown("""
        - Search arXiv database instantly
        - Find papers by keywords, authors, or topics
        - Get comprehensive paper summaries
        - Access full paper content
        """)
    
    with st.expander("📖 **PDF Analysis & Reading**", expanded=False):
        st.markdown("""
        - Extract text from research papers
        - Analyze methodology and findings
        - Summarize key contributions
        - Identify research gaps
        """)
    
    with st.expander("✍️ **Research Paper Generation**", expanded=False):
        st.markdown("""
        - Generate comprehensive papers (8+ pages)
        - Include all standard sections
        - Add mathematical formulations
        - Create professional references
        """)
    
    with st.expander("📄 **Professional PDF Export**", expanded=False):
        st.markdown("""
        - LaTeX-based PDF generation
        - Publication-ready formatting
        - Proper citations and bibliography
        - Mathematical equations support
        """)

    st.markdown("---")

    st.subheader("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True, help="Clear all conversation history"):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

    with col2:
        if st.button("🔄 New Session", use_container_width=True, help="Start fresh conversation"):
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

    st.markdown("---")

    st.subheader("📊 Session Info")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Session", "Active" if st.session_state.messages else "New")

    st.markdown("---")

    st.subheader("📋 How to Use")
    
    with st.expander("🎯 **Getting Started**", expanded=False):
        st.markdown("""
        **Step 1:** Search for papers
        - "Search for papers about machine learning"
        - "Find research on neural networks"
        
        **Step 2:** Select a paper
        - "I'm interested in the 3rd paper"
        - "Tell me more about the first one"
        
        **Step 3:** Generate new research
        - Confirm when asked to write a paper
        - Request PDF generation when ready
        """)
    
    with st.expander("💡 **Example Queries**", expanded=False):
        st.markdown("""
        - "Search for recent papers on transformers"
        - "Find research about climate change modeling"
        - "Look for papers by Geoffrey Hinton"
        - "Search for quantum computing algorithms"
        - "Find papers about computer vision"
        """)

    st.markdown("---")

    st.subheader("🎓 Pro Tips")
    st.info("""
    💡 **Tip:** Be specific in your search queries for better results
    
    🎯 **Tip:** You can refer to papers by number (e.g., "the 2nd paper")
    
    ⚡ **Tip:** Ask for PDF generation after paper writing is complete
    """)

    st.markdown("---")

    st.caption("🤖 Powered by AI • Built for Researchers")
    st.caption(f"💬 Ready to help with your research needs!")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <h1 style="font-size: 4rem; margin: 0; display: flex; align-items: center; justify-content: center; gap: 1rem;">
            🧞‍♂️ 
            <span style="color: #2c3e50; font-weight: 700;">
                Research Genie
            </span>
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0.5rem 0 0 0; font-weight: 300;">
            ✨ Your AI-Powered Research Assistant ✨
        </p>
        <p style="font-size: 1rem; color: #888; margin: 0.5rem 0 2rem 0;">
            🔬 Search • 📖 Analyze • ✍️ Generate • 📄 Export
        </p>
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                border-radius: 15px; margin: 2rem 0; border: 1px solid #dee2e6;">
        <h3 style="color: #495057; margin-bottom: 1rem;">👋 Welcome to Research Genie!</h3>
        <p style="color: #6c757d; margin-bottom: 1.5rem; font-size: 1.1rem;">
            I'm here to help you with all your research needs. Let's get started!
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 1.5rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-weight: 600; color: #495057;">Search Papers</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Find relevant research</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📖</div>
                <div style="font-weight: 600; color: #495057;">Analyze Content</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Deep paper analysis</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✍️</div>
                <div style="font-weight: 600; color: #495057;">Generate Papers</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Create new research</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📄</div>
                <div style="font-weight: 600; color: #495057;">Export PDF</div>
                <div style="font-size: 0.9rem; color: #6c757d;">Professional format</div>
            </div>
        </div>
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(13, 110, 253, 0.1); 
                    border-radius: 10px; border-left: 4px solid #0d6efd;">
            <p style="margin: 0; color: #0d6efd; font-weight: 500;">
                💡 Try saying: "Search for papers about machine learning" or "Find research on climate change"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about research..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🧞‍♂️ Research Genie is thinking..."):
            response = send_message_to_backend(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()
