import time
import pandas as pd
import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Rutas (relativas al directorio del script) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(BASE_DIR, "clientes.xlsx")
ruta_base_pdf = os.path.join(BASE_DIR, "archivos")

# --- Preguntas iniciales ---
root = tk.Tk()
root.withdraw()

frecuencias_input = simpledialog.askstring(
    "Frecuencias", "¿A qué frecuencias querés enviar?\nEj: alta, media, baja"
)
if not frecuencias_input:
    sys.exit()
frecuencias = [f.strip().lower() for f in frecuencias_input.split(",")]

adjuntar_pdf = messagebox.askyesno("Adjuntar PDF", "¿Querés enviar archivos PDF adjuntos si están disponibles?")

tipos_input = simpledialog.askstring(
    "Tipo de mensaje", "¿Qué tipo de mensajes querés enviar?\nEj: mensaje 1, mensaje 2, mensaje 3"
)
if not tipos_input:
    sys.exit()
tipos_mensaje = [m.strip().lower() for m in tipos_input.split(",")]

# --- Leer Excel ---
df = pd.read_excel(ruta_excel)
df = df[df["Frecuencia"].str.lower().str.strip().isin(frecuencias)]
if df.empty:
    print("No hay usuarios con esas frecuencias.")
    sys.exit()

# --- Conexión a Chrome ya abierto (ver abri_chrome.bat) ---
DEBUG_PORT = 9223
opts = Options()
opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


# --- Función de envío ---
def enviar_mensaje(numero, mensaje, pdf):
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={numero}")
        wait = WebDriverWait(driver, 20)

        # 1) Enviar texto
        caja = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/footer//p")))
        caja.send_keys(mensaje, Keys.ENTER)
        time.sleep(3)

        # 2) Adjuntar y enviar PDF
        if pdf and adjuntar_pdf:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@title='Adjuntar']"))).click()

            file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
            file_input.send_keys(os.path.abspath(pdf))

            caption_box = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//*[@id='app']/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div[1]/span"
            )))
            time.sleep(3)
            caption_box.click()
            time.sleep(18)
            caption_box.send_keys(Keys.ENTER)

            wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@role='dialog']")))

        print(f"[OK] {numero}")

    except Exception as e:
        print(f"[ERROR] {numero}: {e}")


# --- Loop de envío ---
for _, row in df.iterrows():
    numero = str(row["Celular"])
    mensaje = " - ".join(
        str(row[t.title()]) for t in tipos_mensaje
        if t.title() in row and pd.notna(row[t.title()])
    ) + " Gracias!"

    pdf_name = row.get("Archivo_PDF", None)
    pdf_path = None
    if pd.notna(pdf_name) and str(pdf_name).strip():
        pdf_path = os.path.join(ruta_base_pdf, str(pdf_name))
        if not os.path.exists(pdf_path):
            pdf_path = None

    enviar_mensaje(numero, mensaje, pdf_path)

# --- Cierre ---
driver.quit()
