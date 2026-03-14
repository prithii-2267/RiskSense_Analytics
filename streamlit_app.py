import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from google import genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RiskSense Executive | logicX",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CSS (High Contrast & Professional UI) ---
# This ensures visibility in both Light and Dark browser themes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Force Metric Cards to White Background with Dark Text */
    [data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    }

    /* Metric Label (Title) */
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* Metric Value (The Numbers) */
    [data-testid="stMetricValue"] {
        color: #1E293B !important;
        font-weight: 700 !important;
    }
    
    /* Professional Sidebar */
    .stSidebar { background-color: #1E293B !important; color: white !important; }
    .stSidebar [data-testid="stMarkdownContainer"] p { color: #CBD5E1 !important; }
    
    /* Custom Button Style */
    .stButton>button {
        background: #1E293B;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
        width: 100%;
        font-weight: 600;
    }
    .stButton>button:hover { background: #334155; color: white; transform: translateY(-1px); border: none; }
    
    /* AI Result Box Styling */
    .ai-box {
        background: #FFFFFF; 
        border-left: 5px solid #1E293B; 
        padding: 25px; 
        border-radius: 8px; 
        color: #1E293B; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI BACKEND SETUP ---
client = genai.Client(api_key="AIzaSyA0UXPmaMu6AYWvDA4T247ICI5d5H9rsZ4")

# --- 4. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🛡️ Parameters")
    budget = st.slider("Total Budget ($)", 50000, 500000, 125000, format="$%d")
    hours = st.slider("Resource Allocation (Hours)", 0, 1000, 300)
    complexity = st.select_slider("Project Complexity", options=["Standard", "Advanced", "Enterprise"])
    st.divider()
    st.caption("Algorithm Version: v2.4.2 (Stable)")
    st.caption("Environment: logicX Production")

# --- 5. RISK ENGINE LOGIC ---
base_score = (hours * 0.1) - (budget * 0.0002)
comp_mod = 1.0 if complexity == "Standard" else 1.3 if complexity == "Advanced" else 1.7
risk_index = min(max(base_score * comp_mod, 5), 98)

# --- 6. DASHBOARD HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("RiskSense Analytics")
    st.markdown("**Predictive Governance Engine** | Real-time Assessment for Data-Driven Projects")
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data"):
        st.rerun()

st.divider()

# --- 7. TOP ROW: KPI METRICS ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Risk Index", f"{risk_index:.1f}%", delta="Normal" if risk_index < 40 else "Critical", delta_color="inverse")
k2.metric("Efficiency Ratio", f"{100-(hours/15):.1f}%", delta="-1.4%")
k3.metric("Project Budget", f"${budget/1000:.0f}k", delta="Target Reach")
k4.metric("Resource Load", f"{(hours/10):.0f}%", delta="High" if hours > 700 else "Stable")

# --- 8. MAIN CONTENT: GAUGE & AI ---
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("Vulnerability Assessment")
    
    # High-Contrast Gauge (Optimized for Dark & Light Themes)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_index,
        number = {'font': {'color': "#F8FAFC", 'size': 85}}, # Bright center number
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "#F8FAFC", 'tickwidth': 2},
            'bar': {'color': "#F8FAFC"}, 
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#475569", 
            'steps': [
                {'range': [0, 35], 'color': '#22C55E'},  # Vibrant Green
                {'range': [35, 70], 'color': '#EAB308'}, # Vibrant Yellow
                {'range': [70, 100], 'color': '#EF4444'} # Vibrant Red
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 90}
        }))
    
    fig.update_layout(
        height=450, 
        margin=dict(l=30, r=30, t=50, b=0),
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#F8FAFC", 'family': "Inter"} 
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🤖 AI Mitigation Blueprint")
    
    gen_btn = st.button("Generate Executive Brief")
    
    if not gen_btn:
        st.markdown("""
            <div style="background: rgba(255,255,255,0.05); border: 1px dashed #475569; padding: 40px; border-radius: 12px; text-align: center; color: #94A3B8;">
                <p style="font-size: 1.2rem; margin-bottom: 5px;">Analysis Engine Ready</p>
                <p style="font-size: 0.8rem;">Click the button to process parameters with logicX AI</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Processing Strategy..."):
            try:
                # --- ONLINE MODE: 200-WORD DYNAMIC AI ANALYSIS ---
                prompt = (
                    f"Act as a Senior AI Project Auditor. Analyze: Risk Index {risk_index:.1f}%, "
                    f"Complexity {complexity}, Budget ${budget:,}. Write a 200-word professional "
                    f"executive synthesis. Use formal terminology like 'non-linear risk trajectory,' "
                    f"'governance pivot,' and '10x AI Tax.' Explain how to stabilize the project. "
                    f"Ensure the tone is high-level, strategic, and dense with professional advice."
                )
                
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                ai_output = response.text
                status_label = "🟢 ONLINE: Gemini 2.0 Active"
                
            except Exception:
                # --- OFFLINE MODE: 200-WORD HEURISTIC SYNTHESIS ---
                status_label = "🟡 OFFLINE: Heuristic Logic Activated"
                ai_output = f"""
                The logicX engine has detected a critical threshold within the project’s Vulnerability Index, standing at {risk_index:.1f}%. 
                Under {complexity} complexity, the delta between resource hours and the ${budget:,} budget indicates a non-linear risk trajectory. 
                To mitigate this '10x AI Tax,' we initiate a three-tier governance pivot. 

                First, **Operational Decoupling**: We recommend transitioning from monolithic development to a modular sprint architecture. 
                This limits technical debt accumulation and allows for real-time adjustments to the scope-to-budget ratio. Second, 
                **Financial Guardrail Implementation**: Given the current capital allocation, a 15% contingency reserve must be ring-fenced 
                immediately to absorb volatility inherent in {complexity}-level projects. 

                Third, **Resource Load Balancing**: The current allocation of hours must be re-optimized. By shifting 20% of non-critical 
                path tasks to automated workflows or deferred sprints, the project can regain a sustainable velocity. This heuristic 
                analysis serves as a quantitative baseline for executive decision-making, ensuring that despite network latency or 
                API unavailability, the project remains grounded in predictive governance principles. This synthesis transforms raw 
                metrics into a strategic roadmap, securing delivery and ensuring long-term project survival.
                """
            
            # --- DISPLAY BLOCK ---
            st.caption(status_label)
            st.markdown(f"""
                <div class="ai-box">
                    <strong style="color: #1E293B; font-size: 1.1rem; display: block; margin-bottom: 10px;">logicX Strategy Brief:</strong>
                    <div style="font-size: 0.95rem; line-height: 1.6; color: #1E293B;">
                        {ai_output}
            """, unsafe_allow_html=True)
# --- 9. DATA MATRIX ---
st.divider()
with st.expander("🔍 View Raw Parameter Matrix"):
    raw_data = pd.DataFrame({
        "Metric Variable": ["Operational Budget", "Allocated Hours", "Execution Complexity", "Final Risk Score"],
        "Current Value": [f"${budget:,}", f"{hours}h", complexity, f"{risk_index:.2f}%"],
        "Safety Threshold": ["$50k min", "1000h max", "Standard/Enterprise", "< 75%"]
    })
    st.table(raw_data)

# --- 10. FOOTER ---
st.markdown("<br>", unsafe_allow_html=True)
st.caption("Developed by **logicX** | Agentic AI Integration")