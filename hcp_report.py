import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
import logging

# =============================
# CONFIG
# =============================
EXCEL_FILE = r"C:\Users\U6079602\OneDrive - Clarivate Analytics\Desktop\Project_Request_Data\Endometrial Cancer.xlsx"
SHEET_NAME = "Consolidation"
OUTPUT_PDF = "data/HCP_Dashboard_Report.pdf"
IMAGE_DIR = "data/images"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# =============================
# COLOR PALETTE (Power BI Style)
# =============================
COLORS = {
    'primary': '#118DFF',
    'secondary': '#12239E',
    'tertiary': '#E66C37',
    'quaternary': '#6B007B',
    'quinary': '#E044A7',
    'success': '#107C10',
    'warning': '#FFB900',
    'danger': '#D13438',
    'teal': '#00B7C3',
    'purple': '#7160E8',
    'background': '#F3F2F1',
    'card_bg': '#FFFFFF',
    'text_dark': '#252423',
    'text_light': '#605E5C'
}

CHART_COLORS = ['#118DFF', '#12239E', '#E66C37', '#6B007B', '#E044A7', 
                '#107C10', '#FFB900', '#D13438', '#00B7C3', '#7160E8',
                '#4C4A48', '#30BFBF', '#E8E8E8', '#FFCB33', '#A4373A']

# =============================
# LOAD DATA
# =============================
try:
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    df.columns = df.columns.str.strip()
    logging.info("Data loaded successfully.")
except Exception as e:
    logging.error(f"Error loading data: {e}")
    raise

# =============================
# DATA PROCESSING
# =============================
# Basic Metrics
total_hcps = len(df)
total_emails = df["Email ID"].nunique()
total_countries = df["Country"].nunique()
total_institutions = df["Affiliation/Institution"].nunique()

# Grouped Data
country_counts = df["Country"].value_counts()
specialty_counts = df["Specialty"].value_counts()
therapy_counts = df["TherapyArea"].value_counts()
top_institutions = df["Affiliation/Institution"].value_counts().head(10)

# Timeline Data (if Date column exists)
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')
    df["Year"] = df["Date"].dt.year
    yearly_counts = df.groupby("Year").size()
    yearly_counts = yearly_counts[yearly_counts.index.notna()]  # Remove NaN years
else:
    yearly_counts = pd.Series()

# Country-Specialty Cross-tabulation
country_specialty = pd.crosstab(df["Country"], df["Specialty"])

