# TradeMint Market Data & Strategy Engine

This module is responsible for consuming market data, generating candles, running strategies, and emitting OrderIntents.

## What this module does
- Consumes mock/generic market data (Ticks)
- Generates 1m and 5m candles
- Runs 3 independent strategies (MA Crossover, Momentum, Breakout)
- Emits OrderIntent objects

## What it does NOT do
- Does not check risk limits
- Does not place actual orders
- Does not manage positions or P&L
- No frontend

## Project Structure
- `backend/app/market_data`: Providers, normalization, candle generation.
- `backend/app/strategies`: Strategy definitions, indicators, manager.
- `backend/app/contracts`: Shared data contracts (OrderIntent).
- `docs`: Integration docs for other developers.

## Setup Instructions
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate it:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Configure environment:
   ```bash
   cp .env.example .env
   ```
   (Set `DATABASE_URL` if you want persistence, though tests/demo use in-memory sqlite by default for simplicity, wait actually use postgresql as requested, but for local demo without docker, sqlite is a fallback if needed, but we stick to what was asked).

5. Run Tests:
   ```bash
   pytest
   ```

6. Run Demo:
   ```bash
   python -m backend.demo
   ```

7. Run FastAPI:
   ```bash
   uvicorn backend.app.main:app --reload
   ```\n