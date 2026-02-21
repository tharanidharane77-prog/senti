// Global data storage
let analysisHistory = [];

// Tab switching functionality
function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');
    
    // Update dashboard when switching to it
    if (tabName === 'dashboard') {
        updateDashboard();
    } else if (tabName === 'trends') {
        updateTrends();
    }
}

// Simulate sentiment analysis
function analyzeSentiment() {
    const textInput = document.getElementById('textInput').value.trim();
    
    if (!textInput) {
        alert('Please enter some text to analyze');
        return;
    }
    
    if (textInput.length < 10) {
        alert('Please enter at least 10 characters');
        return;
    }
    
    // Simulate analysis with random results
    const sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED'];
    const sentiment = sentiments[Math.floor(Math.random() * sentiments.length)];
    
    // Generate random confidence scores that sum to 1
    const scores = {
        Positive: Math.random(),
        Negative: Math.random(),
        Neutral: Math.random(),
        Mixed: Math.random()
    };
    
    const total = scores.Positive + scores.Negative + scores.Neutral + scores.Mixed;
    scores.Positive = scores.Positive / total;
    scores.Negative = scores.Negative / total;
    scores.Neutral = scores.Neutral / total;
    scores.Mixed = scores.Mixed / total;
    
    // Store in history
    const analysis = {
        text: textInput,
        sentiment: sentiment,
        scores: scores,
        timestamp: new Date()
    };
    
    analysisHistory.push(analysis);
    
    // Display result
    displayResult(sentiment, scores);
    
    // Update recent analyses
    updateRecentAnalyses();
    
    // Update statistics
    updateStats();
}

function displayResult(sentiment, scores) {
    const resultSection = document.getElementById('resultSection');
    const sentimentResult = document.getElementById('sentimentResult');
    const confidenceScores = document.getElementById('confidenceScores');
    
    // Get emoji and color
    const emojis = {
        'POSITIVE': '😊',
        'NEGATIVE': '😞',
        'NEUTRAL': '😐',
        'MIXED': '🤔'
    };
    
    const colors = {
        'POSITIVE': '#00cc00',
        'NEGATIVE': '#ff0000',
        'NEUTRAL': '#ffa500',
        'MIXED': '#9370db'
    };
    
    // Display sentiment
    sentimentResult.innerHTML = `
        <div style="color: ${colors[sentiment]}">
            ${emojis[sentiment]} ${sentiment}
        </div>
    `;
    
    // Display confidence scores
    confidenceScores.innerHTML = '';
    
    for (const [type, score] of Object.entries(scores)) {
        const color = colors[type.toUpperCase()];
        const percentage = (score * 100).toFixed(1);
        
        confidenceScores.innerHTML += `
            <div class="score-card">
                <div class="label">${type}</div>
                <div class="value" style="color: ${color}">${percentage}%</div>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${percentage}%; background: ${color}"></div>
                </div>
            </div>
        `;
    }
    
    resultSection.style.display = 'block';
    
    // Scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function clearInput() {
    document.getElementById('textInput').value = '';
    document.getElementById('resultSection').style.display = 'none';
}

function updateRecentAnalyses() {
    const recentDiv = document.getElementById('recentAnalyses');
    
    if (analysisHistory.length === 0) {
        recentDiv.innerHTML = '<p class="empty-state">No analyses yet</p>';
        return;
    }
    
    const emojis = {
        'POSITIVE': '😊',
        'NEGATIVE': '😞',
        'NEUTRAL': '😐',
        'MIXED': '🤔'
    };
    
    const colors = {
        'POSITIVE': '#00cc00',
        'NEGATIVE': '#ff0000',
        'NEUTRAL': '#ffa500',
        'MIXED': '#9370db'
    };
    
    const recent = analysisHistory.slice(-3).reverse();
    recentDiv.innerHTML = '';
    
    recent.forEach(item => {
        const shortText = item.text.length > 50 ? item.text.substring(0, 50) + '...' : item.text;
        recentDiv.innerHTML += `
            <div class="recent-item" style="border-color: ${colors[item.sentiment]}">
                <div style="font-weight: bold;">
                    <span class="emoji">${emojis[item.sentiment]}</span>
                    ${item.sentiment}
                </div>
                <div class="text">${shortText}</div>
            </div>
        `;
    });
}

