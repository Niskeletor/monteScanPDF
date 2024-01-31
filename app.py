import fitz  # Importa PyMuPDF
import pytesseract
from PIL import Image
import tempfile
import os
from smb.SMBConnection import SMBConnection
import json
import logging
from ocr_utils import *

if __name__ == "__main__":

    # Declaracion de filtro para excluir mensajes específicos
    class ExcludeSpecificLogFilter(logging.Filter):
        def filter(self, record):
            # Define la cadena que deseas excluir
            exclude_message = 'Authentication with remote machine'

            # Si el mensaje de log contiene la cadena, no lo registres
            return exclude_message not in record.getMessage()

    # Configura el directorio donde se guardarán los logs
    log_directory = "./logs"
    os.makedirs(log_directory, exist_ok=True)

    # Configura el logging
    logging.basicConfig(filename=os.path.join(log_directory, 'scanFacturas.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    # Crea un filtro para excluir mensajes específicos
    exclude_filter = ExcludeSpecificLogFilter()
    logging.getLogger().addFilter(exclude_filter)

    smb_logger = logging.getLogger('SMB.SMBConnection')
    smb_logger.addFilter(exclude_filter)



    config = leer_configuracion('configuracion.json')
    
    for ruta_inicial in config['ruta_origen']:
        print(ruta_inicial)
        buscar_archivos_samba(config, 'APROBADO', ruta_inicial, config['ruta_destino'], '_rev', 'procesadas')
    
else:
    print('Im not a single module ! :(')