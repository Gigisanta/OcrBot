# OcrBot - Invoice OCR with Z.ai

Sistema para extraer automáticamente datos de facturas utilizando el modelo OCR de Z.ai y guardarlos en un archivo CSV.

## Características

- Upload de imágenes de facturas (JPG/PNG)
- Extracción automática de campos con GLM-OCR de Z.ai
- Visualización de datos extraídos en tiempo real
- Almacenamiento en CSV
- Descarga del CSV con todas las facturas procesadas

## Campos Extraídos

- Número de factura
- Fecha de factura
- Fecha de vencimiento
- Nombre del proveedor
- ID fiscal (NIF/CIF)
- Importe total
- Moneda
- Importe de impuestos
- Líneas de factura (descripción, cantidad, precio unitario, importe)

## Requisitos

- Python 3.11+
- API Key de Z.ai

## Instalación

1. Clonar o descargar el proyecto

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la API Key de Z.ai:
   - Abrir el archivo `.env`
   - Reemplazar `tu_api_key_aqui` con tu API Key real de Z.ai

## Ejecución

1. Iniciar el servidor (con hot reload activado):
```bash
cd backend
python main.py
```

O usa uvicorn directamente:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Hot Reload**: El servidor se reinicia automáticamente cuando guardas cambios en los archivos Python.

2. Abrir el navegador en:
```
http://localhost:8000
```

## Uso

1. Sube una imagen de factura arrastrándola o haciendo clic en "Seleccionar archivo"
2. El sistema procesará la imagen con Z.ai OCR
3. Revisa los datos extraídos
4. Descarga el CSV con el botón "Descargar CSV" cuando quieras exportar todas las facturas

## Estructura del Proyecto

```
factura-ocr/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── ocr_service.py       # Cliente Z.ai GLM-OCR
│   ├── csv_repository.py    # Manejo de CSV
│   └── invoices.csv         # Se genera automáticamente
├── frontend/
│   ├── index.html           # Formulario upload + visualización
│   └── app.js               # API calls + lógica UI
├── .env                     # ZAI_API_KEY, ZAI_MODEL
├── requirements.txt         # Dependencias
└── README.md               # Guía de uso
```

## API Endpoints

### POST /api/invoices/extract
Subir imagen y extraer datos

**Request:**
- Body: multipart/form-data con el archivo `file`

**Response:**
```json
{
  "status": "success",
  "message": "Factura procesada correctamente",
  "invoice": {
    "invoice_number": "...",
    "invoice_date": "YYYY-MM-DD",
    "due_date": "YYYY-MM-DD",
    "vendor_name": "...",
    "vendor_tax_id": "...",
    "total_amount": 0.0,
    "currency": "...",
    "tax_amount": 0.0,
    "line_items": [...]
  }
}
```

### GET /api/invoices/csv
Descargar el CSV con todas las facturas

### GET /api/health
Health check de la API

## Configuración

Variables de entorno en `.env`:

- `ZAI_API_KEY`: Tu API Key de Z.ai (obligatoria)
- `ZAI_MODEL`: Modelo a usar (default: glm-ocr)

## Modelos Soportados

- GLM-OCR: Modelo especializado en documentos
- GLM-4.5V: Modelo vision multimodal
- GLM-4.6V: Versión más reciente con mejor reasoning

## Notas

- El CSV se genera automáticamente en `invoices.csv`
- Cada factura procesada se añade como una nueva fila
- Las imágenes se procesan con un prompt optimizado para facturas

## Troubleshooting

**Error: "No se pudo parsear la respuesta JSON"**
- Verifica que el modelo Z.ai esté respondiendo correctamente
- Intenta con otro modelo (cambia ZAI_MODEL en .env)

**Error: "API Key inválida"**
- Verifica que tu API Key de Z.ai sea correcta
- Asegúrate de tener cuota disponible

**No se detectan campos**
- Asegúrate de que la imagen sea clara y legible
- Prueba con diferentes formatos de factura

## Roadmap

- Soporte para PDF
- Autenticación de usuarios
- Base de datos (PostgreSQL)
- Interfaz con historial de facturas
- Filtros y búsqueda
