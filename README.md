

# 📃 monteScanPDF

![Static Badge](https://img.shields.io/badge/monte-ScanPDF-blue)

`monteScanPDF` es un script en Python 🐍 diseñado para automatizar el proceso de revisión y aprobación de facturas en departamentos financieros. Utiliza OCR (Reconocimiento Óptico de Caracteres) mediante la librería `tesseract` para identificar marcas de agua específicas ("REVISADO", "APROBADO") en documentos PDF y JPG, facilitando así el flujo de trabajo entre diferentes departamentos sin la necesidad de intervención manual.

## 🎯 Propósito

El objetivo de este script es minimizar el trabajo manual en los departamentos de facturación, permitiendo un procesamiento más rápido y eficiente de las facturas. Al automatizar la revisión y el marcaje de documentos como "REVISADO" o "APROBADO", se elimina la necesidad de interacciones directas para confirmar el estado de cada factura, mejorando la eficiencia operativa.

## 🤹‍♂️ Características

- **Automatización de la Revisión de Facturas**: Identifica automáticamente marcas de agua específicas en los documentos.
- **Gestión de Archivos en SMB**: Conexión y manipulación segura de archivos en servidores SMB.
- **Procesamiento de PDF y JPG**: Soporte para documentos en formatos PDF y JPG.
- **Logística de Documentos**: Renombra y transfiere documentos basándose en su estado de revisión/aprobación.
- **Persistencia de Logs**: Registro detallado de operaciones para seguimiento y auditoría.

## 🖥️ Requisitos

- Python 3.8 o superior 🐍
- Tesseract OCR
- Bibliotecas de Python: `PyMuPDF`, `pytesseract`, `PIL`, `tempfile`, `smb.SMBConnection`

## 📀 Instalación

```bash
git clone https://github.com/niskeletor/monteScanPDF.git
cd monteScanPDF
pip install -r requirements.txt
```

## ⚙️ Configuración

### Variables de Entorno

Se recomienda utilizar variables de entorno para configurar las credenciales de acceso y rutas de servidores:

```bash
export SAMBA_USERNAME=usuario@dominio.local
export SAMBA_PASSWORD=contraseña
export SAMBA_SERVIDOR_IP=direccionIPServidor
# Añade las variables de entorno necesarias para tu configuración
```

### Dockerización y Ejecución Programada

Para dockerizar el script y ejecutarlo automáticamente:

1. **Dockerfile**: Asegúrate de tener un `Dockerfile` configurado con todas las dependencias necesarias.
2. **Crontab**: Programa la ejecución con `crontab` para que se ejecute diariamente a las 2 de la madrugada.

## 🚀 Uso

Ejecuta el script con:

```bash
python app.py
```

## 📚 Documentación Adicional
>[!IMPORTANT]
>LIBRERÍAS NECESARIAS
>
Para más información sobre la instalación de Tesseract y las librerías necesarias, consulta los siguientes enlaces:

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/en/latest/)
- [Pytesseract](https://pypi.org/project/pytesseract/)

---

Espero que este borrador cumpla con tus expectativas y proporcione una base sólida para documentar tu proyecto en GitHub. Si necesitas ajustes adicionales o información específica, ¡estaré encantado de ayudarte!

## Contribuir

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor, haz un fork del repositorio y crea un pull request con tus cambios.
```bash
 ______  _                     _       
|  ___ \(_)                   | |      
| |   | |_  ___  ____ ___   _ | | ____ 
| |   | | |/___)/ ___) _ \ / || |/ _  )
| |   | | |___ ( (__| |_| ( (_| ( (/ / 
|_|   |_|_(___/ \____)___/ \____|\____)
```
## Licencia

![Licencia MIT](https://img.shields.io/badge/license-MIT-green)

Este proyecto está licenciado bajo MIT, siéntete de hacer el cambio que necesites!
Espero que esto sea para ti una palanca de ayuda si estás comenzando con el scripting o con algún lenguaje de programación
