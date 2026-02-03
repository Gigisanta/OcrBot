from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from ocr_service import extract_invoice_data
from csv_repository import append_invoice, CSV_PATH

load_dotenv()

app = FastAPI(title="Factura OCR", description="API para extracción de datos de facturas con Z.ai")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/invoices/extract")
async def extract_invoice_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        mime_type = file.content_type or "image/jpeg"

        invoice_data = extract_invoice_data(contents, mime_type)

        append_invoice(invoice_data)

        return {
            "status": "success",
            "message": "Factura procesada correctamente",
            "invoice": invoice_data
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la factura: {str(e)}")

@app.get("/api/invoices/csv")
async def download_csv():
    if not CSV_PATH.exists():
        raise HTTPException(status_code=404, detail="No hay facturas procesadas todavía")

    return FileResponse(
        CSV_PATH,
        filename="invoices.csv",
        media_type="text/csv"
    )

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)