# =============================
# CHART STYLING FUNCTIONS
# =============================
def style_axis(ax, title="", xlabel="", ylabel="", grid=True):
    """Apply consistent styling to axes"""
    ax.set_title(title, fontsize=11, fontweight='bold', color=COLORS['text_dark'], pad=8)
    ax.set_xlabel(xlabel, fontsize=8, color=COLORS['text_light'])
    ax.set_ylabel(ylabel, fontsize=8, color=COLORS['text_light'])
    ax.tick_params(axis='both', labelsize=7, colors=COLORS['text_light'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E0E0E0')
    ax.spines['bottom'].set_color('#E0E0E0')
    if grid:
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='#CCCCCC')
    ax.set_facecolor(COLORS['card_bg'])

# =============================
# DASHBOARD PAGE 1: OVERVIEW
# =============================
def create_overview_dashboard():
    """Create main overview dashboard"""
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor(COLORS['background'])
    
    # Title
    fig.suptitle('Healthcare Professionals (HCP) Data Dashboard', 
                 fontsize=18, fontweight='bold', color=COLORS['text_dark'], y=0.98)
    
    gs = GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.35, 
                  left=0.06, right=0.94, top=0.90, bottom=0.08)
    
    # ===== ROW 1: KPI Cards =====
    # KPI 1: Total HCPs
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['card_bg'])
    ax1.text(0.5, 0.65, f"{total_hcps:,}", ha='center', va='center', 
             fontsize=28, fontweight='bold', color=COLORS['primary'], transform=ax1.transAxes)
    ax1.text(0.5, 0.25, "Total HCPs", ha='center', va='center', 
             fontsize=10, color=COLORS['text_light'], transform=ax1.transAxes)
    ax1.axis('off')
    for spine in ax1.spines.values():
        spine.set_visible(True)
        spine.set_color('#E0E0E0')
    
    # KPI 2: Unique Emails
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['card_bg'])
    ax2.text(0.5, 0.65, f"{total_emails:,}", ha='center', va='center', 
             fontsize=28, fontweight='bold', color=COLORS['success'], transform=ax2.transAxes)
    ax2.text(0.5, 0.25, "Unique Emails", ha='center', va='center', 
             fontsize=10, color=COLORS['text_light'], transform=ax2.transAxes)
    ax2.axis('off')
    for spine in ax2.spines.values():
        spine.set_visible(True)
        spine.set_color('#E0E0E0')
    
    # KPI 3: Countries
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(COLORS['card_bg'])
    ax3.text(0.5, 0.65, f"{total_countries:,}", ha='center', va='center', 
             fontsize=28, fontweight='bold', color=COLORS['tertiary'], transform=ax3.transAxes)
    ax3.text(0.5, 0.25, "Countries", ha='center', va='center', 
             fontsize=10, color=COLORS['text_light'], transform=ax3.transAxes)
    ax3.axis('off')
    for spine in ax3.spines.values():
        spine.set_visible(True)
        spine.set_color('#E0E0E0')
    
    # KPI 4: Institutions
    ax4 = fig.add_subplot(gs[0, 3])
    ax4.set_facecolor(COLORS['card_bg'])
    ax4.text(0.5, 0.65, f"{total_institutions:,}", ha='center', va='center', 
             fontsize=28, fontweight='bold', color=COLORS['quaternary'], transform=ax4.transAxes)
    ax4.text(0.5, 0.25, "Institutions", ha='center', va='center', 
             fontsize=10, color=COLORS['text_light'], transform=ax4.transAxes)
    ax4.axis('off')
    for spine in ax4.spines.values():
        spine.set_visible(True)
        spine.set_color('#E0E0E0')
    
    # ===== ROW 2: Charts =====
    # Country Distribution (Horizontal Bar)
    ax5 = fig.add_subplot(gs[1, 0:2])
    ax5.set_facecolor(COLORS['card_bg'])
    top_countries = country_counts.head(8)
    bars = ax5.barh(range(len(top_countries)), top_countries.values, color=COLORS['primary'])
    ax5.set_yticks(range(len(top_countries)))
    ax5.set_yticklabels(top_countries.index, fontsize=8)
    ax5.invert_yaxis()
    style_axis(ax5, title="HCPs by Country (Top 8)", xlabel="Count", grid=True)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, top_countries.values)):
        ax5.text(val + 0.3, i, str(val), va='center', fontsize=7, color=COLORS['text_dark'])
    
    # Specialty Distribution (Donut Chart)
    ax6 = fig.add_subplot(gs[1, 2:4])
    ax6.set_facecolor(COLORS['card_bg'])
    specialty_top = specialty_counts.head(6).copy()
    if len(specialty_counts) > 6:
        specialty_top['Others'] = specialty_counts[6:].sum()
    
    wedges, texts, autotexts = ax6.pie(specialty_top.values, 
                                        labels=None,
                                        autopct='%1.1f%%',
                                        colors=CHART_COLORS[:len(specialty_top)],
                                        wedgeprops=dict(width=0.6, edgecolor='white'),
                                        pctdistance=0.75,
                                        textprops={'fontsize': 8})
    
    ax6.legend(wedges, specialty_top.index, title="Specialty", loc="center left", 
               bbox_to_anchor=(0.95, 0.5), fontsize=7, title_fontsize=8)
    ax6.set_title("Specialty Distribution", fontsize=11, fontweight='bold', 
                  color=COLORS['text_dark'], pad=8)
    
    # Center text for donut
    ax6.text(0, 0, f"{len(specialty_counts)}\nSpecialties", ha='center', va='center', 
             fontsize=9, fontweight='bold', color=COLORS['text_dark'])
    
    # ===== ROW 3: More Charts =====
    # Top Institutions (Horizontal Bar)
    ax7 = fig.add_subplot(gs[2, 0:2])
    ax7.set_facecolor(COLORS['card_bg'])
    institutions_display = top_institutions.head(8)
    
    # Truncate long institution names
    inst_names = [name[:30] + '...' if len(str(name)) > 30 else str(name) 
                  for name in institutions_display.index]
    
    bars = ax7.barh(range(len(institutions_display)), institutions_display.values, 
                    color=COLORS['teal'])
    ax7.set_yticks(range(len(institutions_display)))
    ax7.set_yticklabels(inst_names, fontsize=7)
    ax7.invert_yaxis()
    style_axis(ax7, title="Top Institutions", xlabel="Count", grid=True)
    
    for i, (bar, val) in enumerate(zip(bars, institutions_display.values)):
        ax7.text(val + 0.1, i, str(val), va='center', fontsize=7, color=COLORS['text_dark'])
    
    # Therapy Area Distribution (Bar Chart)
    ax8 = fig.add_subplot(gs[2, 2:4])
    ax8.set_facecolor(COLORS['card_bg'])
    therapy_top = therapy_counts.head(6)
    bars = ax8.bar(range(len(therapy_top)), therapy_top.values, color=CHART_COLORS[:len(therapy_top)])
    ax8.set_xticks(range(len(therapy_top)))
    ax8.set_xticklabels([str(x)[:12] for x in therapy_top.index], rotation=45, ha='right', fontsize=7)
    style_axis(ax8, title="Therapy Area Distribution", ylabel="Count", grid=True)
    
    for bar, val in zip(bars, therapy_top.values):
        ax8.text(bar.get_x() + bar.get_width()/2, val + 0.3, str(val), 
                 ha='center', fontsize=7, color=COLORS['text_dark'])
    
    path = os.path.join(IMAGE_DIR, "dashboard_overview.png")
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    logging.info("Overview dashboard created.")
    return path

