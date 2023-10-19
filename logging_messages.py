# Встреченное. Не всё best practice.

except Exception as e:
    logger.error('Service can not be started: %r', e, exc_info=exc_info())

logger.debug('Sending request %s with kwargs %s', command, request_kwargs)

logger.error('Raise unhandled exception. Rollback transaction', exc_info=e)

logger.log(level, 'Drill calculation error: %s', repr(exc_val), exc_info=exc_val) # repr по идее заменяется %r

logger.info('Получен запрос для расчета кеша: %r.', request)

logger.info(message, *logger_args, extra={"color_message": color_message})

except Exception:
    logger.exception('Фоновая задача завершилась с ошибкой')
    raise
