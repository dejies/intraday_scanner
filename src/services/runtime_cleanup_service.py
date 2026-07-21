class RuntimeCleanupService:

    def __init__(
        self,
        instrument_master_service,
        market_data_store,
        candle_builder,
        indicator_service,
        scanner,
    ):
        self.instrument_master_service = instrument_master_service
        self.market_data_store = market_data_store
        self.candle_builder = candle_builder
        self.indicator_service = indicator_service
        self.scanner = scanner

    def remove_symbol(self, symbol: str):

        self.market_data_store.remove_symbol(symbol)

        instrument = self.instrument_master_service.get_by_symbol(symbol)

        if instrument is not None:
            self.candle_builder.remove_security(
                instrument.security_id
            )

        self.indicator_service.remove_symbol(symbol)
        self.scanner.remove_symbol(symbol)