import logging

# Configuração do logger
def setup_logger():
    # Formato do logger
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler("app.log")  # Apenas ficheiro, sem consola
        ]
    )

    return logging.getLogger(__name__)
