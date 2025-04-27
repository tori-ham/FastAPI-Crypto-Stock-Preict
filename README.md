## 📈 금융 예측 API 서버 개발 (개인 프로젝트)

### 개요
**실시간으로 암호화폐 및 주식 데이터를 수집**하고, 머신러닝 기반의 예측 모델을 다양하게 사용하며 **가격의 상승과 하락을 예측**하여 결과를 제공하는 금융 예측 API 서버입니다. 
**매일 일자 별 뉴스, 국내외 금리, 환율 등 외부 지표**로부터 feature를 생성하고 모델을 학습하여, 가격 상승/하락 예측 결과의 정확도를 개선하였습니다.
데이터를 효율적으로 관리하고 높은 응답성을 확보하기 위해 FastAPI 기반의 비동기 구조로 설계하였습니다.

### 시스템 구성
#### Back-End (FastAPI)
- 비동기 처리 구조로 높은 응답성 확보
- Open API를 이용하여 실시간 시세 데이터 수집
  - 주식 : Alpha Vantage, yfinance
  - 가상자산 : Binance
- 매일 일자 별 뉴스피드 수집 - 한국, 미국, 일본, 중국, 유럽 
- 경제지표 수집 - 국내 금리, 해외 금리, 각국 환율 등
- Pandas와 Numpy로 Open API로부터 전달받은 데이터 Pre-Processing
- 가격 상승 / 하락 예측을 위해 머신러닝에 사용된 모델
  - LogisticRegression
  - RandomForestClassifier
  - XGBClassifier
- APScheduler를 이용하여 데이터를 주기적으로 수집하고, 예측 결과의 정밀도를 높임
- Redis를 활용하여 데이터 캐싱하고 빠른 응답 속도 구현
- SQLite와 Parquet으로 메타데이터 관리
  - 대용량 시계열 데이터를 Parquet 포맷으로 저장하여 효율성 최적화

#### API
- `/asset/cryptoList`
  - Binance API를 이용하여, Binance에서 서비스하고있는 가상자산 리스트 제공
- `/predict/stockTrend`
  - yfinance API를 이용하여 실제 상장된 주식인지 확인 
  - AlphaVantage API를 이용하여 예측하고자 하는 주식의 실시간 가격 데이터를 조회한 뒤, 미리 학습된 모델에 적용하여 상승 / 하락 예측
- `/predict/cryptoTrend`
  - Binance API를 이용하여 실제 서비스되고있는 가상자산인지 확인
  - Binance에서 예측하고자 하는 가상자산의 실시간 가격 데이터를 조회한 뒤, 미리 학습된 모델에 적용하여 상승 / 하락 예측

#### 실행 방법
```bash
git clone https://github.com/tori-ham/FastAPI-Crypto-Stock-Preict.git
cd FastAPI-Crypto-Stock-Preict
python -m venv env
source env/bin/activate
pip install -r requirements.txt

# FastAPI 서버 실행
uvicorn main:app --reload
```

### 향후 추가 예정 사항
- 프론트엔드 대시보드 구축
- 예측 정확도 모니터링 시스템 도입 및 예측 결과에 따른 학습 모델 자가 보정 설계