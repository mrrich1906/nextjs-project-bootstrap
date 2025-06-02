# Fortis Home WhatsApp Bot Backend

Backend service for managing Fortis Home boarding house (kost) through WhatsApp automation.

## Features

- 📝 Tenant registration with data validation
- 🏠 Room availability checking with images
- 💰 Payment handling and confirmation
- 📊 Google Sheets integration for admin dashboard
- 📢 Broadcast messaging to tenants
- ✅ Automated check-in/check-out process
- 👥 Guest registration system
- 🔔 Payment reminders
- ❓ FAQ and help system

## Prerequisites

- Python 3.8+
- WhatsApp Business API account (Twilio/UltraMsg)
- Google Cloud Project with Sheets API enabled
- Google Service Account with appropriate permissions

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-repo/fortis-home-bot.git
cd fortis-home-bot/backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp sample.env .env
```
Edit `.env` with your configuration:
- WhatsApp API credentials
- Google Sheets credentials
- Admin phone numbers
- Room configuration
- Other settings

5. Set up Google Sheets:
- Create a new Google Spreadsheet
- Share it with your service account email
- Copy the spreadsheet ID from the URL
- Add it to your `.env` file

## Running the Service

1. Start the server:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

2. Configure webhook URL in your WhatsApp Business API:
```
https://your-domain/webhook
```

## Bot Commands

### Tenant Commands
- `#daftar <nama> <nomor_hp> <nomor_kamar>` - Register as new tenant
- `#cek_kamar [nomor_kamar]` - Check room availability
- `#info_biaya [nomor_kamar]` - Get cost information
- `#bayar` - Upload payment proof (with image)
- `#lapor <jenis> <deskripsi>` - Report issues
- `#checkout [tanggal]` - Request check-out
- `#tamu <nama> <nomor_hp> <durasi>` - Register guest
- `#faq [topik]` - Get help information

### Admin Commands
- `#broadcast <pesan>` - Send message to all tenants
- `#broadcast <tipe> <pesan>` - Send to specific tenant type
- `#checkout_admin <kamar> <approve/reject>` - Handle checkout

## Google Sheets Structure

The system uses the following sheets:
1. **Penghuni** (Tenants)
   - nomor_kamar
   - nama
   - nomor_hp
   - tanggal_masuk
   - status

2. **Kamar** (Rooms)
   - nomor_kamar
   - lantai
   - ukuran
   - harga
   - fasilitas
   - foto_url

3. **Pembayaran** (Payments)
   - tanggal
   - nomor_kamar
   - nama_penghuni
   - jumlah
   - bukti_url
   - status

4. **Laporan** (Reports)
   - tanggal
   - nomor_kamar
   - nama_penghuni
   - jenis_laporan
   - deskripsi
   - status

5. **Tamu** (Guests)
   - tanggal
   - nomor_kamar
   - nama_penghuni
   - nama_tamu
   - nomor_hp_tamu
   - durasi_jam
   - status

## Development

### Code Structure
- `app.py` - Main FastAPI application
- `config.py` - Configuration management
- `whatsapp_api.py` - WhatsApp API integration
- `google_sheets.py` - Google Sheets integration
- `commands/` - Command handlers
- `utils.py` - Utility functions

### Testing
```bash
pytest
```

### Linting
```bash
flake8 .
black .
isort .
```

## Deployment

1. Set up a VPS or cloud server
2. Install dependencies
3. Configure environment variables
4. Set up SSL certificate
5. Configure reverse proxy (nginx)
6. Run with production server:
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
