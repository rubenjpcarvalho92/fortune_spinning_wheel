import logging

# Configuração do logger
def setup_logger():
    # Formato do logger
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,  # Nível de log (DEBUG, INFO, WARNING, ERROR)
        format=log_format,
        handlers=[
            logging.FileHandler("app.log"),  # Grava os logs no ficheiro "app.log"
            logging.StreamHandler()          # Exibe os logs no console
        ]
    )

    # Retorna o logger configurado
    return logging.getLogger(__name__)
