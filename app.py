import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Configuration
st.set_page_config(
    page_title="GenZ Mental Health Advice & Analytics Engine", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern Advice Blocks
st.markdown("""
<style>
    .advice-header {
        font-size: 20px;
        font-weight: bold;
        color: #1E1B4B;
        margin-bottom: 10px;
    }
    .low-stress {
        background-color: #f0fdf4;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #16a34a;
        margin-bottom: 15px;
    }
    .med-stress {
        background-color: #fffbeb;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #d97706;
        margin-bottom: 15px;
    }
    .high-stress {
        background-color: #fef2f2;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #dc2626;
        margin-bottom: 15px;
    }
    .slang-chip {
        background-color: #e0e7ff;
        color: #4338ca;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        display: inline-block;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Adaptive GenZ Stress Response & Analytics Engine")
st.write("Input your customized metrics to receive conversational tactics and see how your mental health markers compare to the 2026 GenZ dataset.")

# --- 1. DATASET LOADING ---
@st.cache_data
def load_data():
    filename = "GenZ_Social_Media_Mental_Health_2026 (1).csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        st.error(f"⚠️ Dataset '{filename}' not found in the directory.")
        # Fallback empty dataframe to prevent hard crashes
        return pd.DataFrame(columns=[
            'user_id', 'age', 'gender', 'daily_screen_time_hours', 
            'primary_platform', 'sleep_hours', 'stress_level', 
            'anxiety_score', 'depression_score', 'academic_performance', 'social_activity_hours'
        ])

df = load_data()

# --- 2. SIDEBAR CONFIGURATION ---
st.sidebar.markdown("### 🛠️ Global GenZ Analytics (2026)")
if not df.empty:
    st.sidebar.write(f"**Total Respondents:** {len(df)}")
    st.sidebar.write(f"**Avg Age:** {df['age'].mean():.1f} years")
    st.sidebar.write(f"**Avg Screen Time:** {df['daily_screen_time_hours'].mean():.1f} hrs/day")
    st.sidebar.write(f"**Avg Stress Level:** {df['stress_level'].mean():.1f} / 10")
    
    top_platform = df['primary_platform'].mode()[0]
    st.sidebar.write(f"**Top Platform:** {top_platform}")
else:
    st.sidebar.warning("Dataset not found. Analytics unavailable.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Balance Target")
st.sidebar.write("• **60%** Negative/Anxious Spectrum")
st.sidebar.write("• **40%** Positive/Neutral Spectrum")

# --- 3. HIGH LEVEL OVERVIEW ---
st.subheader("📌 System & Data Overview")
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric(label="Total Database Records", value=f"{len(df)} Profiles")
with col_stat2:
    st.metric(label="Target Demographic", value="Teenagers / Gen-Z")
with col_stat3:
    st.metric(label="Emergency Response Line", value="1-800-273-8255")

st.markdown("---")

# --- 4. INTERACTIVE STRESS CONTROL CENTER ---
st.markdown("### 📋 Step 1: Input Your Metrics")
with st.form("advice_generator_form"):
    
    # Large responsive slider
    user_stress = st.slider(
        "Select Current Stress Level Baseline (1-10):", 
        min_value=1, max_value=10, value=5,
        help="1-3: Low/Manageable | 4-7: Moderate/Validation Needed | 8-10: High/Action Required"
    )
    
    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        platforms = df['primary_platform'].unique().tolist() if not df.empty else ["Instagram", "TikTok", "X", "YouTube", "LinkedIn"]
        user_platform = st.selectbox("Primary Social Platform:", platforms)
    with col_input2:
        user_screen_time = st.number_input("Daily Screen Time (Hours):", min_value=0.0, max_value=24.0, value=4.5, step=0.5)
    with col_input3:
        user_sleep = st.number_input("Average Sleep (Hours):", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        
    use_slang_responses = st.checkbox("Mirror Relatable Teen Tone/Slang phrases", value=True)
    
    submit_btn = st.form_submit_button(label="🎯 Generate Targeted Advice & Analytics")


# --- 5. ADAPTIVE ADVICE & SIMULATION OUTPUT ---
if submit_btn:
    st.markdown("---")
    st.markdown(f"## ⚡ Strategy Engine Output for Stress Level {user_stress}/10")
    
    # Categorize Advice Tiers
    if user_stress <= 3:
        st.markdown(f"""
        <div class="low-stress">
            <div class="advice-header">🟢 Tier 1 Strategy: Reinforce Positive/Neutral Resilience</div>
            <p>Your current level falls within the dataset's lower stress tier. Focus is placed on positive validation and emotional grounding strategies.</p>
            <ul>
                <li><b>Actionable Advice:</b> Remind yourself of small positive events. You are currently logging <b>{user_sleep} hours of sleep</b>—keep prioritizing rest!</li>
                <li><b>Mental Exercise:</b> Grounding exercise. Step back from <b>{user_platform}</b> for 15 minutes to reset your cognitive baselines.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif 4 <= user_stress <= 7:
        st.markdown(f"""
        <div class="med-stress">
            <div class="advice-header">🟡 Tier 2 Strategy: Active Validation & Supportive Venting</div>
            <p>Your situation maps into the core moderate emotional range of the dataset. Active validation is prioritized over direct problem-solving.</p>
            <ul>
                <li><b>Actionable Advice:</b> It is completely valid to feel overwhelmed right now, especially balancing <b>{user_screen_time} hours</b> of screen time. Do not force immediate toxic positivity; allow space to vent.</li>
                <li><b>Mental Exercise:</b> Brain-dump journal. Spend 5 minutes writing down every single item causing cognitive friction, then visually separate what you can control from what you cannot.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown(f"""
        <div class="high-stress">
            <div class="advice-header">🔴 Tier 3 Strategy: Escalation Protocol & Crisis De-escalation</div>
            <p>Critical distress marker detected. Automated safety systems must bypass casual dialogue scripts and switch to explicit protective guidance.</p>
            <ul>
                <li><b>Actionable Advice:</b> High-intensity stress spikes require human-in-the-loop support networks. Consider muting <b>{user_platform}</b> notifications immediately and reach out to trusted peers, family, or counselors.</li>
                <li><b>Emergency Resource:</b> If thoughts turn toward self-harm or feel completely unmanageable, connect with the structured support line immediately at <b>1-800-273-8255</b>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Tone Profile Summary Visual Blocks
    st.markdown("### 💬 Conversational Tone Adjustment Matrix")
    if use_slang_responses:
        st.markdown("""
        <span class="slang-chip">"freaking out" mirroring allowed</span>
        <span class="slang-chip">"vent" context triggers on</span>
        <span class="slang-chip">"spill the tea" casual phrasing active</span>
        <span class="slang-chip">"touch grass" reality check active</span>
        """, unsafe_allow_html=True)
        st.caption("Approachable, peer-level framing is turned on to make the support advice feel organic.")
    else:
        st.markdown('<span class="slang-chip">Standard Professional English Mode</span>', unsafe_allow_html=True)
        st.caption("Standard clinical validation layout selected.")

    # --- 6. INTERACTIVE GAUGES & CHARTS ---
    st.markdown("---")
    st.markdown("### 📊 Deep Analytics: How You Compare to the 2026 Cohort")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Generate dynamic Plotly Gauge chart
        avg_dataset_stress = df['stress_level'].mean() if not df.empty else 5
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = user_stress,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Your Stress vs Dataset Average", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#4338ca"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [1, 3.9], 'color': '#f0fdf4'},
                    {'range': [4, 7.9], 'color': '#fffbeb'},
                    {'range': [8, 10], 'color': '#fef2f2'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': avg_dataset_stress
                }
            }
        ))
        
        fig_gauge.update_layout(height=350, margin=dict(t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(f"The black line represents the dataset average stress level ({avg_dataset_stress:.1f}).")

    with col_chart2:
        if not df.empty:
            # Scatter Plot: Screen Time vs Stress
            fig_scatter = px.scatter(
                df, x="daily_screen_time_hours", y="stress_level", 
                color="primary_platform", opacity=0.6,
                title="Screen Time vs. Stress by Platform",
                labels={
                    "daily_screen_time_hours": "Daily Screen Time (hrs)", 
                    "stress_level": "Stress Level (1-10)",
                    "primary_platform": "Platform"
                }
            )
            
            # Add a bold marker for the user's explicit input
            fig_scatter.add_trace(go.Scatter(
                x=[user_screen_time], y=[user_stress],
                mode='markers', marker=dict(color='black', size=16, symbol='star'),
                name='You'
            ))
            
            fig_scatter.update_layout(height=350, margin=dict(t=40, b=10))
            st.plotly_chart(fig_scatter, use_container_width=True)

    if not df.empty:
        st.markdown("#### 🧠 Platform Mental Health Impact Analysis")
        # Bar chart analyzing Anxiety & Depression scores across different platforms
        platform_stats = df.groupby('primary_platform')[['anxiety_score', 'depression_score']].mean().reset_index()
        fig_bar = px.bar(
            platform_stats, x='primary_platform', y=['anxiety_score', 'depression_score'],
            barmode='group', title="Average Anxiety & Depression Scores by Primary Platform",
            labels={"value": "Average Score", "primary_platform": "Platform", "variable": "Mental Health Metric"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Closing dynamic data insight
        avg_sleep_platform = df[df['primary_platform'] == user_platform]['sleep_hours'].mean()
        st.info(f"**Data Insight:** The dataset shows that users whose primary platform is **{user_platform}** average **{avg_sleep_platform:.1f} hours** of sleep. You reported **{user_sleep} hours**.")

else:
    st.info("💡 Adjust the metrics above and press **'Generate Targeted Advice & Analytics'** to simulate the protocols and generate dataset insights.")
