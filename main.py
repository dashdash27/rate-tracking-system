import time
import os
import requests
from decimal import Decimal
from database import engine, SessionLocal
from models import Base, RequestLog, CurrencyRate

from logger_config import setup_logging

logger = setup_logging()

Base.metadata.create_all(bind=engine)

def fetch_and_save():
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    base_cur = os.getenv("BASE_CURRENCY", "USD")

    if not api_key:
        logger.error("Конфигурация провалена: EXCHANGE_RATE_API_KEY")
        return
    
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_cur}"

    try:
        db = SessionLocal()
        logger.info(f"--- Старт запроса (Базовый курс: {base_cur})")
        response = requests.get(url, timeout=10)
        status = response.status_code

        if status == 200:
            logger.info("API ответило успешно (200 OK)")
        else:
            logger.warning(f"API вернуло статус {status}")

        # Фиксируем запрос в бд
        new_request = RequestLog(
            status_code=status,
            base_currency=base_cur
        )
        db.add(new_request)
        db.flush()

        if status == 200:
            data = response.json()
            rates = data.get("conversion_rates", {})
            target_currencies = ["EUR", "RUB", "CNY", "GBP"]

            for code in target_currencies:
                if code in rates:
                    val = Decimal(str(rates[code]))

                    rate_entry = CurrencyRate(
                        request_id=new_request.id,
                        currency_code=code,
                        value=val
                    )
                    db.add(rate_entry)
            
            logger.info(f"Данные сохранены. ID записи: {new_request.id}")

        db.commit()

    except requests.exceptions.Timeout:
        logger.error("Таймаут: Сервер API слишком долго не отвечал")
        if db: db.rollback()
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка сети: Проблемы с интернет-соединением или DNS")
        if db: db.rollback()
    except Exception as e:
        logger.error(f"Системный сбой: {str(e)}")
        if db: db.rollback()
    finally:
        if db: db.close()

if __name__ == "__main__":
    interval_min = int(os.getenv("FETCH_INTERVAL", 5))
    
    logger.info(f"Скрипт запущен. Интервал: {interval_min} мин.")

    while True:
        fetch_and_save()
        time.sleep(interval_min * 60)