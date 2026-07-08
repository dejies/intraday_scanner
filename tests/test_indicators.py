from src.services.market_data import MarketData
from src.services.historical_data import HistoricalDataService
from src.indicators import IndicatorEngine


market_data = MarketData()

history = HistoricalDataService(
    market_data=market_data,
)

history.load()

engine = IndicatorEngine()

indicators = engine.calculate(
    "INFY",
    market_data.get_candles("INFY"),
)

print(indicators)