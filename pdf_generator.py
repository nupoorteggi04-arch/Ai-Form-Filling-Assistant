"""
PDF Generator - Generates filled PDF forms from mapped form data
"""

from typing import Dict, Any
from io import BytesIO
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_filled_form_pdf(mapped_form: Dict[str, Any]) -> bytes:
    """
    Generate a filled PDF from mapped form data.
    
    Args:
        mapped_form: The mapped form dictionary from form_mapper
        
    Returns:
        bytes: PDF file as bytes
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "PDF generation requires reportlab library. Install it with: pip install reportlab"
        )
    
    # Create a BytesIO buffer to hold the PDF
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
    )
    
    # Add title
    form_name = mapped_form.get("form_name", "Government Form")
    story.append(Paragraph(f"<b>{form_name}</b>", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Add form fields
    fields = mapped_form.get("fields", {})
    
    # Prepare table data
    table_data = [["Field", "Value"]]
    
    for field_id, field_data in fields.items():
        label = field_data.get("label", field_id)
        value = field_data.get("value")
        
        # Format value for display
        if value is None or value == "":
            display_value = "<i>Not provided</i>"
        else:
            display_value = str(value)
        
        table_data.append([label, display_value])
    
    # Create table
    table = Table(table_data, colWidths=[3 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
    ]))
    
    story.append(table)
    
    # Add statistics if available
    statistics = mapped_form.get("statistics", {})
    if statistics:
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("<b>Form Completion Statistics</b>", styles['Heading2']))
        story.append(Spacer(1, 0.1 * inch))
        
        stats_text = f"""
        <b>Completion:</b> {statistics.get('completion_percentage', 0):.1f}%<br/>
        <b>Filled Fields:</b> {statistics.get('filled_fields', 0)} / {statistics.get('total_fields', 0)}<br/>
        <b>Required Fields:</b> {statistics.get('filled_required_fields', 0)} / {statistics.get('required_fields', 0)}<br/>
        """
        story.append(Paragraph(stats_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF bytes
    buffer.seek(0)
    pdf_bytes = buffer.read()
    buffer.close()
    
    return pdf_bytes





