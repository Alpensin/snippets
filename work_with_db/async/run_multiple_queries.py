import asyncio
import functools
import logging
from time import monotonic

import asyncpg
from pydantic import BaseSettings, SecretStr

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.FileHandler('time_logs.log')
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s; %(name)s; %(levelname)s; %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    TASKS_QTY: int = 10
    DATABASE_HOST: SecretStr = SecretStr('localhost')
    DATABASE_PORT: int = 5432
    DATABASE_USER: SecretStr = SecretStr('test')
    DATABASE_PASSWORD: SecretStr = SecretStr('test')
    DATABASE_DATABASE: SecretStr = SecretStr('test')
    TASKS_QTY: int = 10

settings = Settings()

QUERY_1 = ''
QUERY_2 = ''
QUERY_3 = ''
QUERY_4 = ''
QUERY_5 = ''
QUERY_6 = ''

QUERIES = (QUERY_1, QUERY_2, QUERY_3, QUERY_4, QUERY_5, QUERY_6)


def async_timed():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            logger.info("%s started args=%s, kwargs=%s", func, args, kwargs)
            start = monotonic()
            try:
                return await func(*args, **kwargs)
            finally:
                end = monotonic()
                total = end - start
                logger.info("%s finished args=%s, kwargs=%s. Execution time: %s sec", func, args, kwargs, total)
        return wrapped
    return wrapper


@async_timed()
async def run_query(connection, query):
    result = await connection.fetch(query)
    return result


@async_timed()
async def run_query_task(pool, query):
    results_rows_qty = []
    for query in QUERIES:
        try:
            async with pool.acquire() as connection:
                result = await run_query(connection, query)
                results_rows_qty.append(len(result))
        except Exception:
            logger.exception('Неуспешный запрос %s', query)
    return 'Done'


async def main(tasks_qty=10):
    async with asyncpg.create_pool(
                        host=settings.DATABASE_HOST.get_secret_value(),
                        port=settings.DATABASE_PORT,
                        user=settings.DATABASE_USER.get_secret_value(),
                        password=settings.DATABASE_PASSWORD.get_secret_value(),
                        database=settings.DATABASE_DATABASE.get_secret_value(),
                        min_size=tasks_qty,
                        max_size=tasks_qty,) as pool:
        tasks = []
        for _ in range(tasks_qty):
            task = run_query_task(pool, tasks_qty)
            tasks.append(task)
        logger.info("Execution started")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(results)
        logger.info("Execution finished")


asyncio.run(main(tasks_qty=settings.TASKS_QTY))
