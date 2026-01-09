"""
Excel Export Module
Generate formatted Excel files from extracted data
Cloud-safe & Windows-safe
"""
import pandas as pd
from datetime import datetime
import os

def create_excel_report(data_list, output_filename='pubmed_contacts.xlsx'):
    """
    Create Excel file from extracted data
    """
    if not data_list:
        print("No data to export!")
        return None

    # Ensure directory exists
    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Create DataFrame
    df = pd.DataFrame(data_list)

    # Define column order
    column_order = [
        'DataSource','HCPName','Country','Province/State','City','Postal Code',
        'Email ID','Alternate Email','Assistant Email','Phone No.',
        'TherapyArea','Specialty','Sub-Specialty','Areas Of Expertise',
        'Affiliation/Institution','ProfileURL','Status','ProfileNotes',
        'Feedback','RecordUpdateDate','PublicationLinks','Date','Title'
    ]

    # Ensure all columns exist
    for col in column_order:
        if col not in df.columns:
            df[col] = ''

    # Reorder & sort
    df = df[column_order].sort_values(by=['Country','Specialty','HCPName']).reset_index(drop=True)

    # Write Excel
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Contacts', index=False)

        worksheet = writer.sheets['Contacts']
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        header_font = Font(color='FFFFFF', bold=True)

        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')

        column_widths = {
            'A':14,'B':26,'C':14,'D':20,'E':18,'F':14,'G':36,'H':36,'I':36,'J':18,
            'K':22,'L':22,'M':26,'N':42,'O':55,'P':48,'Q':16,'R':30,'S':20,'T':22,
            'U':55,'V':16,'W':65
        }

        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width

        thin = Border(left=Side(style='thin'), right=Side(style='thin'),
                      top=Side(style='thin'), bottom=Side(style='thin'))

        for row in worksheet.iter_rows(min_row=1, max_row=len(df)+1, min_col=1, max_col=len(column_order)):
            for cell in row:
                cell.border = thin
                if cell.row > 1:
                    cell.alignment = Alignment(wrap_text=True, vertical='top')

    print(f"Excel file created: {output_filename}")
    print(f"Total contacts exported: {len(df)}")
    return output_filename
