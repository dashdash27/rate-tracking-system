import logging
import sys

def setup_logging():
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # обработчик для всех событий -> app.log
    all_logs_handler = logging.FileHandler("app.log", encoding='utf-8')
    all_logs_handler.setLevel(logging.INFO)
    all_logs_handler.setFormatter(formatter)

    # обработчик только для ошибок и таймаутов -> errors.log
    errors_handler = logging.FileHandler("errors.log", encoding='utf-8')
    errors_handler.setLevel(logging.ERROR)
    errors_handler.setFormatter(formatter)

    # обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(all_logs_handler)
    root_logger.addHandler(errors_handler)
    root_logger.addHandler(console_handler)

    return logging.getLogger("currency_tracker")