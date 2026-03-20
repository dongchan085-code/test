import os
from google import genai
from typing import Dict, Any

def summarize_paper(paper: Dict[str, Any]) -> str:
    """
    Takes a paper dict from fetch_top_papers and generates a structured summary using Gemini.
    """
    api_key = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    if not api_key or api_key == "your_gemini_api_key_here":
         # Return a beautiful mock response for testing if the user hasn't set their key yet
         return """### 주요 특징 (Main Features)
- 최신 논문의 핵심 특징 1
- 효율적인 데이터 처리 및 성능 향상 방식 제안 (테스트 모킹)

### 아이디어 (Core Idea)
- 모델의 병목 현상을 해결하기 위해 새로운 어텐션 메커니즘을 적용한 혁신적인 아이디어입니다. (테스트)

### Metric (Evaluation Metrics)
- 기존 모델 대비 처리 속도 20% 향상 (테스트 데이터)
- 주요 벤치마크 테스트에서 SOTA 달성

### 사용처 (Use Cases)
- 실시간 텍스트 생성 시스템
- 고성능 대규모 언어 모델 서빙 환경"""
         
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    client = genai.Client(api_key=api_key)
    
    title = paper.get("title", "")
    abstract = paper.get("summary", "")
    
    prompt = f"""You are an expert AI researcher. Summarize the following paper.
You must output the summary strictly in Korean, structured in the 4 sections specified below. Do not include any other introductory or concluding text.

Paper Title: {title}
Abstract: {abstract}

Format exactly like this (use Markdown):
### 주요 특징 (Main Features)
- [feature 1]
- [feature 2]

### 아이디어 (Core Idea)
- [core idea description]

### Metric (Evaluation Metrics)
- [metric 1]
- [metric 2]

### 사용처 (Use Cases)
- [use case 1]
- [use case 2]
"""
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    
    return response.text