function updateStats() {
    document.getElementById('totalAnalyses').textContent = analysisHistory.length;
}

function updateDashboard() {
    if (analysisHistory.length === 0) {
        document.getElementById('dashboardContent').style.display = 'none';
        document.getElementById('emptyDashboard').style.display = 'block';
        return;
    }
    
    document.getElementById('dashboardContent').style.display = 'block';
    document.getElementById('emptyDashboard').style.display = 'none';
    
    // Count sentiments
    const counts = {
        POSITIVE: 0,
        NEGATIVE: 0,
        NEUTRAL: 0,
        MIXED: 0
    };
    
    analysisHistory.forEach(item => {
        counts[item.sentiment]++;
    });
    
    const total = analysisHistory.length;
    
    // Update metrics
    document.getElementById('positiveCount').textContent = counts.POSITIVE;
    document.getElementById('positivePct').textContent = ((counts.POSITIVE / total) * 100).toFixed(1) + '%';
    
    document.getElementById('negativeCount').textContent = counts.NEGATIVE;
    document.getElementById('negativePct').textContent = ((counts.NEGATIVE / total) * 100).toFixed(1) + '%';
    
    document.getElementById('neutralCount').textContent = counts.NEUTRAL;
    document.getElementById('neutralPct').textContent = ((counts.NEUTRAL / total) * 100).toFixed(1) + '%';
    
    document.getElementById('mixedCount').textContent = counts.MIXED;
    document.getElementById('mixedPct').textContent = ((counts.MIXED / total) * 100).toFixed(1) + '%';
    
    // Update charts
    updateCharts(counts);
    
    // Update history table
    updateHistoryTable();
}

function updateCharts(counts) {
    // Pie chart
    const pieData = [{
        values: [counts.POSITIVE, counts.NEGATIVE, counts.NEUTRAL, counts.MIXED],
        labels: ['Positive', 'Negative', 'Neutral', 'Mixed'],
        type: 'pie',
        marker: {
            colors: ['#00cc00', '#ff0000', '#ffa500', '#9370db']
        }
    }];
    
    const pieLayout = {
        height: 400,
        margin: { t: 0, b: 0, l: 0, r: 0 }
    };
    
    Plotly.newPlot('pieChart', pieData, pieLayout);
    
    // Bar chart
    const barData = [{
        x: ['Positive', 'Negative', 'Neutral', 'Mixed'],
        y: [counts.POSITIVE, counts.NEGATIVE, counts.NEUTRAL, counts.MIXED],
        type: 'bar',
        marker: {
            color: ['#00cc00', '#ff0000', '#ffa500', '#9370db']
        }
    }];
    
    const barLayout = {
        height: 400,
        margin: { t: 20, b: 40, l: 40, r: 20 },
        yaxis: { title: 'Count' }
    };
    
    Plotly.newPlot('barChart', barData, barLayout);
}

function updateHistoryTable() {
    const tableDiv = document.getElementById('historyTable');
    
    if (analysisHistory.length === 0) {
        tableDiv.innerHTML = '<p class="empty-state">No history available</p>';
        return;
    }
    
    const emojis = {
        'POSITIVE': '😊',
        'NEGATIVE': '😞',
        'NEUTRAL': '😐',
        'MIXED': '🤔'
    };
    
    let html = `
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: #f0f2f6;">
                    <th style="padding: 12px; text-align: left;">Timestamp</th>
                    <th style="padding: 12px; text-align: left;">Sentiment</th>
                    <th style="padding: 12px; text-align: left;">Text</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    analysisHistory.slice().reverse().forEach(item => {
        const shortText = item.text.length > 100 ? item.text.substring(0, 100) + '...' : item.text;
        const time = item.timestamp.toLocaleString();
        
        html += `
            <tr style="border-bottom: 1px solid #e0e2e6;">
                <td style="padding: 12px;">${time}</td>
                <td style="padding: 12px;">${emojis[item.sentiment]} ${item.sentiment}</td>
                <td style="padding: 12px;">${shortText}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    tableDiv.innerHTML = html;
}

