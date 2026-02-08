# legacy-modern-payment-gateway
Anti-Corruption Layer converting JSON APIs to Fixed-Width Mainframe Formats (ISO 8583 style).
# Legacy-to-Cloud Payment Gateway (ACL)

## Project Overview
This project demonstrates an **Anti-Corruption Layer (ACL)** pattern, commonly used in banking modernization. It serves as a middleware bridge between modern Digital Channels (REST/JSON) and Legacy Core Banking Systems (Fixed-Width/COBOL).

## The Problem
Modern mobile apps (Stripe, GPay) communicate via **JSON**.
Legacy Mainframes (FIS Systematics, CICS) require **Fixed-Width, Positional Data**.
Directly connecting them causes tight coupling and fragility.

## The Solution
This Python Microservice acts as a translator:
1.  **Ingress:** Accepts a standard `JSON` payload.
2.  **Validation:** Enforces strict data types (Pydantic models act as the "Linkage Section").
3.  **Transformation:** Converts data into a 26-byte **Fixed-Width String** (simulating a COBOL Copybook input).
4.  **Processing:** Handles "Implied Decimal" logic for currency (e.g., `$150.00` becomes `00015000`).

## Tech Stack
- **Language:** Python 3.10+
- **Framework:** FastAPI (High-performance Async API)
- **Validation:** Pydantic
- **Architecture:** Domain-Driven Design (Anti-Corruption Layer)

## Usage
**Input (JSON):**
```json
{
  "account_id": "12345",
  "amount": 150.50,
  "currency": "USD"
}
