#!/usr/bin/env python3
"""
Generate sample financial documents for testing the Financial Document Q&A Assistant
"""

# import necessary libraries
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os


# Create a multi-sheet Excel file that mimics real financial reports
def generate_sample_excel():
    """Generate a comprehensive sample Excel financial document"""
    
    # Create sample data for multiple sheets
    
    # Income Statement Data
    # Quarterly revenue, expenses, and profits
    income_statement = pd.DataFrame({
        'Account': [
            'Revenue', 'Sales Revenue', 'Service Revenue', 'Other Income',
            'Total Revenue', '', 
            'Cost of Goods Sold', 'Direct Materials', 'Direct Labor', 'Manufacturing Overhead',
            'Total COGS', '',
            'Gross Profit', '',
            'Operating Expenses', 'Salaries & Wages', 'Marketing & Advertising', 
            'Rent & Utilities', 'Professional Services', 'Insurance', 'Depreciation',
            'Other Operating Expenses', 'Total Operating Expenses', '',
            'Operating Income', '',
            'Other Income/Expenses', 'Interest Income', 'Interest Expense', 
            'Other Non-Operating', 'Total Other Income/Expenses', '',
            'Income Before Taxes', 'Income Tax Expense', '',
            'Net Income'
        ],
        'Q1 2024': [
            '', 1250000, 875000, 125000,
            2250000, '',
            '', 450000, 320000, 180000,
            950000, '',
            1300000, '',
            '', 485000, 125000,
            95000, 65000, 45000, 85000,
            125000, 1025000, '',
            275000, '',
            '', 15000, -35000,
            -8000, -28000, '',
            247000, 74100, '',
            172900
        ],
        'Q2 2024': [
            '', 1380000, 920000, 95000,
            2395000, '',
            '', 485000, 345000, 195000,
            1025000, '',
            1370000, '',
            '', 510000, 145000,
            98000, 72000, 47000, 85000,
            135000, 1092000, '',
            278000, '',
            '', 18000, -38000,
            -5000, -25000, '',
            253000, 75900, '',
            177100
        ],
        'Q3 2024': [
            '', 1520000, 1050000, 180000,
            2750000, '',
            '', 565000, 395000, 225000,
            1185000, '',
            1565000, '',
            '', 545000, 165000,
            102000, 78000, 49000, 85000,
            148000, 1172000, '',
            393000, '',
            '', 22000, -42000,
            12000, -8000, '',
            385000, 115500, '',
            269500
        ]
    })
    
    # Balance Sheet Data
    # Assets, liabilities, and equity for different dates
    balance_sheet = pd.DataFrame({
        'Account': [
            'ASSETS', '',
            'Current Assets', 'Cash and Cash Equivalents', 'Accounts Receivable', 
            'Inventory', 'Prepaid Expenses', 'Other Current Assets',
            'Total Current Assets', '',
            'Non-Current Assets', 'Property, Plant & Equipment', 'Less: Accumulated Depreciation',
            'Net PPE', 'Intangible Assets', 'Investments', 'Other Non-Current Assets',
            'Total Non-Current Assets', '',
            'TOTAL ASSETS', '',
            'LIABILITIES & EQUITY', '',
            'Current Liabilities', 'Accounts Payable', 'Accrued Expenses',
            'Short-term Debt', 'Current Portion of Long-term Debt', 'Other Current Liabilities',
            'Total Current Liabilities', '',
            'Non-Current Liabilities', 'Long-term Debt', 'Deferred Tax Liabilities',
            'Other Non-Current Liabilities', 'Total Non-Current Liabilities', '',
            'Total Liabilities', '',
            'Shareholders Equity', 'Common Stock', 'Retained Earnings',
            'Other Comprehensive Income', 'Total Shareholders Equity', '',
            'TOTAL LIABILITIES & EQUITY'
        ],
        'Dec 31, 2023': [
            '', '',
            '', 485000, 320000,
            285000, 65000, 45000,
            1200000, '',
            '', 2850000, -485000,
            2365000, 125000, 285000, 95000,
            2870000, '',
            4070000, '',
            '', '',
            '', 245000, 125000,
            185000, 95000, 85000,
            735000, '',
            '', 1250000, 185000,
            125000, 1560000, '',
            2295000, '',
            '', 500000, 1185000,
            90000, 1775000, '',
            4070000
        ],
        'Mar 31, 2024': [
            '', '',
            '', 520000, 385000,
            295000, 72000, 48000,
            1320000, '',
            '', 2950000, -540000,
            2410000, 125000, 295000, 102000,
            2932000, '',
            4252000, '',
            '', '',
            '', 265000, 135000,
            195000, 98000, 92000,
            785000, '',
            '', 1285000, 195000,
            135000, 1615000, '',
            2400000, '',
            '', 500000, 1257900,
            94100, 1852000, '',
            4252000
        ],
        'Jun 30, 2024': [
            '', '',
            '', 580000, 425000,
            315000, 78000, 52000,
            1450000, '',
            '', 3050000, -595000,
            2455000, 125000, 305000, 108000,
            2993000, '',
            4443000, '',
            '', '',
            '', 285000, 145000,
            205000, 105000, 98000,
            838000, '',
            '', 1320000, 205000,
            145000, 1670000, '',
            2508000, '',
            '', 500000, 1335000,
            100000, 1935000, '',
            4443000
        ]
    })
    
    # Cash Flow Statement
    # Operating, investing, and financing cash flows
    cash_flow = pd.DataFrame({
        'Cash Flow Statement': [
            'CASH FLOWS FROM OPERATING ACTIVITIES',
            'Net Income', 'Adjustments to reconcile net income:',
            'Depreciation and Amortization', 'Changes in working capital:',
            'Accounts Receivable', 'Inventory', 'Prepaid Expenses',
            'Accounts Payable', 'Accrued Expenses', 'Other working capital changes',
            'Net Cash from Operating Activities', '',
            'CASH FLOWS FROM INVESTING ACTIVITIES',
            'Capital Expenditures', 'Investment Purchases', 'Asset Sales',
            'Other Investing Activities', 'Net Cash from Investing Activities', '',
            'CASH FLOWS FROM FINANCING ACTIVITIES',
            'Long-term Debt Proceeds', 'Long-term Debt Payments', 'Dividend Payments',
            'Share Repurchases', 'Other Financing Activities',
            'Net Cash from Financing Activities', '',
            'Net Change in Cash', 'Cash at Beginning of Period',
            'Cash at End of Period'
        ],
        'Q1 2024': [
            '',
            172900, '',
            85000, '',
            -65000, -10000, -7000,
            20000, 10000, 5000,
            210900, '',
            '',
            -185000, -20000, 15000,
            -8000, -198000, '',
            '',
            50000, -25000, -45000,
            0, -12000, -32000, '',
            -19100, 485000,
            465900
        ],
        'Q2 2024': [
            '',
            177100, '',
            85000, '',
            -40000, -20000, -6000,
            20000, 10000, 8000,
            234100, '',
            '',
            -185000, -15000, 8000,
            -5000, -197000, '',
            '',
            0, -25000, -50000,
            0, -8000, -83000, '',
            -45900, 465900,
            420000
        ],
        'Q3 2024': [
            '',
            269500, '',
            85000, '',
            -40000, -20000, -6000,
            20000, 10000, 12000,
            330500, '',
            '',
            -185000, -25000, 12000,
            -2000, -200000, '',
            '',
            0, -30000, -60000,
            0, -10000, -100000, '',
            30500, 420000,
            450500
        ]
    })
    
    # Key Metrics Summary
    # Ratios and KPIs (margins, liquidity, efficiency)
    metrics_summary = pd.DataFrame({
        'Metric': [
            'Revenue Growth (QoQ)', 'Gross Margin %', 'Operating Margin %',
            'Net Margin %', 'ROA %', 'ROE %', 'Current Ratio',
            'Quick Ratio', 'Debt-to-Equity', 'Asset Turnover',
            'Days Sales Outstanding', 'Inventory Turnover',
            'Working Capital', 'EBITDA'
        ],
        'Q1 2024': [
            'N/A', 57.8, 12.2, 7.7, 4.1, 9.3, 1.68, 1.30, 0.69, 0.53, 62.3, 3.23, 535000, 360000
        ],
        'Q2 2024': [
            6.4, 57.2, 11.6, 7.4, 4.0, 9.1, 1.73, 1.35, 0.68, 0.54, 64.8, 3.25, 612000, 363000
        ],
        'Q3 2024': [
            14.8, 56.9, 14.3, 9.8, 6.1, 13.9, 1.73, 1.36, 0.68, 0.62, 55.4, 3.47, 612000, 478000
        ]
    })
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter('sample_financial_statements.xlsx', engine='openpyxl') as writer:
        income_statement.to_excel(writer, sheet_name='Income Statement', index=False)
        balance_sheet.to_excel(writer, sheet_name='Balance Sheet', index=False)
        cash_flow.to_excel(writer, sheet_name='Cash Flow', index=False)
        metrics_summary.to_excel(writer, sheet_name='Key Metrics', index=False)
    
    print("✅ Generated sample_financial_statements.xlsx")