function updateTrends() {
    if (analysisHistory.length < 2) {
        document.getElementById('trendsContent').style.display = 'none';
        document.getElementById('emptyTrends').style.display = 'block';
        return;
    }
    
    document.getElementById('trendsContent').style.display = 'block';
    document.getElementById('emptyTrends').style.display = 'none';
    
    // Timeline chart
    const timestamps = analysisHistory.map(item => item.timestamp);
    const sentiments = analysisHistory.map(item => item.sentiment);
    const sentimentValues = sentiments.map(s => {
        const map = { 'POSITIVE': 3, 'NEUTRAL': 2, 'NEGATIVE': 1, 'MIXED': 1.5 };
        return map[s];
    });
    
    const timelineData = [{
        x: timestamps,
        y: sentimentValues,
        mode: 'markers+lines',
        marker: {
            size: 12,
            color: sentiments.map(s => {
                const colors = {
                    'POSITIVE': '#00cc00',
                    'NEGATIVE': '#ff0000',
                    'NEUTRAL': '#ffa500',
                    'MIXED': '#9370db'
                };
                return colors[s];
            })
        },
        line: {
            color: '#667eea',
            width: 2
        },
        text: sentiments,
        hovertemplate: '%{text}<br>%{x}<extra></extra>'
    }];
    
    const timelineLayout = {
        height: 400,
        margin: { t: 20, b: 60, l: 60, r: 20 },
        xaxis: { title: 'Time' },
        yaxis: {
            title: 'Sentiment',
            tickvals: [1, 2, 3],
            ticktext: ['Negative', 'Neutral', 'Positive']
        }
    };
    
    Plotly.newPlot('timelineChart', timelineData, timelineLayout);
    
    // Confidence trends
    const positiveScores = analysisHistory.map(item => item.scores.Positive);
    const negativeScores = analysisHistory.map(item => item.scores.Negative);
    const neutralScores = analysisHistory.map(item => item.scores.Neutral);
    const mixedScores = analysisHistory.map(item => item.scores.Mixed);
    
    const trendData = [
        {
            x: timestamps,
            y: positiveScores,
            mode: 'lines+markers',
            name: 'Positive',
            line: { color: '#00cc00' }
        },
        {
            x: timestamps,
            y: negativeScores,
            mode: 'lines+markers',
            name: 'Negative',
            line: { color: '#ff0000' }
        },
        {
            x: timestamps,
            y: neutralScores,
            mode: 'lines+markers',
            name: 'Neutral',
            line: { color: '#ffa500' }
        },
        {
            x: timestamps,
            y: mixedScores,
            mode: 'lines+markers',
            name: 'Mixed',
            line: { color: '#9370db' }
        }
    ];
    
    const trendLayout = {
        height: 400,
        margin: { t: 20, b: 60, l: 60, r: 20 },
        xaxis: { title: 'Time' },
        yaxis: { title: 'Confidence Score' },
        hovermode: 'x unified'
    };
    
    Plotly.newPlot('trendChart', trendData, trendLayout);
}

function clearHistory() {
    if (confirm('Are you sure you want to clear all analysis history?')) {
        analysisHistory = [];
        updateStats();
        updateRecentAnalyses();
        updateDashboard();
        updateTrends();
        clearInput();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateStats();
    updateRecentAnalyses();
    
    // Auto-refresh handling
    const autoRefreshCheckbox = document.getElementById('autoRefresh');
    autoRefreshCheckbox.addEventListener('change', function() {
        if (this.checked) {
            alert('Auto-refresh enabled (simulated for demo purposes)');
        }
    });
});
