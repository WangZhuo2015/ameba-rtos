ameba_internal_library(example_raw_spi_trx_interrupt)

target_sources(
    ${CURRENT_LIB_NAME} PRIVATE
    example_raw_spi_trx_interrupt.c
    app_example.c
)