# Build a styled PDF income statement
def generate_sample_pdf():
    """Generate a sample PDF financial report"""
    
    # Create PDF document
    doc = SimpleDocTemplate("sample_income_statement.pdf", pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Get text styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.blue
    )
    
    # Story array to hold document content
    story = []    # content container
    
    # Title
    story.append(Paragraph("TechCorp Industries Inc.", title_style))
    story.append(Paragraph("Consolidated Income Statement", title_style))
    story.append(Paragraph("For the Nine Months Ended September 30, 2024", styles['Normal']))
    story.append(Paragraph("(Amounts in USD)", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Income Statement Data
    # Table contains quarterly + YTD figures
    data = [
        ['', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'YTD Total'],
        ['REVENUE', '', '', '', ''],
        ['Sales Revenue', '$1,250,000', '$1,380,000', '$1,520,000', '$4,150,000'],
        ['Service Revenue', '$875,000', '$920,000', '$1,050,000', '$2,845,000'],
        ['Other Income', '$125,000', '$95,000', '$180,000', '$400,000'],
        ['Total Revenue', '$2,250,000', '$2,395,000', '$2,750,000', '$7,395,000'],
        ['', '', '', '', ''],
        ['COST OF GOODS SOLD', '', '', '', ''],
        ['Direct Materials', '$450,000', '$485,000', '$565,000', '$1,500,000'],
        ['Direct Labor', '$320,000', '$345,000', '$395,000', '$1,060,000'],
        ['Manufacturing Overhead', '$180,000', '$195,000', '$225,000', '$600,000'],
        ['Total Cost of Goods Sold', '$950,000', '$1,025,000', '$1,185,000', '$3,160,000'],
        ['', '', '', '', ''],
        ['Gross Profit', '$1,300,000', '$1,370,000', '$1,565,000', '$4,235,000'],
        ['Gross Margin %', '57.8%', '57.2%', '56.9%', '57.3%'],
        ['', '', '', '', ''],
        ['OPERATING EXPENSES', '', '', '', ''],
        ['Salaries & Wages', '$485,000', '$510,000', '$545,000', '$1,540,000'],
        ['Marketing & Advertising', '$125,000', '$145,000', '$165,000', '$435,000'],
        ['Rent & Utilities', '$95,000', '$98,000', '$102,000', '$295,000'],
        ['Professional Services', '$65,000', '$72,000', '$78,000', '$215,000'],
        ['Insurance', '$45,000', '$47,000', '$49,000', '$141,000'],
        ['Depreciation', '$85,000', '$85,000', '$85,000', '$255,000'],
        ['Other Operating Expenses', '$125,000', '$135,000', '$148,000', '$408,000'],
        ['Total Operating Expenses', '$1,025,000', '$1,092,000', '$1,172,000', '$3,289,000'],
        ['', '', '', '', ''],
        ['Operating Income', '$275,000', '$278,000', '$393,000', '$946,000'],
        ['Operating Margin %', '12.2%', '11.6%', '14.3%', '12.8%'],
        ['', '', '', '', ''],
        ['OTHER INCOME (EXPENSE)', '', '', '', ''],
        ['Interest Income', '$15,000', '$18,000', '$22,000', '$55,000'],
        ['Interest Expense', '($35,000)', '($38,000)', '($42,000)', '($115,000)'],
        ['Other Non-Operating', '($8,000)', '($5,000)', '$12,000', '($1,000)'],
        ['Total Other Income (Expense)', '($28,000)', '($25,000)', '($8,000)', '($61,000)'],
        ['', '', '', '', ''],
        ['Income Before Taxes', '$247,000', '$253,000', '$385,000', '$885,000'],
        ['Income Tax Expense', '$74,100', '$75,900', '$115,500', '$265,500'],
        ['', '', '', '', ''],
        ['Net Income', '$172,900', '$177,100', '$269,500', '$619,500'],
        ['Net Margin %', '7.7%', '7.4%', '9.8%', '8.4%'],
        ['', '', '', '', ''],
        ['Shares Outstanding', '500,000', '500,000', '500,000', '500,000'],
        ['Earnings Per Share', '$0.35', '$0.35', '$0.54', '$1.24']
    ]
    
    # Create table
    table = Table(data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    
    # Table style
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        
        # Section headers (bold)
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),  # REVENUE
        ('FONTNAME', (0, 7), (0, 7), 'Helvetica-Bold'),  # COGS
        ('FONTNAME', (0, 16), (0, 16), 'Helvetica-Bold'), # OPERATING EXPENSES
        ('FONTNAME', (0, 27), (0, 27), 'Helvetica-Bold'), # OTHER INCOME
        
        # Total rows (bold)
        ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),  # Total Revenue
        ('FONTNAME', (0, 11), (-1, 11), 'Helvetica-Bold'), # Total COGS
        ('FONTNAME', (0, 13), (-1, 13), 'Helvetica-Bold'), # Gross Profit
        ('FONTNAME', (0, 24), (-1, 24), 'Helvetica-Bold'), # Total Operating Expenses
        ('FONTNAME', (0, 26), (-1, 26), 'Helvetica-Bold'), # Operating Income
        ('FONTNAME', (0, 31), (-1, 31), 'Helvetica-Bold'), # Total Other Income
        ('FONTNAME', (0, 33), (-1, 33), 'Helvetica-Bold'), # Income Before Taxes
        ('FONTNAME', (0, 36), (-1, 36), 'Helvetica-Bold'), # Net Income
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Highlight important rows
        ('BACKGROUND', (0, 5), (-1, 5), colors.lightblue),   # Total Revenue
        ('BACKGROUND', (0, 13), (-1, 13), colors.lightgreen), # Gross Profit
        ('BACKGROUND', (0, 26), (-1, 26), colors.lightyellow), # Operating Income
        ('BACKGROUND', (0, 36), (-1, 36), colors.lightcyan),   # Net Income
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Add notes section
    story.append(Paragraph("Notes:", heading_style))
    notes = [
        "1. All amounts are presented in US Dollars",
        "2. Revenue recognition follows ASC 606 guidelines",
        "3. Depreciation is calculated using straight-line method",
        "4. Income tax rate is approximately 30%",
        "5. Quarterly results are unaudited"
    ]
    
    for note in notes:
        story.append(Paragraph(note, styles['Normal']))
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 20))
    
    # Key financial highlights
    story.append(Paragraph("Key Financial Highlights (YTD):", heading_style))
    highlights = [
        "• Total Revenue increased by 22% compared to same period last year",
        "• Gross Margin maintained at healthy 57.3%",
        "• Operating Income grew by 34% year-over-year",
        "• Net Income of $619,500 represents 8.4% net margin",
        "• Strong cash generation from operations"
    ]
    
    for highlight in highlights:
        story.append(Paragraph(highlight, styles['Normal']))
        story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    print("✅ Generated sample_income_statement.pdf")


# Main Driver
# Calls both functions above, generates Excel + PDF, and prints summary
def create_sample_documents():
    """Create both sample documents and a summary"""
    print("📊 Generating Sample Financial Documents")
    print("=" * 40)
    
    try:
        generate_sample_excel()    # Excel
        generate_sample_pdf()    # PDF
        
        print("\n🎉 Sample documents created successfully!")
        print("\nFiles generated:")
        print("📊 sample_financial_statements.xlsx - Multi-sheet Excel workbook with:")
        print("   • Income Statement")
        print("   • Balance Sheet") 
        print("   • Cash Flow Statement")
        print("   • Key Metrics Summary")
        print()
        print("📄 sample_income_statement.pdf - Formatted income statement report")
        print()
        print("💡 These documents contain realistic financial data for testing")
        print("   the Financial Document Q&A Assistant application.")
        
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Install missing packages with:")
        print("pip install reportlab openpyxl")
    except Exception as e:
        print(f"❌ Error generating documents: {e}")


if __name__ == "__main__":
    create_sample_documents()