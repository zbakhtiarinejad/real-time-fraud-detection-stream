from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(alerts_data):

    pdf = SimpleDocTemplate("fraud_summary.pdf")

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph("Fraud Detection Summary Report", styles['Title'])

    content.append(title)
    content.append(Spacer(1, 20))

    for item in alerts_data:

        text = f"""
        Card: {item['card_number']}<br/>
        Amount: ${item['amount']}<br/>
        Country: {item['country']}<br/>
        Timestamp: {item['timestamp']}<br/>
        """

        paragraph = Paragraph(text, styles['BodyText'])

        content.append(paragraph)
        content.append(Spacer(1, 12))

    pdf.build(content)

    print("PDF report generated.")