import gspread

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

client = gspread.service_account("kassymtelegrambot.json", scopes=scope)