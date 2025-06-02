from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from config import settings
from whatsapp_api import WhatsAppAPI
from commands import (
    registration,
    room_check,
    payment,
    reports,
    broadcast,
    checkout,
    guest,
    faq,
)
from utils import validate_command, log_message

app = FastAPI(title="Fortis Home WhatsApp Bot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whatsapp_api = WhatsAppAPI(settings.WHATSAPP_API_TOKEN, settings.WHATSAPP_API_URL)

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    try:
        message = whatsapp_api.parse_incoming_message(data)
        log_message(message)
        command, args = validate_command(message)
        if command == "#daftar":
            response = registration.handle_registration(args)
        elif command == "#cek_kamar":
            response = room_check.handle_room_check(args)
        elif command == "#info_biaya":
            response = payment.handle_cost_info(args)
        elif command == "#lapor":
            response = reports.handle_report(args)
        elif command == "#bayar":
            response = payment.handle_payment(args)
        elif command == "#checkout":
            response = checkout.handle_checkout(args)
        elif command == "#tamu":
            response = guest.handle_guest_registration(args)
        elif command == "#faq":
            response = faq.handle_faq(args)
        elif command == "#broadcast":
            response = broadcast.handle_broadcast(args)
        else:
            response = "Maaf, perintah tidak dikenali. Ketik #faq untuk bantuan."
        await whatsapp_api.send_message(message.from_number, response)
        return JSONResponse(content={"status": "success"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
