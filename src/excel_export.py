"""
Excel Export Module
Generate formatted Excel files from extracted data
Cloud-safe & Windows-safe
"""
import pandas as pd
import os

# -----------------------------------
# Excel file creator
# -----------------------------------
def create_excel_report(data_list, output_filename='pubmed_contacts.xlsx'):
    if not data_list:
        print("No data to export")
        return None

    # Ensure output directory exists
    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(data_list)

    column_order = [
        'DataSource','HCPName','Country','Province/State','City','Postal Code',
        'Email ID','Alternate Email','Assistant Email','Phone No.',
        'TherapyArea','Specialty','Sub-Specialty','Areas Of Expertise',
        'Affiliation/Institution','ProfileURL','Status','ProfileNotes',
        'Feedback','RecordUpdateDate','PublicationLinks','Date','Title'
    ]

    for col in column_order:
        if col not in df.columns:
            df[col] = ''

    df = df[column_order].sort_values(by=['Country','Specialty','HCPName']).reset_index(drop=True)

    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Contacts', index=False)
        ws = writer.sheets['Contacts']

        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        header_font = Font(color='FFFFFF', bold=True)

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')

        column_widths = {
            'A':14,'B':26,'C':14,'D':20,'E':18,'F':14,'G':36,'H':36,'I':36,'J':18,
            'K':22,'L':22,'M':26,'N':42,'O':55,'P':48,'Q':16,'R':30,'S':20,'T':22,
            'U':55,'V':16,'W':65
        }

        for col, width in column_widths.items():
            ws.column_dimensions[col].width = width

        thin = Border(left=Side(style='thin'), right=Side(style='thin'),
                      top=Side(style='thin'), bottom=Side(style='thin'))

        for row in ws.iter_rows(min_row=1, max_row=len(df)+1, min_col=1, max_col=len(column_order)):
            for cell in row:
                cell.border = thin
                if cell.row > 1:
                    cell.alignment = Alignment(wrap_text=True, vertical='top')

    print(f"Excel created: {output_filename}")
    return output_filename


# -----------------------------------
# Summary printer (needed by main.py)
# -----------------------------------
def print_summary_statistics(data_list):
    if not data_list:
        print("No data to summarize")
        return

    df = pd.DataFrame(data_list)

    print("="*50)
    print("EXTRACTION SUMMARY")
    print("="*50)
    print(f"Total Contacts: {len(df)}")

    if 'Country' in df.columns:
        print("\nBy Country:")
        for country, count in df['Country'].value_counts().items():
            print(f"  {country}: {count}")

    if 'Specialty' in df.columns:
        print("\nBy Specialty:")
        for sp, count in df['Specialty'].value_counts().head(10).items():
            print(f"  {sp}: {count}")

    if 'TherapyArea' in df.columns:
        vals = df[df['TherapyArea'] != '']['TherapyArea'].value_counts().head(10)
        if not vals.empty:
            print("\nBy Therapy Area:")
            for t, c in vals.items():
                print(f"  {t}: {c}")
