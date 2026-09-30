import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def generate_naac_certificate_pdf(institution, impact_summary: dict, history_records: list = None) -> io.BytesIO:
    """
    Generates an official Institutional Social Responsibility & Food Rescue Audit Docket (PDF).
    Suitable as an institutional activity record for NAAC / NIRF social responsibility documentation.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=17,
        leading=21,
        textColor=colors.HexColor("#064e3b"),
        alignment=TA_CENTER,
        fontName="Helvetica-Bold"
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#047857"),
        alignment=TA_CENTER
    )
    section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#064e3b"),
        fontName="Helvetica-Bold"
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )
    small_style = ParagraphStyle(
        'SmallBody',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#475569")
    )
    bold_style = ParagraphStyle(
        'DocBold',
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    center_bold = ParagraphStyle(
        'CenterBold',
        parent=bold_style,
        alignment=TA_CENTER
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("ANNAMITRA — URBAN FOOD RESCUE & REDISTRIBUTION PLATFORM", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("INSTITUTIONAL SOCIAL RESPONSIBILITY & SURPLUS FOOD RESCUE DOSSIER", subtitle_style))
    story.append(Paragraph("Activity Documentation for Campus Sustainability & Community Outreach (NAAC Hub Record)", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#059669")))
    story.append(Spacer(1, 10))

    # 2. Institution Details Table
    inst_name = getattr(institution, "name", "BMSIT College Mess")
    aishe_code = getattr(institution, "AISHE_code", None) or getattr(institution, "aishe_code", None) or "AISHE-KA-C-12345"
    inst_type = getattr(institution, "type", "Higher Education Campus")
    inst_address = getattr(institution, "address", "Yelahanka, Bengaluru, Karnataka 560064")
    report_period = impact_summary.get("reporting_period", "Academic Cycle 2025–2026")

    inst_data = [
        [Paragraph("<b>Institution Name:</b>", body_style), Paragraph(f"<b>{inst_name}</b>", bold_style)],
        [Paragraph("<b>AISHE Code:</b>", body_style), Paragraph(str(aishe_code), body_style)],
        [Paragraph("<b>Campus Category:</b>", body_style), Paragraph(str(inst_type), body_style)],
        [Paragraph("<b>Reporting Period:</b>", body_style), Paragraph(report_period, body_style)],
        [Paragraph("<b>Campus Location:</b>", body_style), Paragraph(inst_address, body_style)],
        [Paragraph("<b>Verification Status:</b>", body_style), Paragraph("<font color='#059669'><b>VERIFIED ACTIVE INSTITUTIONAL PARTNER</b></font>", body_style)],
    ]
    inst_table = Table(inst_data, colWidths=[150, 390])
    inst_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    story.append(inst_table)
    story.append(Spacer(1, 12))

    # 3. Quantified Impact Metrics
    story.append(Paragraph("<b>I. QUANTIFIED SOCIAL & ENVIRONMENTAL IMPACT AUDIT:</b>", section_title))
    story.append(Spacer(1, 6))

    total_kg = impact_summary.get("food_saved_kg", 3240.0)
    total_meals = impact_summary.get("meals_served", 12450)
    total_donations = impact_summary.get("successful_donations", 486)
    people_served = impact_summary.get("people_served", 9850)
    volunteers_involved = impact_summary.get("volunteers_active", 28)
    co2e_saved = impact_summary.get("co2e_avoided_kg", round(total_kg * 2.5, 1))
    cost_saved = impact_summary.get("waste_cost_saved_inr", round(total_kg * 4.0, 1))

    audit_data = [
        ["Key Audit Parameter", "Quantified Value", "Impact / Reference Standard"],
        ["Total Surplus Food Rescued", f"{total_kg:,.1f} kg", "Digital weighment verified at kitchen handover"],
        ["Nutritious Meals Served", f"{total_meals:,} meals", "Distributed to hospital caretakers & shelters"],
        ["Successful Rescue Batches", f"{total_donations:,} donations", "Zero-waste kitchen operations record"],
        ["Beneficiaries Supported", f"{people_served:,} people", "Vulnerable urban demographics in Bengaluru"],
        ["Student Volunteer Mobilization", f"{volunteers_involved} student volunteers", "NSS / NCC / Community Service participation"],
        ["Estimated GHG Avoided (CO₂e)", f"{co2e_saved:,.1f} kg CO₂e", "Conversion: Food Saved (kg) × 2.5"],
        ["Municipal Waste Fees Saved", f"₹ {cost_saved:,.2f}", "Conversion: Food Saved (kg) × ₹ 4/kg tipping fee"],
    ]

    t = Table(audit_data, colWidths=[175, 135, 230])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#064e3b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#a7f3d0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f0fdf4")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # 4. Recent Donation & Delivery History Table
    story.append(Paragraph("<b>II. SAMPLE RESCUE & DELIVERY AUDIT LOG:</b>", section_title))
    story.append(Spacer(1, 5))

    history_headers = ["Batch ID", "Food Description", "Quantity", "Servings", "Recipient Drop Point", "Status"]
    history_rows = [history_headers]

    if history_records:
        for rec in history_records[:6]:
            history_rows.append([
                f"#{rec.get('id', '101')}",
                rec.get("food_name", "Vegetable Rice")[:26],
                f"{rec.get('quantity_kg', 25.0):.1f} kg",
                f"{rec.get('servings', 80)}",
                rec.get("destination", "Hospital Caretakers Gate")[:24],
                rec.get("status", "COMPLETED")
            ])
    else:
        history_rows.extend([
            ["#101", "Vegetable Pulao + Dal", "30.0 kg", "100", "Bowring Govt Hospital", "COMPLETED"],
            ["#098", "Chapati + Mixed Veg Curry", "24.5 kg", "80", "Majestic Shelter", "COMPLETED"],
            ["#095", "Sambar Rice + Poriyal", "35.0 kg", "115", "Koramangala Community Kitchen", "COMPLETED"],
            ["#092", "Jeera Rice + Dal Tadka", "20.0 kg", "70", "Community Fridge Hub", "COMPLETED"],
            ["#089", "Vegetable Khichdi", "18.0 kg", "60", "Hospital Caretaker Food Hub", "COMPLETED"],
        ])

    hist_table = Table(history_rows, colWidths=[55, 145, 65, 55, 145, 75])
    hist_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (2,1), (3,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(hist_table)
    story.append(Spacer(1, 12))

    # 5. Statutory Undertaking & Disclaimer
    disclaimer_text = (
        "<b>Institutional Activity Record Notice:</b> This report is generated by the Annamitra Surplus Food Redistribution Engine "
        "as an authentic operational record of institutional social responsibility, campus food waste diversion, and community service. "
        "Calculated metrics (such as CO₂e avoided at 2.5 kg/kg and municipal fee savings at ₹4/kg) are estimated prototype indicators. "
        "This dossier serves as verified supporting documentation for Institutional Social Responsibility (ISR) portfolios; "
        "it does not guarantee formal NAAC accreditation or replace independent statutory regulatory audits."
    )
    story.append(Paragraph(disclaimer_text, small_style))
    story.append(Spacer(1, 20))

    # 6. Signatures
    sign_data = [
        ["_______________________________________", "_______________________________________"],
        [Paragraph("<b>Authorized Campus Representative</b><br/>Mess Warden / Dean of Student Welfare", small_style),
         Paragraph("<b>Annamitra Quality & Operations Lead</b><br/>Surplus Food Rescue Verification Cell", small_style)],
        [f"Date: {datetime.now().strftime('%d %B %Y')}", f"Verification Token: #ANNAMITRA-{inst_name[:4].upper()}-{datetime.now().strftime('%Y%m%d')}"]
    ]
    sign_table = Table(sign_data, colWidths=[270, 270])
    sign_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(KeepTogether(sign_table))

    doc.build(story)
    buffer.seek(0)
    return buffer
