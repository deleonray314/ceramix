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
gc = gspread.authorize(creds)
drive_service = build('drive', 'v3', credentials=creds)
    

def flujo_completo(nombre_hoja):
    try:
        # Carga de los datos
        sheet = gc.open(nombre_hoja).get_worksheet(0)
        datos = sheet.get_all_values()

        indices_borrar = []
        for i, valor in enumerate(datos):
            if "TOTAL" in valor or "VENTAS" in valor:
                indices_borrar.append(i)
        
        for idx in reversed(indices_borrar):
            sheet.delete_rows(idx)
        # Crear DataFrame
        df = pd.DataFrame(datos[1:], columns=datos[0])
        print(df.head(21))
    except Exception as e:
        print(f"Error: {e}")


flujo_completo(SHEET_NAME)
 
