import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GenZ Mental Health & Social Media",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Replace with your actual file path if needed
    df = pd.read_csv("GenZ_Social_Media_Mental_Health_2026.csv")
    return df

df = load_data()

# --- SIDEBAR & NAVIGATION ---
st.sidebar.title("🧠 GenZ Insights 2026")
st.sidebar.write("Explore how social media impacts mental health.")
page = st.sidebar.radio("Navigate", ["📊 Dashboard & Insights", "🔮 Personal Assessment"])

# --- PAGE 1: DASHBOARD & INSIGHTS ---
if page == "📊 Dashboard & Insights":
    st.title("📊 GenZ Social Media & Mental Health Dashboard")
    st.markdown("Explore trends, correlations, and insights from the 2026 dataset.")

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Participants", len(df))
    col2.metric("Avg Screen Time", f"{df['daily_screen_time_hours'].mean():.1f} hrs")
    col3.metric("Avg Sleep Hours", f"{df['sleep_hours'].mean():.1f} hrs")
    col4.metric("Avg Stress Level", f"{df['stress_level'].mean():.1f} / 20")

    st.divider()

    # Charts Section
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📱 Primary Platform Distribution")
        fig1 = px.pie(df, names='primary_platform', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
        st.info("**Insight:** See which platforms dominate GenZ's daily routines.")

    with col_chart2:
        st.subheader("😴 Screen Time vs. Sleep Hours")
        fig2 = px.scatter(df, x='daily_screen_time_hours', y='sleep_hours', color='primary_platform', 
                          trendline="ols", opacity=0.6)
        st.plotly_chart(fig2, use_container_width=True)
        st.info("**Insight:** Higher screen time generally correlates with a reduction in sleep hours.")

    st.divider()
    
    st.subheader("🧠 Mental Health Scores by Platform")
    fig3 = px.box(df, x='primary_platform', y='anxiety_score', color='primary_platform')
    st.plotly_chart(fig3, use_container_width=True)

# --- PAGE 2: PERSONAL ASSESSMENT ---
elif page == "🔮 Personal Assessment":
    st.title("🔮 Personal Digital Wellbeing Assessment")
    st.markdown("Enter your daily habits to see how you compare to the GenZ average, get personalized advice, and see your digital profile emoji!")

    with st.form("user_input_form"):
        st.subheader("Tell us about your habits:")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", 13, 27, 20)
            platform = st.selectbox("Primary Platform", df['primary_platform'].unique())
            screen_time = st.number_input("Daily Screen Time (hours)", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
            
        with col2:
            sleep_hours = st.number_input("Average Sleep (hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
            stress_level = st.slider("Current Stress Level (1-20)", 1, 20, 10)
            social_activity = st.number_input("Offline Social Activity (hours)", min_value=0.0, max_value=24.0, value=2.0, step=0.5)
            
        submitted = st.form_submit_button("Analyze My Profile")

    if submitted:
        st.divider()
        st.subheader("Your Results")
        
        # Calculations for comparisons
        platform_users = df[df['primary_platform'] == platform]
        platform_pct = (len(platform_users) / len(df)) * 100
        avg_screen_time_platform = platform_users['daily_screen_time_hours'].mean()
        
        # Determine Emoji and Advice based on inputs
        if screen_time > 8 and sleep_hours < 6:
            emoji = "🧟"
            status = "The Zombie Scroller"
            advice = "Your screen time is very high and sleep is suffering. Try setting digital curfews 1 hour before bed to improve your mental recovery."
        elif stress_level > 15:
            emoji = "🤯"
            status = "The Overwhelmed User"
            advice = "Your stress levels are peaking. Consider taking a 24-hour social media detox and focusing on your offline social activities."
        elif sleep_hours >= 7 and screen_time < avg_screen_time_platform:
            emoji = "🧘"
            status = "The Zen Master"
            advice = "Great job! You have a healthy balance between your digital life and personal wellbeing. Keep maintaining those boundaries."
        else:
            emoji = "📱"
            status = "The Average Scroller"
            advice = "You are right in the middle of the pack. Monitor your screen time to ensure it doesn't creep up and affect your sleep!"

        # Display Results Beautifully
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.markdown(f"<h1 style='text-align: center; font-size: 100px;'>{emoji}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>{status}</h3>", unsafe_allow_html=True)
            
        with res_col2:
            st.success(f"**Advice:** {advice}")
            
            st.markdown("### 📊 How you compare:")
            st.write(f"- **Platform Popularity:** You are among the **{platform_pct:.1f}%** of GenZ users who prefer {platform}.")
            
            if screen_time > avg_screen_time_platform:
                st.warning(f"- **Screen Time:** Your screen time ({screen_time} hrs) is **higher** than the average {platform} user ({avg_screen_time_platform:.1f} hrs).")
            else:
                st.info(f"- **Screen Time:** Your screen time ({screen_time} hrs) is **lower** than the average {platform} user ({avg_screen_time_platform:.1f} hrs).")
                
            overall_sleep = df['sleep_hours'].mean()
            st.write(f"- **Sleep Check:** The overall GenZ average sleep is **{overall_sleep:.1f} hours**. You get **{sleep_hours} hours**.")
