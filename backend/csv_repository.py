import csv
import json
from pathlib import Path
from typing import List, Dict

CSV_PATH = Path(__file__).parent.parent / "invoices.csv"

def ensure_csv_headers():
    if not CSV_PATH.exists():
        CSV_PATH.write_text(
            "invoice_number,invoice_date,due_date,vendor_name,vendor_tax_id,"
            "total_amount,currency,tax_amount,items_json\n"
        )

def append_invoice(invoice: Dict):
    ensure_csv_headers()
    items_json = json.dumps(invoice.get("line_items", []), ensure_ascii=False)

    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            invoice.get("invoice_number") or "",
            invoice.get("invoice_date") or "",
            invoice.get("due_date") or "",
            invoice.get("vendor_name") or "",
            invoice.get("vendor_tax_id") or "",
            invoice.get("total_amount") or 0.0,
            invoice.get("currency") or "",
            invoice.get("tax_amount") or 0.0,
            items_json,
        ])

def load_invoices() -> List[Dict]:
    if not CSV_PATH.exists():
        return []

    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        invoices = []
        for row in reader:
            row["items_json"] = json.loads(row["items_json"] or "[]")
            invoices.append(row)
        return invoices