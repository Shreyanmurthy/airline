# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Invoice API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or ["http://localhost:5173"] if you want to pin it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Dummy data (simulate scraping) ----
INVOICES = [
    {"invoiceNo": "INV-1001", "date": "2025-07-30", "airline": "Thai Airways", "amount": 9800,  "gstin": "29ABCDE1234F1Z5"},
    {"invoiceNo": "INV-1002", "date": "2025-07-29", "airline": "IndiGo",       "amount": 12999, "gstin": "27PQRSX5678L2Z1"},
    {"invoiceNo": "INV-1003", "date": "2025-07-28", "airline": "Air India",    "amount": 7400,  "gstin": "07WXYZA9012K3Z6"},
    {"invoiceNo": "INV-1004", "date": "2025-07-26", "airline": "Thai Airways", "amount": 15500, "gstin": "29ABCDE1234F1Z5"},
    {"invoiceNo": "INV-1005", "date": "2025-07-25", "airline": "Vistara",      "amount": 11250, "gstin": "19LMNOP3456Q7Z9"},
]

@app.get("/")
def root():
    return {"ok": True, "message": "Invoice API running"}

# 1) Return list of invoices
@app.get("/invoices")
def get_invoices():
    return {"invoices": INVOICES}

# 2) Airline-wise total invoice values
@app.get("/summary")
def get_summary():
    totals = {}
    for inv in INVOICES:
        totals[inv["airline"]] = totals.get(inv["airline"], 0) + inv["amount"]
    # return as list for easy table rendering
    summary = [{"airline": k, "total": v} for k, v in totals.items()]
    return {"summary": summary}

# 3) "AI" suggest: invoices > ₹10,000 (rule-based)
@app.get("/ai-suggest")
def ai_suggest(min_amount: int = 10000):
    suggested = [inv for inv in INVOICES if inv["amount"] > min_amount]
    return {"rule": f"amount > ₹{min_amount}", "invoices": suggested}