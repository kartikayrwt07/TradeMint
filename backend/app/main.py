from fastapi import FastAPI
from .config.settings import settings

app = FastAPI(title="TradeMint Strategy Engine")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "trademint-market-strategy",
        "provider": settings.market_data_provider
    }
