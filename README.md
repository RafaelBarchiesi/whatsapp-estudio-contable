# 📲 WhatsApp Bot – Estudio Contable

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-automation-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)](https://www.microsoft.com/windows)

Herramienta de automatización desarrollada para un estudio contable real. Permite enviar mensajes personalizados de WhatsApp de forma masiva a clientes, con la opción de adjuntar archivos PDF individuales (liquidaciones, facturas, informes) según cada destinatario.

---

## ⚙️ ¿Qué hace?

1. Lee una lista de clientes desde un archivo Excel (`clientes.xlsx`)
2. Pregunta via interfaz gráfica (tkinter) qué frecuencias y tipos de mensaje enviar
3. Se conecta a una sesión de Chrome ya abierta con WhatsApp Web (sin cerrar sesión)
4. Para cada cliente: envía el mensaje de texto y, si corresponde, adjunta el PDF específico

---

## 🖥️ Interfaz gráfica

Al ejecutar el script aparecen 3 ventanas que permiten configurar el envío sin tocar el código:

- **Frecuencias:** qué segmento de clientes contactar (`alta`, `media`, `baja`)
- **Adjuntar PDF:** si se quieren enviar archivos individuales
- **Tipo de mensaje:** qué columnas del Excel incluir en el mensaje

---

## 📂 Estructura del proyecto

```
/
├── enviar_mensaje.py       # Script principal
├── abri_chrome.bat         # Abre Chrome en modo debug (ejecutar primero)
├── clientes_ejemplo.csv    # Ejemplo de estructura del Excel
├── clientes.xlsx           # Tu archivo real (no incluido en el repo)
└── archivos/               # Carpeta con los PDFs a adjuntar
```

---

## 🛠 Tecnologías

| Librería | Uso |
|---|---|
| `Selenium` | Automatización de WhatsApp Web |
| `webdriver-manager` | Gestión automática del ChromeDriver |
| `Pandas` | Lectura y filtrado del Excel |
| `tkinter` | Interfaz gráfica para configurar el envío |

---

## ▶️ Cómo usarlo

### 1. Instalá las dependencias
```bash
pip install selenium webdriver-manager pandas openpyxl
```

### 2. Preparás el Excel
Creá un archivo `clientes.xlsx` con estas columnas:

| Celular | Frecuencia | Mensaje 1 | Mensaje 2 | Mensaje 3 | Archivo_PDF |
|---|---|---|---|---|---|
| 5491112345678 | alta | Vencimiento: 30/04 | Saldo: $15000 | | factura_001.pdf |

- El número debe incluir código de país (sin `+`): `549` para Argentina
- `Frecuencia`: `alta`, `media` o `baja`
- `Archivo_PDF`: nombre del archivo en la carpeta `/archivos` (opcional)

### 3. Abrís Chrome en modo debug
```
Doble click en abri_chrome.bat
```
Escaneás el QR de WhatsApp Web en esa ventana de Chrome. **Solo la primera vez.**

### 4. Ejecutás el script
```bash
python enviar_mensaje.py
```
Respondés las 3 preguntas de la GUI y el envío arranca automáticamente.

---

## ⚠️ Consideraciones

- Funciona en **Windows** (el `.bat` es para Windows; en Mac/Linux se puede adaptar)
- Requiere tener Chrome instalado
- WhatsApp puede detectar automatización si el volumen es muy alto — se recomienda usar con moderación
- El archivo `clientes.xlsx` real **no se sube al repo** por privacidad (está en `.gitignore`)

---

## 👤 Autor

**Rafael Barchiesi** — Desarrollado para uso profesional en estudio contable privado.
