#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETF Flow Analysis with AI Insights
Tracks major ETFs and analyzes capital flows using OBV and Volume Ratio
Generates AI-based insights on sector rotation
"""

import os
import json
import logging
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime
from typing import Dict, List, Optional
from tqdm import tqdm
from dotenv import load_dotenv

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class ETFFlowAnalyzer:
    def __init__(self, data_dir: str = '.'):
        self.data_dir = data_dir
        self.output_csv = os.path.join(data_dir, 'us_etf_flows.csv')
        self.output_json = os.path.join(data_dir, 'etf_flow_analysis.json')
        
        # Major ETFs to track
        self.etfs = {
            'SPY': 'S&P 500', 'QQQ': 'Nasdaq 100', 'IWM': 'Russell 2000', 'VTI': 'Total Stock Market',
            'XLK': 'Technology', 'XLF': 'Financials', 'XLV': 'Healthcare', 
            'XLE': 'Energy', 'XLY': 'Consumer Disc', 'XLP': 'Consumer Staples',
            'XLI': 'Industrials', 'XLB': 'Materials', 'XLU': 'Utilities', 
            'XLRE': 'Real Estate', 'XLC': 'Comm Services',
            'SMH': 'Semiconductors', 'XBI': 'Biotech', 'ARKK': 'Innovation',
            'GDX': 'Gold Miners', 'GLD': 'Gold', 'USO': 'Oil', 'TLT': '20Y Treasury',
            'HYG': 'High Yield Bonds', 'LQD': 'Corp Bonds', 'KRE': 'Regional Banks', 'EEM': 'Emerging Markets'
        }
        
        self.categories = {
            'Broad Market': ['SPY', 'QQQ', 'IWM', 'VTI'],
            'Sector': ['XLK', 'XLF', 'XLV', 'XLE', 'XLY', 'XLP', 'XLI', 'XLB', 'XLU', 'XLRE', 'XLC'],
            'Data': ['SMH', 'XBI', 'ARKK', 'GDX', 'GLD', 'USO', 'TLT', 'HYG', 'LQD', 'KRE', 'EEM']
        }
        
    def calculate_flow_proxy(self, data: pd.DataFrame) -> Dict:
        """Calculate proxy for fund flows using Price and Volume"""
        if len(data) < 20:
            return {}
            
        # 1. OBV Trend (20d)
        data['obv'] = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        obv_change = (data['obv'].iloc[-1] - data['obv'].iloc[-20])
        # Normalize OBV change by average volume
        obv_norm = obv_change / (data['Volume'].rolling(20).mean().iloc[-1] * 20) * 100
        
        # 2. Volume Ratio (5d / 20d)
        vol_ratio = data['Volume'].tail(5).mean() / data['Volume'].tail(20).mean()
        
        # 3. Price Momentum (20d)
        mom_20d = (data['Close'].iloc[-1] / data['Close'].iloc[-20] - 1) * 100
        
        # Improved Flow Score (0-100) with clipping to prevent extremes
        # Normalize inputs to reasonable ranges
        obv_weight = np.clip(obv_norm, -5, 5)  # Limit obv impact to -5 to +5
        mom_weight = np.clip(mom_20d / 10, -3, 3)  # Scale down momentum, limit to -3 to +3
        vol_weight = (vol_ratio - 1) * 10  # Volume ratio contribution
        
        # Calculate score (0-100)
        score = 50  # Base score
        score += obv_weight * 5  # OBV: -25 to +25
        score += mom_weight * 5  # Momentum: -15 to +15
        score += vol_weight  # Volume: varies based on ratio
        
        # Ensure score is in 0-100 range
        score = max(0, min(100, score))
        
        return {
            'price': round(data['Close'].iloc[-1], 2),
            'change_1d': round(data['Close'].pct_change().iloc[-1] * 100, 2),
            'flow_score': round(score, 1),
            'vol_ratio': round(vol_ratio, 2),
            'momentum_20d': round(mom_20d, 2)
        }

    def generate_ai_analysis(self, results: List[Dict]) -> str:
        """Generate AI analysis of ETF flows"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key: return "AI Analysis: No API Key provided."
        
        # Find winners and losers
        sorted_res = sorted(results, key=lambda x: x['flow_score'], reverse=True)
        top_3 = sorted_res[:3]
        bottom_3 = sorted_res[-3:]
        
        summary_txt = f"Top Inflows: {', '.join([x['ticker'] for x in top_3])}\n"
        summary_txt += f"Top Outflows: {', '.join([x['ticker'] for x in bottom_3])}\n"
        
        prompt = f"""Analyze these ETF flow trends and suggest what they mean for the broader market rotation.
        {summary_txt}
        Provide a concise 3-sentence summary in Korean."""
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(f"{url}?key={api_key}", json=payload)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logger.error(f"AI Generation Error: {e}")
        return "AI Analysis Unavailable"

    def run(self):
        logger.info("🚀 Starting ETF Flow Analysis...")
        results = []
        
        for ticker, name in tqdm(self.etfs.items(), desc="Analyzing ETFs"):
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1mo")
                
                if hist.empty: continue
                
                metrics = self.calculate_flow_proxy(hist)
                if metrics:
                    # Determine category
                    res_cat = 'Data'
                    for cat, tickers in self.categories.items():
                        if ticker in tickers:
                            res_cat = cat
                            break
                            
                    results.append({
                        'category': res_cat,
                        'ticker': ticker,
                        'name': name,
                        **metrics
                    })
            except Exception as e:
                logger.error(f"Error analyzing {ticker}: {e}")
                
        # Save CSV
        df = pd.DataFrame(results)
        df = df.sort_values('flow_score', ascending=False)
        df.to_csv(self.output_csv, index=False)
        logger.info(f"✅ Saved ETF flows to {self.output_csv}")
        
        # AI Analysis
        ai_text = self.generate_ai_analysis(results)
        
        # Save JSON
        output = {
            'timestamp': datetime.now().isoformat(),
            'ai_analysis': ai_text,
            'top_flows': df.head(5).to_dict('records'),
            'bottom_flows': df.tail(5).to_dict('records')
        }
        
        with open(self.output_json, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved AI analysis to {self.output_json}")
        
        print(f"\\n[AI] AI Insight: {ai_text}")

if __name__ == "__main__":
    ETFFlowAnalyzer().run()
