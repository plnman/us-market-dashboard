import json
import pandas as pd
from datetime import datetime

# Load Top 5 stocks
df = pd.read_csv('c:/us_market/smart_money_picks_v2.csv').head(5)
summaries = {}

timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

for _, row in df.iterrows():
    ticker = row['ticker']
    name = row['name']
    summaries[ticker] = {
        "summary": f"AI Summary for {name} ({ticker}): Strong institutional support with a composite score of {row['composite_score']}. Technical indicators show positive momentum.",
        "summary_ko": f"{name} ({ticker})에 대한 AI 요약: 기관들의 강력한 지지를 받고 있으며 종합 점수는 {row['composite_score']}점입니다. 기술적 지표들이 긍정적인 모멘텀을 보여주고 있습니다.",
        "summary_en": f"AI Summary for {name} ({ticker}): Strong institutional support with a composite score of {row['composite_score']}. Technical indicators show positive momentum.",
        "updated": timestamp
    }

with open('c:/us_market/ai_summaries.json', 'w', encoding='utf-8') as f:
    json.dump(summaries, f, indent=2, ensure_ascii=False)

print(f"Created dummy summaries for {len(summaries)} stocks.")
