import re
import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from config import settings

def validate_phone_number(phone: str) -> bool:
    """Validate Indonesian phone number format"""
    pattern = r'^08[0-9]{8,11}$'
    return bool(re.match(pattern, phone))

def validate_room_number(room: str) -> bool:
    """Validate if room number exists"""
    return room in settings.AVAILABLE_ROOMS

def validate_command(message: Dict[str, Any]) -> Tuple[str, list]:
    """
    Validate and parse WhatsApp command
    Returns tuple of (command, arguments)
    """
    try:
        text = message.get("text", "").strip()
        if not text or not text.startswith("#"):
            raise ValueError("Invalid command format")

        parts = text.split()
        command = parts[0].lower()
        args = parts[1:]

        # Add sender's phone number to args for context
        args_dict = {
            "from_number": message.get("from_number"),
            "args": args
        }

        return command, args_dict

    except Exception as e:
        logging.error(f"Command validation error: {e}")
        raise ValueError("Invalid command format")

def is_admin(phone_number: str) -> bool:
    """Check if phone number belongs to admin"""
    return phone_number in settings.ADMIN_PHONE_NUMBERS

def calculate_deposit_return(deposit: float, maintenance_costs: float) -> float:
    """Calculate deposit return amount after deducting maintenance costs"""
    return max(0, deposit - maintenance_costs)

def format_currency(amount: float) -> str:
    """Format amount as Indonesian Rupiah"""
    return f"Rp {amount:,.0f}"

def log_message(message: Dict[str, Any]) -> None:
    """Log incoming WhatsApp message"""
    try:
        log_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from": message.get("from_number", "unknown"),
            "message": message.get("text", ""),
            "media_url": message.get("media_url", "")
        }
        
        logging.info(f"Incoming message: {log_data}")
        
    except Exception as e:
        logging.error(f"Logging error: {e}")

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def generate_invoice_number() -> str:
    """Generate unique invoice number"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"INV-{timestamp}"

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection"""
    # Remove any potential harmful characters
    return re.sub(r'[<>{}[\]\\]', '', text)

def validate_payment_amount(amount: float, expected: float, tolerance: float = 0.01) -> bool:
    """Validate if payment amount matches expected amount within tolerance"""
    return abs(amount - expected) <= tolerance

def get_sheet_name_for_month(base_name: str) -> str:
    """Get sheet name with current month suffix"""
    return f"{base_name}_{datetime.now().strftime('%Y_%m')}"

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format"""
    # Remove any non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Ensure starts with '08' for Indonesian numbers
    if digits.startswith('62'):
        digits = '0' + digits[2:]
    
    return digits

def calculate_late_fee(days_late: int, rent_amount: float) -> float:
    """Calculate late payment fee"""
    if days_late <= 0:
        return 0
    
    # 5% penalty per week, maximum 20%
    weeks_late = (days_late + 6) // 7  # Round up to nearest week
    penalty_rate = min(weeks_late * 0.05, 0.20)
    
    return rent_amount * penalty_rate

def get_reminder_message(tenant_name: str, room_number: str, days_until_due: int) -> str:
    """Get payment reminder message based on days until due"""
    if days_until_due > 5:
        return (
            f"🔔 Reminder Pembayaran\n\n"
            f"Halo {tenant_name},\n"
            f"Pembayaran kost untuk kamar {room_number}\n"
            f"akan jatuh tempo dalam {days_until_due} hari.\n\n"
            "Mohon siapkan pembayaran tepat waktu.\n"
            "Terima kasih 🙏"
        )
    elif days_until_due > 0:
        return (
            f"⚠️ Reminder Pembayaran Segera\n\n"
            f"Halo {tenant_name},\n"
            f"Pembayaran kost untuk kamar {room_number}\n"
            f"akan jatuh tempo dalam {days_until_due} hari.\n\n"
            "Mohon segera lakukan pembayaran\n"
            "untuk menghindari denda keterlambatan.\n"
            "Terima kasih 🙏"
        )
    else:
        return (
            f"🚨 Pembayaran Telat\n\n"
            f"Halo {tenant_name},\n"
            f"Pembayaran kost untuk kamar {room_number}\n"
            f"telah melewati jatuh tempo.\n\n"
            "Mohon segera lunasi pembayaran\n"
            "untuk menghindari denda tambahan.\n"
            "Terima kasih 🙏"
        )

def format_duration(minutes: int) -> str:
    """Format duration in minutes to human readable string"""
    if minutes < 60:
        return f"{minutes} menit"
    elif minutes < 1440:  # Less than 24 hours
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours} jam {mins} menit" if mins else f"{hours} jam"
    else:
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        return f"{days} hari {hours} jam" if hours else f"{days} hari"
