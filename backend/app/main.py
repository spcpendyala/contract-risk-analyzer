from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title='Contract Risk Analyzer API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
        'http://localhost:5174',
        'https://contracts.palaemonsystems.com',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(analyze.router)

@app.get('/health')
def health(): return {'status': 'healthy'}
