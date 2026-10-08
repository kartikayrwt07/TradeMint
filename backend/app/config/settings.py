from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    market_data_provider: str = "mock"
    database_url: str = "sqlite+aiosqlite:///:memory:"

    strategy_a_enabled: bool = True
    strategy_a_quantity: int = 50
    ma_fast_period: int = 5
    ma_slow_period: int = 20

    strategy_b_enabled: bool = True
    strategy_b_quantity: int = 50
    momentum_period: int = 5
    momentum_threshold: float = 0.005

    strategy_c_enabled: bool = True
    strategy_c_quantity: int = 50
    breakout_lookback: int = 20

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
