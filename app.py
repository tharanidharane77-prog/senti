import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Real-Time Sentiment Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    .sentiment-positive {
        color: #00cc00;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #ff0000;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #ffa500;
        font-weight: bold;
    }
    .sentiment-mixed {
        color: #9370db;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'sentiment_data' not in st.session_state:
    st.session_state.sentiment_data = []
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def simulate_sentiment_analysis(text):
    """Simulates sentiment analysis (placeholder for AWS Comprehend)"""
    # This would connect to AWS Comprehend in production
    sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED']
    import random
    sentiment = random.choice(sentiments)
    
    scores = {
        'Positive': round(random.random(), 3),
        'Negative': round(random.random(), 3),
        'Neutral': round(random.random(), 3),
        'Mixed': round(random.random(), 3)
    }
    
    # Normalize scores
    total = sum(scores.values())
    scores = {k: round(v/total, 3) for k, v in scores.items()}
    
    return {
        'sentiment': sentiment,
        'scores': scores,
        'timestamp': datetime.now()
    }

def get_sentiment_color(sentiment):
    """Returns color based on sentiment"""
    colors = {
        'POSITIVE': '#00cc00',
        'NEGATIVE': '#ff0000',
        'NEUTRAL': '#ffa500',
        'MIXED': '#9370db'
    }
    return colors.get(sentiment, '#808080')

def get_sentiment_emoji(sentiment):
    """Returns emoji based on sentiment"""
    emojis = {
        'POSITIVE': '😊',
        'NEGATIVE': '😞',
        'NEUTRAL': '😐',
        'MIXED': '🤔'
    }
    return emojis.get(sentiment, '❓')

# Header
st.title("🎯 Real-Time Sentiment Tracking Dashboard")
st.markdown("### Powered by AWS Amplify + Amazon Comprehend")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("#### AWS Services")
    st.info("🔹 **AWS Amplify**: Frontend Hosting\n🔹 **Amazon Comprehend**: Sentiment Analysis")
    
    st.markdown("---")
    st.markdown("#### Analysis Settings")
    language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Italian"])
    auto_refresh = st.checkbox("Auto Refresh", value=False)
    
    if auto_refresh:
        refresh_rate = st.slider("Refresh Rate (seconds)", 1, 10, 3)
    
    st.markdown("---")
    st.markdown("#### Statistics")
    total_analyses = len(st.session_state.analysis_history)
    st.metric("Total Analyses", total_analyses)
    
    if st.button("Clear History", type="secondary"):
        st.session_state.analysis_history = []
        st.session_state.sentiment_data = []
        st.rerun()

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Analyze Text", "📊 Dashboard", "📈 Trends", "ℹ️ About"])

with tab1:
    st.header("Text Sentiment Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_method = st.radio("Input Method", ["Single Text", "Batch Upload"], horizontal=True)
        
        if input_method == "Single Text":
            text_input = st.text_area(
                "Enter text to analyze:",
                placeholder="Type or paste your text here...",
                height=150
            )
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                analyze_btn = st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True)
            with col_btn2:
                clear_btn = st.button("🗑️ Clear", use_container_width=True)
            
            if analyze_btn and text_input:
                with st.spinner("Analyzing sentiment..."):
                    time.sleep(0.5)  # Simulate API call
                    result = simulate_sentiment_analysis(text_input)
                    
                    # Store in history
                    st.session_state.analysis_history.append({
                        'text': text_input[:100] + '...' if len(text_input) > 100 else text_input,
                        'sentiment': result['sentiment'],
                        'timestamp': result['timestamp'],
                        'scores': result['scores']
                    })
                    
                    # Display result
                    st.success("✅ Analysis Complete!")
                    
                    sentiment = result['sentiment']
                    emoji = get_sentiment_emoji(sentiment)
                    color = get_sentiment_color(sentiment)
                    
                    st.markdown(f"### Sentiment: <span style='color:{color}'>{emoji} {sentiment}</span>", unsafe_allow_html=True)
                    
                    # Display confidence scores
                    st.markdown("#### Confidence Scores:")
                    score_cols = st.columns(4)
                    for idx, (sent_type, score) in enumerate(result['scores'].items()):
                        with score_cols[idx]:
                            st.metric(sent_type, f"{score:.1%}")
                    
                    # Progress bars
                    for sent_type, score in result['scores'].items():
                        st.progress(score, text=f"{sent_type}: {score:.1%}")
            
            if clear_btn:
                st.rerun()
        
        else:  # Batch Upload
            uploaded_file = st.file_uploader("Upload a text file or CSV", type=['txt', 'csv'])
            
            if uploaded_file:
                st.info("📁 File uploaded successfully!")
                
                if st.button("🔍 Analyze Batch", type="primary"):
                    with st.spinner("Processing batch analysis..."):
                        time.sleep(1.5)
                        st.success("✅ Batch analysis complete! Check the Dashboard tab for results.")
    
    with col2:
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Enter clear, complete sentences
        - Minimum 10 characters recommended
        - Supports multiple languages
        - Real-time processing
        - Results saved to history
        """)
        
        st.markdown("### 📋 Recent Analyses")
        if st.session_state.analysis_history:
            for item in st.session_state.analysis_history[-3:]:
                emoji = get_sentiment_emoji(item['sentiment'])
                st.markdown(f"{emoji} **{item['sentiment']}**")
                st.caption(f"{item['text'][:50]}...")
        else:
            st.caption("No analyses yet")

with tab2:
    st.header("Sentiment Dashboard")
    
    if st.session_state.analysis_history:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        sentiments = [item['sentiment'] for item in st.session_state.analysis_history]
        
        with col1:
            positive_count = sentiments.count('POSITIVE')
            st.metric("😊 Positive", positive_count, delta=f"{positive_count/len(sentiments)*100:.1f}%")
        
        with col2:
            negative_count = sentiments.count('NEGATIVE')
            st.metric("😞 Negative", negative_count, delta=f"{negative_count/len(sentiments)*100:.1f}%")
        
        with col3:
            neutral_count = sentiments.count('NEUTRAL')
            st.metric("😐 Neutral", neutral_count, delta=f"{neutral_count/len(sentiments)*100:.1f}%")
        
        with col4:
            mixed_count = sentiments.count('MIXED')
            st.metric("🤔 Mixed", mixed_count, delta=f"{mixed_count/len(sentiments)*100:.1f}%")
        
        st.markdown("---")
        
        # Visualizations
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Sentiment Distribution")
            sentiment_counts = pd.Series(sentiments).value_counts()
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                color=sentiment_counts.index,
                color_discrete_map={
                    'POSITIVE': '#00cc00',
                    'NEGATIVE': '#ff0000',
                    'NEUTRAL': '#ffa500',
                    'MIXED': '#9370db'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            st.subheader("Sentiment Breakdown")
            fig_bar = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                color=sentiment_counts.index,
                color_discrete_map={
                    'POSITIVE': '#00cc00',
                    'NEGATIVE': '#ff0000',
                    'NEUTRAL': '#ffa500',
                    'MIXED': '#9370db'
                },
                labels={'x': 'Sentiment', 'y': 'Count'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Analysis History Table
        st.subheader("📜 Analysis History")
        history_df = pd.DataFrame(st.session_state.analysis_history)
        st.dataframe(
            history_df[['timestamp', 'sentiment', 'text']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("👈 No data yet. Start by analyzing some text in the 'Analyze Text' tab!")

with tab3:
    st.header("Sentiment Trends Over Time")
    
    if len(st.session_state.analysis_history) > 1:
        # Time series data
        df = pd.DataFrame(st.session_state.analysis_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sentiment over time
        st.subheader("Sentiment Timeline")
        fig_timeline = px.scatter(
            df,
            x='timestamp',
            y='sentiment',
            color='sentiment',
            color_discrete_map={
                'POSITIVE': '#00cc00',
                'NEGATIVE': '#ff0000',
                'NEUTRAL': '#ffa500',
                'MIXED': '#9370db'
            },
            size_max=15
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Confidence scores over time
        st.subheader("Average Confidence Scores Trend")
        
        # Extract average scores
        timestamps = []
        avg_positive = []
        avg_negative = []
        avg_neutral = []
        avg_mixed = []
        
        for item in st.session_state.analysis_history:
            timestamps.append(item['timestamp'])
            avg_positive.append(item['scores'].get('Positive', 0))
            avg_negative.append(item['scores'].get('Negative', 0))
            avg_neutral.append(item['scores'].get('Neutral', 0))
            avg_mixed.append(item['scores'].get('Mixed', 0))
        
        fig_trends = go.Figure()
        fig_trends.add_trace(go.Scatter(x=timestamps, y=avg_positive, mode='lines+markers', name='Positive', line=dict(color='#00cc00')))
        fig_trends.add_trace(go.Scatter(x=timestamps, y=avg_negative, mode='lines+markers', name='Negative', line=dict(color='#ff0000')))
        fig_trends.add_trace(go.Scatter(x=timestamps, y=avg_neutral, mode='lines+markers', name='Neutral', line=dict(color='#ffa500')))
        fig_trends.add_trace(go.Scatter(x=timestamps, y=avg_mixed, mode='lines+markers', name='Mixed', line=dict(color='#9370db')))
        
        fig_trends.update_layout(
            xaxis_title="Time",
            yaxis_title="Confidence Score",
            hovermode='x unified'
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        
    else:
        st.info("📊 Need at least 2 analyses to show trends. Keep analyzing!")

with tab4:
    st.header("About This Application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Overview
        This is a **Real-Time Sentiment Tracking Dashboard** built with Streamlit and designed to integrate with AWS services.
        
        ### 🛠️ Technologies
        - **Frontend**: Streamlit
        - **Hosting**: AWS Amplify
        - **AI/ML**: Amazon Comprehend
        - **Visualization**: Plotly
        
        ### ✨ Features
        - Real-time sentiment analysis
        - Support for multiple languages
        - Batch processing capability
        - Interactive visualizations
        - Historical trend analysis
        - Confidence score tracking
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Sentiment Types
        
        **😊 POSITIVE**: Text expressing positive emotions, satisfaction, or approval
        
        **😞 NEGATIVE**: Text expressing negative emotions, dissatisfaction, or criticism
        
        **😐 NEUTRAL**: Text that is factual, objective, or lacks emotional content
        
        **🤔 MIXED**: Text containing both positive and negative sentiments
        
        ### 🔧 AWS Integration Points
        - Amazon Comprehend API for sentiment detection
        - AWS Amplify for static hosting
        - Amazon S3 for data storage (optional)
        - Amazon CloudWatch for monitoring (optional)
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 🚀 Deployment with AWS Amplify
    
    1. **Initialize Amplify**: `amplify init`
    2. **Add Hosting**: `amplify add hosting`
    3. **Configure Comprehend**: Set up IAM roles and permissions
    4. **Deploy**: `amplify publish`
    
    ### 📝 Environment Variables (for backend integration)
    ```
    AWS_REGION=us-east-1
    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    ```
    """)

# Auto-refresh functionality
if auto_refresh and 'last_refresh' in st.session_state:
    if (datetime.now() - st.session_state.last_refresh).seconds >= refresh_rate:
        st.session_state.last_refresh = datetime.now()
        st.rerun()
elif auto_refresh:
    st.session_state.last_refresh = datetime.now()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Built with ❤️ using Streamlit | Powered by AWS Amplify + Amazon Comprehend</div>",
    unsafe_allow_html=True
)
