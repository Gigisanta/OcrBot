import os
import base64
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict

load_dotenv()

api_key = os.getenv("ZAI_API_KEY")

if not api_key or api_key == "tu_api_key_aqui":
    raise ValueError(
        "API Key no configurada. Por favor, configura tu API Key de Z.ai en el archivo .env. "
        "Edita el archivo .env y reemplaza 'tu_api_key_aqui' con tu API Key real de Z.ai"
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://api.z.ai/api/paas/v4/"
)

def build_image_url_from_bytes(file_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"

def extract_invoice_data(file_bytes: bytes, mime_type: str = "image/jpeg") -> Dict:
    model = os.getenv("ZAI_MODEL", "glm-4.5v")
    image_url = build_image_url_from_bytes(file_bytes, mime_type)

    prompt = """Eres un asistente experto en extracción de datos de facturas.
Extrae de la imagen de la factura la siguiente información en formato JSON:

{
  "invoice_number": "...",
  "invoice_date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD o null si no aparece",
  "vendor_name": "...",
  "vendor_tax_id": "...",
  "total_amount": 0.0,
  "currency": "...",
  "tax_amount": 0.0,
  "line_items": [
    {
      "description": "...",
      "quantity": 0,
      "unit_price": 0.0,
      "amount": 0.0
    }
  ]
}

Si un campo no se puede determinar con seguridad, usa null o una cadena vacía.
Responde solo con el JSON, sin texto adicional ni markdown."""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            max_tokens=2048,
            temperature=0.0,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("El modelo no devolvió contenido")

        cleaned_content = content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[7:]
        if cleaned_content.startswith("```"):
            cleaned_content = cleaned_content[3:]
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]
        cleaned_content = cleaned_content.strip()

        invoice_data = json.loads(cleaned_content)
        return invoice_data

    except json.JSONDecodeError as e:
        raise ValueError(f"No se pudo parsear la respuesta JSON del modelo: {e}")
    except Exception as e:
        raise Exception(f"Error al llamar a la API de Z.ai: {e}")