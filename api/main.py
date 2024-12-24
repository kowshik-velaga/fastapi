from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from api.auth import authenticate
from api.models import SentimentResult
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API!"}

@app.post("/analyze", dependencies=[Depends(authenticate)])
async def analyze_csv(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload a CSV file.")

    # Load CSV file
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV file: {e}")

    # Check for required columns
    required_columns = {'id', 'text'}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"CSV file must contain columns: {required_columns}")

    # Perform Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    results = []

    for index, row in df.iterrows():
        sentiment_scores = analyzer.polarity_scores(row['text'])
        sentiment = (
            "positive" if sentiment_scores['compound'] > 0 else
            "neutral" if sentiment_scores['compound'] == 0 else
            "negative"
        )
        results.append(SentimentResult(
            id=row['id'],
            text=row['text'],
            sentiment=sentiment
        ).dict())

    return JSONResponse(content=results)
