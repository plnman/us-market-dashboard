#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Stock Summary Generator
Generates investment summaries using Gemini AI
"""

import os, json, logging, time, requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsCollector:
    def get_news(self, ticker: str):
        # Simplified for brevity - uses Google News RSS
        news = []
        try:
            import xml.etree.ElementTree as ET
            url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for item in root.findall('.//item')[:3]:
                    news.append({'title': item.find('title').text, 'published': item.find('pubDate').text})
        except: pass
        return news

class GeminiGenerator:
    def __init__(self):
        self.key = os.getenv('GOOGLE_API_KEY')
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def generate(self, ticker, data, news, lang='ko'):
        if not self.key: return "No API Key"
        
        news_txt = "\\n".join([n['title'] for n in news])
        score_info = f"Score: {data.get('composite_score')}/100, Quant: {data.get('grade')}"
        
        if lang == 'ko':
            prompt = f"""종목: {ticker}
정보: {score_info}
뉴스: {news_txt}
요청: 3-4문장으로 투자 의견 요약 (수급, 펀더멘털, 전략). 이모지 X."""
        else:
            prompt = f"""Stock: {ticker}
Info: {score_info}
News: {news_txt}
Req: 3-4 sentence investment summary. No emojis."""

        try:
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(f"{self.url}?key={self.key}", json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except: return "Analysis Failed"

class AIStockAnalyzer:
    def __init__(self, data_dir='.'):
        self.data_dir = data_dir
        self.output = os.path.join(data_dir, 'ai_summaries.json')
        self.gen = GeminiGenerator()
        self.news = NewsCollector()
        
    def run(self, top_n=20):
        csv = os.path.join(self.data_dir, 'smart_money_picks_v2.csv')
        if not os.path.exists(csv): return
        
        df = pd.read_csv(csv).head(top_n)
        results = {}
        
        # Load existing
        if os.path.exists(self.output):
            with open(self.output, encoding='utf-8') as f: results = json.load(f)
            
        for _, row in tqdm(df.iterrows(), total=len(df)):
            ticker = row['ticker']
            if ticker in results: continue # Skip if exists
            
            print(f"DEBUG: Processing {ticker}")
            news = self.news.get_news(ticker)
            print(f"DEBUG: Got news for {ticker}")
            
            summary_ko = self.gen.generate(ticker, row.to_dict(), news, 'ko')
            print(f"DEBUG: Generated KO summary for {ticker}")
            
            summary_en = self.gen.generate(ticker, row.to_dict(), news, 'en')
            print(f"DEBUG: Generated EN summary for {ticker}")
            
            results[ticker] = {
                'summary': summary_ko,
                'summary_ko': summary_ko,
                'summary_en': summary_en,
                'updated': os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()
            }
            
            # Save incrementally every 5 items
            if len(results) % 5 == 0:
                with open(self.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved progress: {len(results)} summaries")
                
            time.sleep(1) # Rate limit
            
        with open(self.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(results)} summaries")

if __name__ == "__main__":
    print("Starting AI Summary Generation for Top 5 stocks...")
    AIStockAnalyzer().run(top_n=5)
