from src.services.instrument_master_service import (
    InstrumentMasterService,
)


def main() -> None:

    service = InstrumentMasterService()

    #
    # Download (if required) and load.
    #
    service.load()

    print()

    print("=" * 70)
    print("Instrument Master Loaded Successfully")
    print("=" * 70)

    print()

    print("Statistics")

    print("-----------------------------")

    print(
        "Total Instruments :",
        len(service.get_all()),
    )

    print()

    #
    # Lookup by symbol
    #
    symbol = "INFY"

    instrument = service.get_by_symbol(
        symbol,
    )

    if instrument:

        print(
            f"{symbol} ->"
        )

        print(instrument)

    else:

        print(
            f"{symbol} not found."
        )

    print()

    #
    # Lookup by security id
    #
    security_id = 1594

    instrument = service.get_by_security_id(
        security_id,
    )

    if instrument:

        print(
            f"{security_id} ->"
        )

        print(instrument)

    else:

        print(
            f"{security_id} not found."
        )


if __name__ == "__main__":
    main()