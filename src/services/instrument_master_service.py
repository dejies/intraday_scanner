
"""
Instrument Master Service.

Skeleton production-ready service.
NOTE: Complete parser logic should be adapted to the exact Dhan CSV schema.
"""
from __future__ import annotations

import csv
from pathlib import Path
from collections import defaultdict

from src.models.instrument import Instrument
from src.services.base_service import BaseService
from src.services.http_client import HttpClient


class InstrumentMasterService(BaseService):

    CSV = {
        "security_id": "SEM_SMST_SECURITY_ID",
        "exchange": "SEM_EXM_EXCH_ID",
        "segment": "SEM_SEGMENT",
        "instrument_type": "SEM_INSTRUMENT_NAME",
        "symbol": "SEM_TRADING_SYMBOL",
        "custom_symbol": "SEM_CUSTOM_SYMBOL",
        "company_name": "SM_SYMBOL_NAME",
        "lot_size": "SEM_LOT_UNITS",
        "tick_size": "SEM_TICK_SIZE",
        "series": "SEM_SERIES",
        "expiry_date": "SEM_EXPIRY_DATE",
        "strike_price": "SEM_STRIKE_PRICE",
        "option_type": "SEM_OPTION_TYPE",
    }

    def __init__(self):
        super().__init__()
        self._by_symbol = {}
        self._by_security_id = {}
        self._by_exchange = defaultdict(list)
        self._by_segment = defaultdict(list)

    def download(self):
        client = HttpClient(
            base_url=self.settings.dhan_instrument_master_url,
            timeout=self.settings.api_timeout,
            retry_count=self.settings.retry_count,
            retry_delay=self.settings.retry_delay,
        )
        client.download("", self.settings.instrument_master_file)

    def load(self):
        path = Path(self.settings.instrument_master_file)
        if not path.exists():
            self.download()

        self._by_symbol.clear()
        self._by_security_id.clear()
        self._by_exchange.clear()
        self._by_segment.clear()

        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                inst = self._parse_row(row)
                if inst is None:
                    continue
                self._by_symbol[inst.symbol.upper()] = inst
                self._by_security_id[inst.security_id] = inst
                self._by_exchange[inst.exchange].append(inst)
                self._by_segment[inst.segment].append(inst)

    def _parse_row(self, row):
        try:
            c = self.CSV
            return Instrument(
                security_id=int(row[c["security_id"]]),
                exchange=row[c["exchange"]].strip(),
                segment=row[c["segment"]].strip(),
                instrument_type=row[c["instrument_type"]].strip(),
                symbol=row[c["symbol"]].strip(),
                custom_symbol=row[c["custom_symbol"]].strip(),
                company_name=row[c["company_name"]].strip(),
                lot_size=float(row[c["lot_size"]] or 0),
                tick_size=float(row[c["tick_size"]] or 0),
                series=row[c["series"]].strip() or None,
                expiry_date=row[c["expiry_date"]].strip() or None,
                strike_price=float(row[c["strike_price"]]) if row[c["strike_price"]] else None,
                option_type=row[c["option_type"]].strip() or None,
            )
        except Exception as ex:

            print("ERROR:", ex)
            print(row)

            return None

    def refresh(self):
        self.download()
        self.load()

    def get_all(self):
        return list(self._by_symbol.values())

    def get_by_symbol(self, symbol):
        return self._by_symbol.get(symbol.upper())

    def get_by_security_id(self, security_id):
        return self._by_security_id.get(int(security_id))

    def get_by_exchange(self, exchange):
        return list(self._by_exchange.get(exchange, []))

    def get_by_segment(self, segment):
        return list(self._by_segment.get(segment, []))

    def search_symbol(self, text):
        t=text.upper()
        return [i for s,i in self._by_symbol.items() if t in s]

    def search_company(self, text):
        t=text.upper()
        return [i for i in self._by_symbol.values() if t in i.company_name.upper()]