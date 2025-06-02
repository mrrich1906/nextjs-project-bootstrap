from typing import Dict, Any, List, Optional
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import settings
import logging

class GoogleSheetsClient:
    def __init__(self):
        try:
            # Load credentials from environment variable
            creds_json = json.loads(settings.GOOGLE_SHEETS_CREDENTIALS)
            credentials = Credentials.from_service_account_info(
                creds_json,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            self.spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID
            
        except Exception as e:
            logging.error(f"Failed to initialize Google Sheets client: {e}")
            raise

    async def get_sheet_data(self, sheet_name: str) -> List[Dict[str, Any]]:
        """
        Get all data from a specific sheet as list of dictionaries
        Each dictionary represents a row with column headers as keys
        """
        try:
            # Get the sheet data
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            # First row contains headers
            headers = values[0]
            
            # Convert remaining rows to dictionaries
            return [
                {headers[i]: value for i, value in enumerate(row)}
                for row in values[1:]
            ]
            
        except Exception as e:
            logging.error(f"Failed to get sheet data: {e}")
            raise

    async def append_row(self, sheet_name: str, data: Dict[str, Any]) -> None:
        """
        Append a new row to the specified sheet
        Data should be a dictionary with column headers as keys
        """
        try:
            # Get current headers
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!1:1"
            ).execute()
            
            headers = result.get('values', [[]])[0]
            
            # Prepare row data in correct order
            row_data = [data.get(header, "") for header in headers]
            
            # Append the row
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name,
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={
                    'values': [row_data]
                }
            ).execute()
            
        except Exception as e:
            logging.error(f"Failed to append row: {e}")
            raise

    async def update_cell(self, sheet_name: str, cell: str, value: Any) -> None:
        """Update a specific cell in the sheet"""
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!{cell}",
                valueInputOption='USER_ENTERED',
                body={
                    'values': [[value]]
                }
            ).execute()
            
        except Exception as e:
            logging.error(f"Failed to update cell: {e}")
            raise

    async def update_row(self, sheet_name: str, row_number: int, data: Dict[str, Any]) -> None:
        """Update an entire row in the sheet"""
        try:
            # Get current headers
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!1:1"
            ).execute()
            
            headers = result.get('values', [[]])[0]
            
            # Prepare row data in correct order
            row_data = [data.get(header, "") for header in headers]
            
            # Update the row
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A{row_number}",
                valueInputOption='USER_ENTERED',
                body={
                    'values': [row_data]
                }
            ).execute()
            
        except Exception as e:
            logging.error(f"Failed to update row: {e}")
            raise

    async def find_row(self, sheet_name: str, column: str, value: Any) -> Optional[int]:
        """Find the row number where column matches value"""
        try:
            # Get all data
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return None
            
            # Find column index
            headers = values[0]
            try:
                col_idx = headers.index(column)
            except ValueError:
                raise ValueError(f"Column '{column}' not found")
            
            # Find matching row
            for i, row in enumerate(values[1:], start=2):
                if len(row) > col_idx and row[col_idx] == value:
                    return i
            
            return None
            
        except Exception as e:
            logging.error(f"Failed to find row: {e}")
            raise

    async def create_backup(self) -> None:
        """Create a backup of all sheets in the spreadsheet"""
        try:
            # Get all sheet names
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheet_names = [sheet['properties']['title'] 
                         for sheet in spreadsheet['sheets']]
            
            # Create new spreadsheet for backup
            backup_spreadsheet = self.service.spreadsheets().create(body={
                'properties': {
                    'title': f'Backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                }
            }).execute()
            
            # Copy each sheet to backup
            for sheet_name in sheet_names:
                data = await self.get_sheet_data(sheet_name)
                if data:
                    headers = list(data[0].keys())
                    values = [headers]
                    values.extend([[row.get(h, "") for h in headers] for row in data])
                    
                    self.service.spreadsheets().values().update(
                        spreadsheetId=backup_spreadsheet['spreadsheetId'],
                        range=f"{sheet_name}!A1",
                        valueInputOption='RAW',
                        body={
                            'values': values
                        }
                    ).execute()
            
        except Exception as e:
            logging.error(f"Failed to create backup: {e}")
            raise

# Singleton instance
_sheets_client = None

def get_sheets_client() -> GoogleSheetsClient:
    """Get or create singleton instance of GoogleSheetsClient"""
    global _sheets_client
    if _sheets_client is None:
        _sheets_client = GoogleSheetsClient()
    return _sheets_client