# =============================
# DASHBOARD PAGE 2: DETAILED ANALYSIS
# =============================
def create_detailed_dashboard():
    """Create detailed analysis dashboard"""
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor(COLORS['background'])
    
    fig.suptitle('Detailed Analysis Dashboard', 
                 fontsize=18, fontweight='bold', color=COLORS['text_dark'], y=0.98)
    
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3,
                  left=0.06, right=0.94, top=0.90, bottom=0.10)
    
    # ===== Country-Specialty Stacked Bar =====
    ax1 = fig.add_subplot(gs[0, 0:2])
    ax1.set_facecolor(COLORS['card_bg'])
    
    top_5_countries = country_counts.head(5).index
    cs_data = country_specialty.loc[top_5_countries].T
    cs_data = cs_data.loc[cs_data.sum(axis=1) > 0]
    
    bottom = np.zeros(len(top_5_countries))
    for i, (specialty, values) in enumerate(cs_data.iterrows()):
        ax1.bar(range(len(top_5_countries)), values.values, bottom=bottom, 
                label=str(specialty)[:18], color=CHART_COLORS[i % len(CHART_COLORS)])
        bottom += values.values
    
    ax1.set_xticks(range(len(top_5_countries)))
    ax1.set_xticklabels(top_5_countries, rotation=45, ha='right', fontsize=8)
    ax1.legend(title="Specialty", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=6, title_fontsize=7)
    style_axis(ax1, title="Country vs Specialty Distribution", ylabel="Count", grid=True)
    
    # ===== Country Pie Chart =====
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.set_facecolor(COLORS['card_bg'])
    
    country_top = country_counts.head(5).copy()
    if len(country_counts) > 5:
        others_count = country_counts[5:].sum()
        country_top['Others'] = others_count
    
    wedges, texts, autotexts = ax2.pie(country_top.values,
                                        labels=None,
                                        autopct='%1.1f%%',
                                        colors=CHART_COLORS[:len(country_top)],
                                        wedgeprops=dict(edgecolor='white', linewidth=1),
                                        pctdistance=0.8,
                                        textprops={'fontsize': 8})
    
    ax2.legend(wedges, country_top.index, title="Country", loc="center left",
               bbox_to_anchor=(0.85, 0.5), fontsize=7, title_fontsize=8)
    ax2.set_title("Country Distribution", fontsize=11, fontweight='bold',
                  color=COLORS['text_dark'], pad=8)
    
    # ===== Timeline Chart (if available) =====
    ax3 = fig.add_subplot(gs[1, 0:2])
    ax3.set_facecolor(COLORS['card_bg'])
    
    if len(yearly_counts) > 0:
        years = yearly_counts.index.astype(int)
        counts = yearly_counts.values
        
        ax3.fill_between(years, counts, alpha=0.3, color=COLORS['primary'])
        ax3.plot(years, counts, marker='o', linewidth=2, color=COLORS['primary'], 
                 markersize=6, markerfacecolor='white', markeredgewidth=2)
        
        for x, y in zip(years, counts):
            ax3.annotate(str(y), (x, y), textcoords="offset points", 
                        xytext=(0, 8), ha='center', fontsize=7, color=COLORS['text_dark'])
        
        style_axis(ax3, title="Publications Over Time", xlabel="Year", ylabel="Count", grid=True)
    else:
        ax3.text(0.5, 0.5, "Timeline data not available", ha='center', va='center',
                 fontsize=11, color=COLORS['text_light'], transform=ax3.transAxes)
        ax3.set_facecolor(COLORS['card_bg'])
        ax3.axis('off')
    
    # ===== Email Coverage Gauge =====
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.set_facecolor(COLORS['card_bg'])
    
    email_coverage = (total_emails / total_hcps) * 100 if total_hcps > 0 else 0
    
    # Create gauge chart
    theta = np.linspace(0, np.pi, 100)
    
    # Background arc (gray)
    ax4.plot(np.cos(theta), np.sin(theta), color='#E0E0E0', linewidth=15, solid_capstyle='round')
    
    # Foreground arc (colored based on percentage)
    theta_filled = np.linspace(0, np.pi * (email_coverage / 100), 100)
    color = COLORS['success'] if email_coverage >= 70 else (COLORS['warning'] if email_coverage >= 40 else COLORS['danger'])
    ax4.plot(np.cos(theta_filled), np.sin(theta_filled), color=color, linewidth=15, solid_capstyle='round')
    
    # Center text
    ax4.text(0, 0.2, f"{email_coverage:.1f}%", ha='center', va='center',
             fontsize=20, fontweight='bold', color=COLORS['text_dark'])
    ax4.text(0, -0.1, "Email Coverage", ha='center', va='center',
             fontsize=9, color=COLORS['text_light'])
    
    ax4.set_xlim(-1.5, 1.5)
    ax4.set_ylim(-0.5, 1.5)
    ax4.axis('off')
    ax4.set_title("Data Quality Indicator", fontsize=11, fontweight='bold',
                  color=COLORS['text_dark'], pad=8)
    
    path = os.path.join(IMAGE_DIR, "dashboard_detailed.png")
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    logging.info("Detailed dashboard created.")
    return path

