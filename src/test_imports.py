from datetime import datetime
from decimal import Decimal

from builders import CandleBuilder
from models.tick import Tick


builder = CandleBuilder()

tick = Tick(
    security_id=1333,
    timestamp=datetime.now(),
    ltp=Decimal("1850.25"),
    volume=100,
)

result = builder.process_tick(tick)


timestamp = datetime.now()

tick1 = Tick(
    security_id=1333,
    timestamp=timestamp,
    ltp=Decimal("100"),
    volume=100,
)

tick2 = Tick(
    security_id=1333,
    timestamp=timestamp,
    ltp=Decimal("102"),
    volume=110,
)

builder = CandleBuilder()

builder.process_tick(tick1)
result = builder.process_tick(tick2)

from datetime import datetime
from decimal import Decimal

from builders import CandleBuilder
from models.tick import Tick

builder = CandleBuilder()

tick1 = Tick(
    security_id=1333,
    timestamp=datetime(2026, 7, 11, 9, 15, 10),
    ltp=Decimal("100"),
    volume=100,
)

tick2 = Tick(
    security_id=1333,
    timestamp=datetime(2026, 7, 11, 9, 15, 45),
    ltp=Decimal("102"),
    volume=110,
)

tick3 = Tick(
    security_id=1333,
    timestamp=datetime(2026, 7, 11, 9, 16, 5),
    ltp=Decimal("103"),
    volume=120,
)

builder.process_tick(tick1)
builder.process_tick(tick2)

result = builder.process_tick(tick3)

print("Completed:", result.completed_candles)
print("Current:", result.current_candle)