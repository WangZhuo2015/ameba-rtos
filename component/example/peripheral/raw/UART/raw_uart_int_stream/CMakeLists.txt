ameba_internal_library(example_raw_uart_int_stream)

target_sources(
    ${CURRENT_LIB_NAME} PRIVATE
    example_raw_uart_int_stream.c
    app_example.c
)
