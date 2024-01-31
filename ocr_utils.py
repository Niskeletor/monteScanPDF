import fitz  # Importa PyMuPDF
import pytesseract
from PIL import Image
import tempfile
import os
from smb.SMBConnection import SMBConnection
import json
import logging


def crear_subdirectorio_si_no_existe(conn, shared_folder, subdirectorio):
    try:
        # Intenta listar el subdirectorio para ver si ya existe
        conn.listPath(shared_folder, subdirectorio)
        print('EXISTE SUBDIRECTORIO')
    except Exception as e:
        # Si ocurre un error al listar, asumimos que el subdirectorio no existe y lo creamos
        logging.info(f"Creando subdirectorio: {subdirectorio}")
        conn.createDirectory(shared_folder, subdirectorio)
        logging.info(f"Subdirectorio creado: {subdirectorio}")

def leer_configuracion(archivo_json):
    with open(archivo_json, 'r') as archivo:
        return json.load(archivo)

def ocr_en_imagen(file_path, keyword):
    # Función para procesar imagenes en JPG
    try:
        return keyword in pytesseract.image_to_string(Image.open(file_path))
    except IOError:
        return False

def ocr_en_pdf_con_fitz(file_path, keyword):
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        if keyword in pytesseract.image_to_string(img):
            return True
    return False

def buscar_archivos_samba(config, keyword, ruta_origen, ruta_destino, sufijo, subDirCopia):
    
    try:
        print('iniciando conexion')
        logging.info('iniciando conexion')
        conn = SMBConnection(config['username_samba'], config['password_samba'], "myclient", config['servidor_ip'], use_ntlm_v2=True, is_direct_tcp=True)
        print('conectando')
        logging.info('conectando')
        assert conn.connect(config['servidor_ip'], 445)
        print('conectado')
        logging.info('conectado')
        
    except Exception as e:
        print(e)
        logging.error(e)
    
    
    print('listando archivos')
    print(config['shared_folder'] + " Recurso compartido")
    print(ruta_origen + " Ruta origen")
    print(ruta_destino + " Ruta destino")
    print(keyword + " Palabra clave")
    
    try:
        files = conn.listPath(config['shared_folder'], ruta_origen)
        for file in files:
            if file.filename.endswith('.pdf') or file.filename.endswith('.jpg'):
                with tempfile.TemporaryDirectory() as tempdir:
                    file_path = os.path.join(tempdir, file.filename)
                    with open(file_path, 'wb') as fp:
                        conn.retrieveFile(config['shared_folder'], os.path.join(ruta_origen, file.filename), fp)

                    encontrado = False
                    if file.filename.endswith('.jpg'):
                        encontrado = ocr_en_imagen(file_path, keyword)
                        print('Buscando en imagen la palabra clave ' + keyword + ' en el archivo ' + file.filename + ' : ' + str(encontrado) + ' ruta: ' + file_path)
                        logging.info('Buscando en imagen la palabra clave ' + keyword + ' en el archivo ' + file.filename + ' : ' + str(encontrado) + ' ruta: ' + file_path)
                    elif file.filename.endswith('.pdf'):
                        encontrado = ocr_en_pdf_con_fitz(file_path, keyword)
                        print('Buscando en imagen la palabra clave ' + keyword + ' en el archivo ' + file.filename + ' : ' + str(encontrado) + ' ruta: ' + file_path)
                        logging.info('Buscando en imagen la palabra clave ' + keyword + ' en el archivo ' + file.filename + ' : ' + str(encontrado) + ' ruta: ' + file_path)

                        if encontrado:
                            # Separa el nombre del archivo de su extensión
                            print('encontrado en imagen la palabra clave ' + keyword + ' en el archivo ' + file.filename + ' : ' + str(encontrado) + ' ruta: ' + file_path)
                            logging.info('encontrado en imagen la palabra clave ' + keyword + ' en el archivo ' + file.filename + ' : ' + str(encontrado) + ' ruta: ' + file_path)
                            nombre_base, extension = os.path.splitext(file.filename)
                            
                            # Construye el nuevo nombre añadiendo '_rev' antes de la extensión
                            new_file_name = f"{nombre_base}{sufijo}{extension}"

                            procesadas_path = os.path.join(ruta_origen, 'procesadas', new_file_name)
                            destino_final_path = os.path.join(ruta_destino, new_file_name)
                            
                            # Verificar y crear el subdirectorio 'procesadas' si es necesario
                            crear_subdirectorio_si_no_existe(conn, config['shared_folder'], ruta_origen + '/' + subDirCopia )

                            try:
                                with open(file_path, 'rb') as fp:
                                    conn.storeFile(config['shared_folder'], procesadas_path, fp)
                                    print('Moviendo archivo a procesadas: ' + procesadas_path)
                                    logging.info('Moviendo archivo a procesadas: ' + procesadas_path)
                                    fp.seek(0)  # Regresa al inicio del archivo para leerlo nuevamente
                                    conn.storeFile(config['shared_folder'], destino_final_path, fp)
                                    print('Copiando archivo a destino final: ' + destino_final_path)
                                    logging.info('Copiando archivo a destino final: ' + destino_final_path)

                                # Si llegamos aquí, ambas operaciones de almacenamiento fueron exitosas
                                # Procedemos a eliminar el archivo original
                                conn.deleteFiles(config['shared_folder'], os.path.join(ruta_origen, file.filename))
                                print(f"Archivo original {file.filename} eliminado con éxito.")
                                logging.info(f"Archivo original {file.filename} eliminado con éxito.")
                                

                            except Exception as e:
                                print(f"Error durante el almacenamiento o eliminación del archivo: {e}")

    except Exception as e:
        print(e)                        
        
    finally:
    # Cerramos conexion
        conn.close()