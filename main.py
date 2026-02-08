from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime

# --- INITIALIZE THE "CICS REGION" (The API Server) ---
app = FastAPI(
    title="Legacy-to-Cloud Payment Gateway",
    description="Anti-Corruption Layer (ACL) converting JSON to Fixed-Width Mainframe formats.",
    version="1.0.0"
)

# --- 1. THE LINKAGE SECTION (Data Definition) ---
# This acts like a COBOL Copybook. It enforces strict input validation.
class PaymentRequest(BaseModel):
    account_id: str  # Target: 10 Bytes (Right Justified)
    amount: float    # Target: 8 Bytes (Implied Decimal)
    currency: str    # Target: 3 Bytes (ISO Code)

# --- 2. THE PROCEDURE DIVISION (Transformation Logic) ---
def to_mainframe_format(account: str, amount: float) -> str:
    """
    Simulates a COBOL 'MOVE' and 'STRING' operation.
    Converts modern types into a Fixed-Width String (ISO 8583 style).
    
    Target Layout (26 Bytes Total):
    [01-10] Account Number (Right Justified, Zero Padded)
    [11-18] Amount (Implied Decimal, Zero Padded)
    [19-26] Date (YYYYMMDD)
    """
    # LOGIC: Pad Account Number with Zeros (e.g., "123" -> "0000000123")
    acc_str = account.rjust(10, '0') 
    
    # LOGIC: Handle Implied Decimal (e.g., 150.50 -> "00015050")
    # We format to 2 decimal places, then remove the dot.
    amt_str = f"{amount:08.2f}".replace('.', '') 
    
    # LOGIC: Get System Date
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    
    # LOGIC: Concatenate (STRING command)
    return f"{acc_str}{amt_str}{date_str}"

# --- 3. THE TRANSACTION ID (API Endpoint) ---
@app.post("/process-transaction/")
async def process_transaction(payment: PaymentRequest):
    try:
        # Step A: Anti-Corruption Layer (Translation)
        legacy_payload = to_mainframe_format(payment.account_id, payment.amount)
        
        # Step B: Log the "Mainframe" Input (Evidence for the logs)
        print(f"Sending to Core Banking System: [{legacy_payload}]")
        
        # Step C: Return Success (Simulating CICS Return Code 00)
        return {
            "status": "success",
            "message": "Translated JSON to Legacy Fixed-Width",
            "mainframe_string": legacy_payload,
            "byte_length": len(legacy_payload),
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        # Step D: Error Handling (Simulating an ABEND)
        raise HTTPException(status_code=500, detail=f"Translation Error: {str(e)}")

# To run locally: uvicorn main:app --reload
