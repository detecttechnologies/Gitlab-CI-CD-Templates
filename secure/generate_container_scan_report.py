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


def truncate_description(description, max_length=300):
    """Truncate description to fit in table cell"""
    if len(description) <= max_length:
        return description
    return description[:max_length] + "..."


def styled_table(data, col_widths=None, font_size=9):
    """Return a styled table that looks nice (used in summary + details)"""
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


def generate_pdf(input_json, output_pdf):
    # Load JSON
    with open(input_json, "r") as f:
        data = json.load(f)

    vulnerabilities = data.get("vulnerabilities", [])
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]

    # Wrap long text
    wrap_style = ParagraphStyle(
        "wrap",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
    )

    # Group by package & severity
    package_issues = defaultdict(lambda: defaultdict(list))
    for vuln in vulnerabilities:
        severity = vuln.get("severity", "Unknown")
        package = vuln["location"]["dependency"]["package"]["name"]
        package_issues[severity][package].append(vuln)

    total_packages = {pkg for sev in package_issues.values() for pkg in sev.keys()}
    total_vulns = len(vulnerabilities)

    # Create PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elements = []

    # Title
    elements.append(Paragraph("Container Scanning Report", style_heading))
    elements.append(Spacer(1, 12))

    # --- SUMMARY SECTION ---
    elements.append(Paragraph("Summary", style_heading))
    elements.append(Spacer(1, 6))

    summary_data = [
        ["Metric", "Count"],
        ["Total Vulnerabilities", str(total_vulns)],
        ["Total Affected Packages", str(len(total_packages))],
    ]
    elements.append(styled_table(summary_data, col_widths=[200, 100]))
    elements.append(Spacer(1, 12))

    # Package Summary Table
    elements.append(Paragraph("Affected Packages by Severity", style_heading))
    elements.append(Spacer(1, 6))

    pkg_summary_data = [["Severity", "Package", "CVE Count"]]
    for severity, pkgs in package_issues.items():
        for pkg, vulns in pkgs.items():
            pkg_summary_data.append([severity, pkg, str(len(vulns))])

    elements.append(styled_table(pkg_summary_data, col_widths=[80, 200, 80]))
    elements.append(PageBreak())

    # --- DETAILED VULNERABILITIES ---
    elements.append(Paragraph("Detailed Vulnerabilities", style_heading))
    elements.append(Spacer(1, 12))

    rows_per_page = 15
    for page_start in range(0, total_vulns, rows_per_page):
        page_end = min(page_start + rows_per_page, total_vulns)
        page_vulns = vulnerabilities[page_start:page_end]

        table_data = [["Severity", "CVE", "Package", "Version", "Description"]]

        for vuln in page_vulns:
            severity = vuln.get("severity", "Unknown")
            identifiers = vuln.get("identifiers", [])
            cve = next((i["value"] for i in identifiers if i["type"] == "cve"), "N/A")
            package = vuln["location"]["dependency"]["package"]["name"]
            version = vuln["location"]["dependency"].get("version", "N/A")
            description = vuln.get("description", "N/A")

            truncated_desc = truncate_description(description, max_length=300)
            table_data.append([severity, cve, package, version, Paragraph(truncated_desc, wrap_style)])

        elements.append(styled_table(table_data, col_widths=[60, 90, 100, 80, 200]))

        if page_end < total_vulns:
            elements.append(PageBreak())
            elements.append(Paragraph("Detailed Vulnerabilities (continued)", style_heading))
            elements.append(Spacer(1, 12))

    doc.build(elements)


# Example usage
generate_pdf("gl-container-scanning-report.json", "container-scanning-report.pdf")
