import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GenZ Mental Health & Social Media Analytics", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR UI ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1E1B4B; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #4f46e5; }
    .insight-box { background-color: #e0e7ff; padding: 20px; border-radius: 10px; border-left: 6px solid #4338ca; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Adjust path if you put it inside a 'data' folder
    filename = "GenZ_Social_Media_Mental_Health_2026.csv" 
    if os.path.exists(filename):
        return pd.read_csv(filename)
    elif os.path.exists(f"data/{filename}"):
        return pd.read_csv(f"data/{filename}")
    else:
        st.error(f"⚠️ Dataset '{filename}' not found. Please ensure it is in the correct folder.")
        return pd.DataFrame()

df = load_data()

# --- SIDEBAR: EXPLICIT USER INPUTS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
st.sidebar.title("👤 Your Profile Input")
st.sidebar.info("Enter your details to see how you compare against the 2026 GenZ cohort.")

with st.sidebar.form("user_input_form"):
    user_age = st.number_input("Age", min_value=13, max_value=30, value=20)
    
    genders = df['gender'].unique().tolist() if not df.empty else ["Male", "Female", "Other"]
    user_gender = st.selectbox("Gender", genders)
    
    platforms = df['primary_platform'].unique().tolist() if not df.empty else ["Instagram", "TikTok", "YouTube", "X", "LinkedIn"]
    user_platform = st.selectbox("Primary Platform", platforms)
    
    user_screen_time = st.slider("Daily Screen Time (Hours)", 0.0, 16.0, 5.0, 0.5)
    user_sleep = st.slider("Average Sleep (Hours)", 0.0, 12.0, 7.0, 0.5)
    user_stress = st.slider("Current Stress Level (1-10)", 1, 10, 5)
    
    submit_btn = st.form_submit_button("Compare My Profile 📊")

# --- MAIN DASHBOARD ---
st.title("🧠 GenZ Social Media & Mental Health (2026)")
st.write("Deep analytics exploring the relationship between screen time, platform choice, and mental wellbeing.")

if not df.empty:
    # --- GLOBAL KPIs ---
    st.markdown("### 🌍 Global Cohort Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Surveyed", f"{len(df):,}")
    col2.metric("Avg Screen Time", f"{df['daily_screen_time_hours'].mean():.1f} hrs")
    col3.metric("Avg Stress Level", f"{df['stress_level'].mean():.1f} / 10")
    col4.metric("Top Platform", df['primary_platform'].mode()[0])

    st.markdown("---")

    # --- PERSONAL COMPARISON SECTION ---
    if submit_btn:
        st.markdown(f"### 🎯 Your Profile vs. The Dataset")
        
        # Determine if user is above or below average
        avg_screen = df['daily_screen_time_hours'].mean()
        avg_sleep = df['sleep_hours'].mean()
        
        screen_diff = "above" if user_screen_time > avg_screen else "below"
        sleep_diff = "above" if user_sleep > avg_sleep else "below"
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 Personalized Insight</h4>
            You are spending <b>{user_screen_time} hours</b> on screen daily, which is <b>{screen_diff}</b> the GenZ average of {avg_screen:.1f} hours. 
            You are sleeping <b>{user_sleep} hours</b>, which is <b>{sleep_diff}</b> the average of {avg_sleep:.1f} hours. 
            Users on <b>{user_platform}</b> report an average stress level of {df[df['primary_platform'] == user_platform]['stress_level'].mean():.1f}/10.
        </div>
        """, unsafe_allow_html=True)

        col_gauge, col_scatter = st.columns(2)
        
        with col_gauge:
            # Gauge Chart for Stress
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = user_stress,
                delta = {'reference': df['stress_level'].mean(), 'position': "top"},
                title = {'text': "Your Stress vs Average", 'font': {'size': 18}},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "#4f46e5"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [1, 4], 'color': '#d1fae5'},
                        {'range': [4, 7], 'color': '#fef3c7'},
                        {'range': [7, 10], 'color': '#fee2e2'}
                    ],
                }
            ))
            fig_gauge.update_layout(height=350, margin=dict(t=50, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_scatter:
            # Scatter plot showing where the user lands
            fig_scatter = px.scatter(
                df, x="daily_screen_time_hours", y="sleep_hours", 
                color="primary_platform", opacity=0.3,
                title="Screen Time vs. Sleep (Star = YOU)",
                labels={"daily_screen_time_hours": "Screen Time (hrs)", "sleep_hours": "Sleep (hrs)"}
            )
            # Add user marker
            fig_scatter.add_trace(go.Scatter(
                x=[user_screen_time], y=[user_sleep],
                mode='markers', marker=dict(color='black', size=18, symbol='star', line=dict(width=2, color='white')),
                name='You'
            ))
            fig_scatter.update_layout(height=350, margin=dict(t=50, b=10))
            st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    
    # --- DEEP ANALYTICS CHARTS ---
    st.markdown("### 📊 Deep Cohort Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Mental Health by Platform", "Screen Time Impact", "Academic Performance"])
    
    with tab1:
        st.markdown("#### Anxiety & Depression Scores Across Platforms")
        platform_mh = df.groupby('primary_platform')[['anxiety_score', 'depression_score']].mean().reset_index()
        fig_bar = px.bar(
            platform_mh, x='primary_platform', y=['anxiety_score', 'depression_score'],
            barmode='group', color_discrete_sequence=['#4f46e5', '#ec4899']
        )
        fig_bar.update_layout(xaxis_title="Platform", yaxis_title="Average Score")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with tab2:
        st.markdown("#### Screen Time vs. Anxiety Score")
        fig_trend = px.scatter(
            df, x="daily_screen_time_hours", y="anxiety_score", 
            color="gender", trendline="ols", opacity=0.6,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with tab3:
        st.markdown("#### Academic Performance vs. Stress Level")
        fig_box = px.box(
            df, x="stress_level", y="academic_performance", 
            color="stress_level", color_continuous_scale="Reds"
        )
        fig_box.update_layout(xaxis_title="Reported Stress Level (1-10)", yaxis_title="Academic Performance")
        st.plotly_chart(fig_box, use_container_width=True)

else:
    st.warning("Please upload the dataset to view analytics.")
