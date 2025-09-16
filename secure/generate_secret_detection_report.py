import json
from collections import defaultdict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def truncate_description(text: str, max_length: int = 300) -> str:
    """Truncate long text to keep row height reasonable in the PDF table."""
    if not isinstance(text, str):
        return "N/A"
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def styled_table(data, col_widths=None, font_size: int = 8) -> Table:
    """Return a consistently styled table for summary and details sections."""
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4a4a4a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f8f8")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    return table


def generate_pdf(input_json: str, output_pdf: str) -> None:
    # Load JSON
    with open(input_json, "r") as f:
        data = json.load(f)

    vulnerabilities = data.get("vulnerabilities", [])
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]

    # Paragraph style for wrapped text in table cells
    wrap_style = ParagraphStyle(
        "wrap",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
    )

    # Group by severity and file
    file_issues = defaultdict(lambda: defaultdict(list))
    for vuln in vulnerabilities:
        severity = vuln.get("severity", "Unknown")
        location = vuln.get("location", {}) or {}
        file_path = location.get("file") or location.get("path") or location.get("file_path") or "N/A"
        file_issues[severity][file_path].append(vuln)

    total_files = {f for sev in file_issues.values() for f in sev.keys()}
    total_vulns = len(vulnerabilities)

    # Create PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elements = []

    # Title
    elements.append(Paragraph("Secret Detection Report", style_heading))
    elements.append(Spacer(1, 12))

    # Summary section
    elements.append(Paragraph("Summary", style_heading))
    elements.append(Spacer(1, 6))
    summary_data = [
        ["Metric", "Count"],
        ["Total Findings", str(total_vulns)],
        ["Total Affected Files", str(len(total_files))],
    ]
    elements.append(styled_table(summary_data, col_widths=[200, 100]))
    elements.append(Spacer(1, 12))

    # Affected Files by Severity
    elements.append(Paragraph("Affected Files by Severity", style_heading))
    elements.append(Spacer(1, 6))
    files_summary_data = [["Severity", "File", "Finding Count"]]
    for severity, files in file_issues.items():
        for file_path, vulns in files.items():
            files_summary_data.append([severity, file_path, str(len(vulns))])
    elements.append(styled_table(files_summary_data, col_widths=[80, 250, 80]))

    elements.append(PageBreak())

    # Detailed findings
    elements.append(Paragraph("Detailed Findings", style_heading))
    elements.append(Spacer(1, 12))

    rows_per_page = 15
    for page_start in range(0, total_vulns, rows_per_page):
        page_end = min(page_start + rows_per_page, total_vulns)
        page_vulns = vulnerabilities[page_start:page_end]

        table_data = [["Severity", "Rule", "File", "Line", "Match"]]
        for vuln in page_vulns:
            severity = vuln.get("severity", "Unknown")
            rule_name = vuln.get("name") or (vuln.get("scanner", {}) or {}).get("name") or "N/A"
            location = vuln.get("location", {}) or {}
            file_path = location.get("file") or location.get("path") or location.get("file_path") or "N/A"
            line_num = location.get("start_line") or location.get("line") or "N/A"
            match_text = vuln.get("message") or vuln.get("description") or "N/A"

            truncated = truncate_description(match_text, max_length=300)
            table_data.append(
                [
                    severity,
                    rule_name,
                    file_path,
                    str(line_num),
                    Paragraph(truncated, wrap_style),
                ]
            )

        elements.append(
            styled_table(
                table_data,
                col_widths=[50, 85, 130, 35, 130],
            )
        )

        if page_end < total_vulns:
            elements.append(PageBreak())
            elements.append(Paragraph("Detailed Findings (continued)", style_heading))
            elements.append(Spacer(1, 12))

    doc.build(elements)


# Example usage
generate_pdf("gl-secret-detection-report.json", "secret-detection-report.pdf")
