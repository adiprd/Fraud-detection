from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import random
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

class FraudDetector:
    def __init__(self):
        self.transactions = None
        self.fraud_rules = None
        self.model = None
        
    def load_data(self):
        """Load transaction data"""
        try:
            self.transactions = pd.read_csv('data/transactions.csv')
            self.transactions['timestamp'] = pd.to_datetime(self.transactions['timestamp'])
            self.fraud_rules = pd.read_csv('data/fraud_rules.csv')
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def detect_fraud_patterns(self, transaction):
        """Detect fraud patterns based on rules"""
        fraud_score = 0
        alerts = []
        
        # Rule 1: Amount anomaly
        avg_amount = self.transactions['amount'].mean()
        if transaction['amount'] > avg_amount * 3:
            fraud_score += 30
            alerts.append("Amount significantly higher than average")
        
        # Rule 2: Unusual time (late night transactions)
        hour = transaction['timestamp'].hour
        if hour >= 23 or hour <= 5:
            fraud_score += 20
            alerts.append("Transaction at unusual hours")
        
        # Rule 3: New vendor
        vendor_history = self.transactions[
            self.transactions['employee_id'] == transaction['employee_id']
        ]['vendor'].unique()
        
        if transaction['vendor'] not in vendor_history:
            fraud_score += 25
            alerts.append("Transaction with new vendor")
        
        # Rule 4: High frequency transactions
        recent_transactions = self.transactions[
            (self.transactions['employee_id'] == transaction['employee_id']) &
            (self.transactions['timestamp'] > transaction['timestamp'] - timedelta(hours=1))
        ]
        
        if len(recent_transactions) > 5:
            fraud_score += 15
            alerts.append("High frequency of transactions")
        
        # Rule 5: Weekend transactions for business expenses
        if transaction['timestamp'].weekday() >= 5 and transaction['category'] == 'Business Expense':
            fraud_score += 10
            alerts.append("Business expense on weekend")
        
        # Determine risk level
        if fraud_score >= 60:
            risk_level = "HIGH"
            action = "BLOCK & ALERT SECURITY"
        elif fraud_score >= 40:
            risk_level = "MEDIUM" 
            action = "REVIEW REQUIRED"
        else:
            risk_level = "LOW"
            action = "MONITOR"
        
        return {
            'fraud_score': fraud_score,
            'risk_level': risk_level,
            'action': action,
            'alerts': alerts
        }
    
    def analyze_transactions(self):
        """Analyze all transactions for fraud patterns"""
        results = []
        
        for _, transaction in self.transactions.iterrows():
            fraud_analysis = self.detect_fraud_patterns(transaction)
            
            results.append({
                'transaction_id': transaction['transaction_id'],
                'employee_id': transaction['employee_id'],
                'employee_name': transaction['employee_name'],
                'vendor': transaction['vendor'],
                'amount': transaction['amount'],
                'category': transaction['category'],
                'timestamp': transaction['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'fraud_score': fraud_analysis['fraud_score'],
                'risk_level': fraud_analysis['risk_level'],
                'action': fraud_analysis['action'],
                'alerts': ', '.join(fraud_analysis['alerts'])
            })
        
        return pd.DataFrame(results)
    
    def get_fraud_summary(self, analysis_results):
        """Get summary statistics"""
        total_transactions = len(analysis_results)
        high_risk = len(analysis_results[analysis_results['risk_level'] == 'HIGH'])
        medium_risk = len(analysis_results[analysis_results['risk_level'] == 'MEDIUM'])
        total_flagged = high_risk + medium_risk
        
        total_amount = analysis_results['amount'].sum()
        flagged_amount = analysis_results[
            analysis_results['risk_level'].isin(['HIGH', 'MEDIUM'])
        ]['amount'].sum()
        
        return {
            'total_transactions': total_transactions,
            'high_risk_count': high_risk,
            'medium_risk_count': medium_risk,
            'total_flagged': total_flagged,
            'total_amount': round(total_amount, 2),
            'flagged_amount': round(flagged_amount, 2),
            'fraud_percentage': round((total_flagged / total_transactions) * 100, 1)
        }
    
    def get_top_risky_employees(self, analysis_results, top_n=5):
        """Get employees with highest fraud risk"""
        employee_risk = analysis_results.groupby(['employee_id', 'employee_name']).agg({
            'fraud_score': 'mean',
            'amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        employee_risk['avg_fraud_score'] = employee_risk['fraud_score']
        employee_risk = employee_risk.nlargest(top_n, 'avg_fraud_score')
        
        return employee_risk.to_dict('records')
    
    def generate_visualizations(self, analysis_results, summary):
        """Generate fraud detection visualizations"""
        visualizations = {}
        
        # Color scheme for fraud detection
        colors = ['#FF6B6B', '#FFA726', '#66BB6A', '#42A5F5']
        
        # 1. Risk Distribution Pie Chart
        risk_counts = analysis_results['risk_level'].value_counts()
        
        fig1, ax1 = plt.subplots(figsize=(8, 8))
        ax1.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%',
                colors=[colors[0], colors[1], colors[2]], startangle=90)
        ax1.set_title('Transaction Risk Distribution', fontsize=14, fontweight='bold')
        
        img1 = io.BytesIO()
        plt.savefig(img1, format='png', bbox_inches='tight', facecolor='#F8F9FA')
        img1.seek(0)
        visualizations['risk_pie'] = base64.b64encode(img1.getvalue()).decode()
        plt.close(fig1)
        
        # 2. Fraud Score Distribution
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.hist(analysis_results['fraud_score'], bins=20, color=colors[3], alpha=0.7, edgecolor='black')
        ax2.set_title('Fraud Score Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Fraud Score')
        ax2.set_ylabel('Number of Transactions')
        ax2.grid(True, alpha=0.3)
        
        img2 = io.BytesIO()
        plt.savefig(img2, format='png', bbox_inches='tight', facecolor='#F8F9FA')
        img2.seek(0)
        visualizations['score_hist'] = base64.b64encode(img2.getvalue()).decode()
        plt.close(fig2)
        
        return visualizations

# Initialize detector
detector = FraudDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not detector.load_data():
        return render_template('error.html', message="Failed to load transaction data")
    
    # Analyze transactions
    analysis_results = detector.analyze_transactions()
    summary = detector.get_fraud_summary(analysis_results)
    risky_employees = detector.get_top_risky_employees(analysis_results)
    visuals = detector.generate_visualizations(analysis_results, summary)
    
    # Get high risk transactions for alert table
    high_risk_transactions = analysis_results[
        analysis_results['risk_level'] == 'HIGH'
    ].head(10).to_dict('records')
    
    return render_template('dashboard.html',
                         summary=summary,
                         risky_employees=risky_employees,
                         high_risk_transactions=high_risk_transactions,
                         visuals=visuals)

@app.route('/api/check_transaction', methods=['POST'])
def api_check_transaction():
    """API to check individual transaction"""
    data = request.json
    
    # Simulate real-time transaction check
    transaction = {
        'amount': data['amount'],
        'employee_id': data['employee_id'],
        'vendor': data['vendor'],
        'category': data['category'],
        'timestamp': datetime.now()
    }
    
    fraud_analysis = detector.detect_fraud_patterns(transaction)
    
    return jsonify({
        'fraud_score': fraud_analysis['fraud_score'],
        'risk_level': fraud_analysis['risk_level'],
        'action': fraud_analysis['action'],
        'alerts': fraud_analysis['alerts']
    })

@app.route('/api/transactions')
def api_transactions():
    if not detector.load_data():
        return jsonify({'error': 'Data loading failed'})
    
    analysis_results = detector.analyze_transactions()
    return jsonify(analysis_results.to_dict('records'))

if __name__ == '__main__':
    print("Fraud Detection AI started at http://localhost:5000")
    app.run(debug=True, port=5000)