# =============================
# DASHBOARD PAGE 3: DATA TABLES
# =============================
def create_summary_tables():
    """Create summary statistics dashboard"""
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor(COLORS['background'])
    
    fig.suptitle('Summary Statistics & Data Tables', 
                 fontsize=18, fontweight='bold', color=COLORS['text_dark'], y=0.98)
    
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25,
                  left=0.06, right=0.94, top=0.90, bottom=0.08)
    
    # ===== Country Summary Table =====
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(COLORS['card_bg'])
    ax1.axis('off')
    
    country_table_data = [["Country", "HCP Count", "% Share"]]
    for country, count in country_counts.head(10).items():
        pct = (count / total_hcps) * 100
        country_table_data.append([str(country)[:20], str(count), f"{pct:.1f}%"])
    
    table1 = ax1.table(cellText=country_table_data, loc='center', cellLoc='center',
                       colWidths=[0.5, 0.25, 0.25])
    table1.auto_set_font_size(False)
    table1.set_fontsize(8)
    table1.scale(1, 1.6)
    
    # Style header row
    for i in range(3):
        table1[(0, i)].set_facecolor(COLORS['primary'])
        table1[(0, i)].set_text_props(color='white', fontweight='bold')
    
    # Alternate row colors
    for i in range(1, len(country_table_data)):
        for j in range(3):
            if i % 2 == 0:
                table1[(i, j)].set_facecolor('#F5F5F5')
            else:
                table1[(i, j)].set_facecolor('white')
    
    ax1.set_title("Top 10 Countries by HCP Count", fontsize=11, fontweight='bold',
                  color=COLORS['text_dark'], pad=15)
    
    # ===== Specialty Summary Table =====
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(COLORS['card_bg'])
    ax2.axis('off')
    
    specialty_table_data = [["Specialty", "HCP Count", "% Share"]]
    for specialty, count in specialty_counts.head(10).items():
        pct = (count / total_hcps) * 100
        specialty_name = str(specialty)[:20] + '...' if len(str(specialty)) > 20 else str(specialty)
        specialty_table_data.append([specialty_name, str(count), f"{pct:.1f}%"])
    
    table2 = ax2.table(cellText=specialty_table_data, loc='center', cellLoc='center',
                       colWidths=[0.5, 0.25, 0.25])
    table2.auto_set_font_size(False)
    table2.set_fontsize(8)
    table2.scale(1, 1.6)
    
    for i in range(3):
        table2[(0, i)].set_facecolor(COLORS['tertiary'])
        table2[(0, i)].set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(specialty_table_data)):
        for j in range(3):
            if i % 2 == 0:
                table2[(i, j)].set_facecolor('#F5F5F5')
            else:
                table2[(i, j)].set_facecolor('white')
    
    ax2.set_title("Top 10 Specialties by HCP Count", fontsize=11, fontweight='bold',
                  color=COLORS['text_dark'], pad=15)
    
    # ===== Institution Summary Table =====
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(COLORS['card_bg'])
    ax3.axis('off')
    
    institution_table_data = [["Institution", "HCP Count"]]
    for inst, count in top_institutions.head(10).items():
        inst_name = str(inst)[:35] + '...' if len(str(inst)) > 35 else str(inst)
        institution_table_data.append([inst_name, str(count)])
    
    table3 = ax3.table(cellText=institution_table_data, loc='center', cellLoc='center',
                       colWidths=[0.7, 0.3])
    table3.auto_set_font_size(False)
    table3.set_fontsize(8)
    table3.scale(1, 1.6)
    
    for i in range(2):
        table3[(0, i)].set_facecolor(COLORS['teal'])
        table3[(0, i)].set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(institution_table_data)):
        for j in range(2):
            if i % 2 == 0:
                table3[(i, j)].set_facecolor('#F5F5F5')
            else:
                table3[(i, j)].set_facecolor('white')
    
    ax3.set_title("Top 10 Institutions by HCP Count", fontsize=11, fontweight='bold',
                  color=COLORS['text_dark'], pad=15)
    
    # ===== Key Metrics Summary =====
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(COLORS['card_bg'])
    ax4.axis('off')
    
    avg_hcp_country = total_hcps / total_countries if total_countries > 0 else 0
    avg_hcp_inst = total_hcps / total_institutions if total_institutions > 0 else 0
    email_cov = (total_emails / total_hcps * 100) if total_hcps > 0 else 0
    
    metrics_data = [
        ["Metric", "Value"],
        ["Total HCPs", f"{total_hcps:,}"],
        ["Unique Emails", f"{total_emails:,}"],
        ["Countries", f"{total_countries:,}"],
        ["Institutions", f"{total_institutions:,}"],
        ["Specialties", f"{len(specialty_counts):,}"],
        ["Therapy Areas", f"{len(therapy_counts):,}"],
        ["Email Coverage", f"{email_cov:.1f}%"],
        ["Avg HCPs/Country", f"{avg_hcp_country:.1f}"],
        ["Avg HCPs/Institution", f"{avg_hcp_inst:.2f}"]
    ]
    
    table4 = ax4.table(cellText=metrics_data, loc='center', cellLoc='center',
                       colWidths=[0.6, 0.4])
    table4.auto_set_font_size(False)
    table4.set_fontsize(8)
    table4.scale(1, 1.6)
    
    for i in range(2):
        table4[(0, i)].set_facecolor(COLORS['quaternary'])
        table4[(0, i)].set_text_props(color='white', fontweight='bold')
    
    for i in range(1, len(metrics_data)):
        for j in range(2):
            if i % 2 == 0:
                table4[(i, j)].set_facecolor('#F5F5F5')
            else:
                table4[(i, j)].set_facecolor('white')
    
    ax4.set_title("Key Metrics Summary", fontsize=11, fontweight='bold',
                  color=COLORS['text_dark'], pad=15)
    
    path = os.path.join(IMAGE_DIR, "dashboard_tables.png")
    plt.savefig(path, dpi=120, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close()
    logging.info("Summary tables dashboard created.")
    return path

# =============================
# GENERATE ALL DASHBOARDS
# =============================
overview_img = create_overview_dashboard()
detailed_img = create_detailed_dashboard()
tables_img = create_summary_tables()

# =============================
# GENERATE PDF REPORT
# =============================
def generate_pdf_report():
    """Generate final PDF report with all dashboards"""
    
    # Get page dimensions
    page_width, page_height = landscape(A4)
    
    doc = SimpleDocTemplate(
        OUTPUT_PDF, 
        pagesize=landscape(A4),
        leftMargin=0.3*inch, 
        rightMargin=0.3*inch,
        topMargin=0.3*inch, 
        bottomMargin=0.3*inch
    )
    
    # Calculate available dimensions
    available_width = page_width - 0.6*inch
    available_height = page_height - 1.2*inch  # Leave space for title and margins
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor(COLORS['text_dark']),
        spaceAfter=10,
        alignment=1  # Center alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor(COLORS['text_light']),
        spaceAfter=15,
        alignment=1  # Center alignment
    )
    
    story = []
    
    # Page 1: Overview Dashboard
    story.append(Paragraph("HCP Data Analytics Report", title_style))
    story.append(Paragraph("Comprehensive Healthcare Professionals Database Analysis", subtitle_style))
    story.append(Image(overview_img, width=available_width, height=available_height))
    story.append(PageBreak())
    
    # Page 2: Detailed Analysis
    story.append(Paragraph("Detailed Analysis", title_style))
    story.append(Paragraph("In-depth insights into HCP distribution and data quality", subtitle_style))
    story.append(Image(detailed_img, width=available_width, height=available_height))
    story.append(PageBreak())
    
    # Page 3: Summary Tables
    story.append(Paragraph("Summary Statistics", title_style))
    story.append(Paragraph("Tabular representation of key metrics and distributions", subtitle_style))
    story.append(Image(tables_img, width=available_width, height=available_height))
    
    doc.build(story)
    logging.info(f"PDF report generated: {OUTPUT_PDF}")

generate_pdf_report()

print(f"\n{'='*60}")
print("REPORT GENERATION COMPLETE!")
print(f"{'='*60}")
print(f"Output PDF: {OUTPUT_PDF}")
print(f"Images saved to: {IMAGE_DIR}")
print(f"\nKey Metrics:")
print(f"  - Total HCPs: {total_hcps:,}")
print(f"  - Unique Emails: {total_emails:,}")
print(f"  - Countries: {total_countries:,}")
print(f"  - Institutions: {total_institutions:,}")
print(f"{'='*60}")