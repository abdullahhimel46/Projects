import openpyxl

def create_accounts_file(filename):
    # Sample account data
    accounts_data = [
        ["Account Number", "Account Holder", "Balance"],
        ["123456", "Moinul Islam", 1000.0],
        ["654321", "Hasan Ali", 1500.0],
        ["789012", "Abu Shale", 2000.0]
    ]

    # Create a new workbook and select the active sheet
    wb = openpyxl.Workbook()
    ws = wb.active

    # Write account data to the sheet
    for row in accounts_data:
        ws.append(row)

    # Save the workbook to the specified filename
    wb.save(filename)

    print(f"{filename} created successfully with sample data!")

# Create the accounts.xlsx file
create_accounts_file("accounts.xlsx")
