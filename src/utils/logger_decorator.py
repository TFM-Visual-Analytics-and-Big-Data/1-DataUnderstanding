from functools import wraps
import logging
import time

logger = logging.getLogger('log/pipelineError')

def handle_errors(retries: int = 3, delay: float = 1.0):
    """
    Decorador para manejo robusto de errores con reintentos
    
    Args:
        retries: Número de reintentos
        delay: Tiempo de espera entre reintentos (segundos)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"Intento {attempt + 1} fallido para {func.__name__}: {str(e)}"
                    )
                    if attempt < retries - 1:
                        time.sleep(delay)
            
            logger.error(
                f"Todos los intentos fallaron para {func.__name__}. Último error: {str(last_error)}"
            )
            raise last_error
        return wrapper
    return decorator