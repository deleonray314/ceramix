##############################################
# Modificación de los datos en El Google Drive 
##############################################

# Import libraries 
import pandas as pd
import gspread
import io
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración desde el .env
CUENTA_DE_SERVICIO = os.getenv("GOOGLE_APP_CREDENTIALS")
FOLDER_ID = os.getenv('CARPETA_DESTINO')
SHEET_NAME = os.getenv('SHEET_NAME')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(CUENTA_DE_SERVICIO, scopes=SCOPES)
client = gspread.authorize(creds)
drive_service = build('drive', 'v3', credentials=creds)
    

def flujo_completo(nombre_hoja):
    try:
        # Carga de los datos
        spreadsheet = client.open(nombre_hoja)
        sheet = spreadsheet.get_worksheet(0)

        #sheet.delete_rows(2)  En caso de recibir un encabezado Se elimnan las 2 primeras filas de la hoja 


        datos = sheet.get_all_values()
        sheet.id # El id de la hoja puede ser necesario

        # Indentificar indices de las filas a borrar 
        indices_borrar = [i for i, fila in enumerate(datos)
        if any(palabra in str(fila) for palabra in ['TOTAL', 'VENTAS', 'CANTIDAD FACTURAS','CANTIDAD DEVOLUCIONES'])
        ]
        indices_borrar.sort(reverse=True)
      
        if not indices_borrar:
            print('No se encontraron filas para borrar')    
            return
        
        # Construir el request para ek batch_update
        requests = []
        for idx in indices_borrar:
            requests.append({
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet.id,
                        "dimension": "ROWS",
                        "startIndex": idx,
                        "endIndex": idx + 1
                    }
                }
            })
        
        # Ejecutar el batch_update
        spreadsheet.batch_update({"requests": requests})

        print(f'Se eliminaron {len(indices_borrar)} filas')
        
        # Recargar datos después de eliminar filas para el DataFrame
        datos = sheet.get_all_values()
        
        # Crear DataFrame
        df = pd.DataFrame(datos[1:], columns=datos[0])
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")


flujo_completo(SHEET_NAME)
 
