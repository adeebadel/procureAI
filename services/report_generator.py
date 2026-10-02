import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# --------------------------------------------------
# REPORT STYLES
# --------------------------------------------------

def get_styles():

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=8
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.grey,
            spaceAfter=20
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            spaceBefore=12,
            spaceAfter=8
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["Normal"],
            fontSize=8,
            leading=11
        )
    )

    styles.add(
        ParagraphStyle(
            name="TinyText",
            parent=styles["Normal"],
            fontSize=7,
            leading=9
        )
    )

    return styles


# --------------------------------------------------
# SAFE TEXT
# --------------------------------------------------

def safe_text(value):

    if value is None:
        return "-"

    value = str(value).strip()

    if not value:
        return "-"

    return value


# --------------------------------------------------
# STATUS COLOR
# --------------------------------------------------

def status_color(status):

    if status == "Satisfied":
        return colors.HexColor("#166534")

    if status == "Missing":
        return colors.HexColor("#991B1B")

    if status == "Review":
        return colors.HexColor("#92400E")

    return colors.grey


# --------------------------------------------------
# SUMMARY TABLE
# --------------------------------------------------

def build_summary_table(
    summary,
    styles
):

    total = summary.get(
        "total",
        0
    )

    satisfied = summary.get(
        "satisfied",
        0
    )

    review = summary.get(
        "review",
        0
    )

    missing = summary.get(
        "missing",
        0
    )

    data = [

        [
            Paragraph(
                "<b>Total Requirements</b>",
                styles["SmallText"]
            ),

            Paragraph(
                "<b>Satisfied</b>",
                styles["SmallText"]
            ),

            Paragraph(
                "<b>Review</b>",
                styles["SmallText"]
            ),

            Paragraph(
                "<b>Missing</b>",
                styles["SmallText"]
            )
        ],

        [
            str(total),
            str(satisfied),
            str(review),
            str(missing)
        ]

    ]

    table = Table(
        data,
        colWidths=[
            40 * mm,
            40 * mm,
            40 * mm,
            40 * mm
        ]
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#E5E7EB")
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#D1D5DB")
            )

        ])
    )

    return table


# --------------------------------------------------
# COMPLIANCE TABLE
# --------------------------------------------------

def build_compliance_table(
    results,
    styles
):

    header = [

        Paragraph(
            "<b>#</b>",
            styles["TinyText"]
        ),

        Paragraph(
            "<b>Requirement</b>",
            styles["TinyText"]
        ),

        Paragraph(
            "<b>Category</b>",
            styles["TinyText"]
        ),

        Paragraph(
            "<b>Status</b>",
            styles["TinyText"]
        ),

        Paragraph(
            "<b>Bidder Evidence</b>",
            styles["TinyText"]
        ),

        Paragraph(
            "<b>Page</b>",
            styles["TinyText"]
        ),

        Paragraph(
            "<b>Reason</b>",
            styles["TinyText"]
        )

    ]

    data = [header]

    for index, result in enumerate(
        results,
        start=1
    ):

        status = safe_text(
            result.get(
                "status"
            )
        )

        status_style = ParagraphStyle(
            name=f"Status{index}",
            parent=styles["TinyText"],
            textColor=status_color(status),
            fontName="Helvetica-Bold"
        )

        requirement = Paragraph(
            safe_text(
                result.get(
                    "requirement"
                )
            ),
            styles["TinyText"]
        )

        category = Paragraph(
            safe_text(
                result.get(
                    "category"
                )
            ),
            styles["TinyText"]
        )

        status_paragraph = Paragraph(
            status,
            status_style
        )

        evidence = Paragraph(
            safe_text(
                result.get(
                    "evidence"
                )
            ),
            styles["TinyText"]
        )

        bidder_page = safe_text(
            result.get(
                "bidder_page"
            )
        )

        reason = Paragraph(
            safe_text(
                result.get(
                    "reason"
                )
            ),
            styles["TinyText"]
        )

        data.append([

            str(index),

            requirement,

            category,

            status_paragraph,

            evidence,

            bidder_page,

            reason

        ])

    table = Table(
        data,
        colWidths=[
            7 * mm,
            39 * mm,
            21 * mm,
            19 * mm,
            43 * mm,
            10 * mm,
            38 * mm
        ],
        repeatRows=1
    )

    table_style = [

        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#E5E7EB")
        ),

        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.35,
            colors.HexColor("#D1D5DB")
        ),

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP"
        ),

        (
            "ALIGN",
            (0, 0),
            (0, -1),
            "CENTER"
        ),

        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            7
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            5
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5
        )

    ]

    # Add subtle status backgrounds
    for row_index, result in enumerate(
        results,
        start=1
    ):

        status = result.get(
            "status"
        )

        if status == "Satisfied":

            table_style.append(
                (
                    "BACKGROUND",
                    (3, row_index),
                    (3, row_index),
                    colors.HexColor("#DCFCE7")
                )
            )

        elif status == "Review":

            table_style.append(
                (
                    "BACKGROUND",
                    (3, row_index),
                    (3, row_index),
                    colors.HexColor("#FEF3C7")
                )
            )

        elif status == "Missing":

            table_style.append(
                (
                    "BACKGROUND",
                    (3, row_index),
                    (3, row_index),
                    colors.HexColor("#FEE2E2")
                )
            )

    table.setStyle(
        TableStyle(
            table_style
        )
    )

    return table


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

def add_page_number(
    canvas,
    doc
):

    canvas.saveState()

    page_number = canvas.getPageNumber()

    canvas.setFont(
        "Helvetica",
        7
    )

    canvas.setFillColor(
        colors.grey
    )

    canvas.drawString(
        20 * mm,
        10 * mm,
        "ProcureAI — Procurement Compliance Intelligence"
    )

    canvas.drawRightString(
        190 * mm,
        10 * mm,
        f"Page {page_number}"
    )

    canvas.restoreState()


# --------------------------------------------------
# GENERATE PDF REPORT
# --------------------------------------------------

def generate_compliance_report(
    compliance_report,
    tender_name="Tender",
    bidder_name="Bidder"
):
    """
    Generate a downloadable PDF compliance report.

    Returns:
        BytesIO object containing the PDF.
    """

    if not compliance_report:

        compliance_report = {
            "results": [],
            "summary": {
                "total": 0,
                "satisfied": 0,
                "review": 0,
                "missing": 0
            }
        }

    results = compliance_report.get(
        "results",
        []
    )

    summary = compliance_report.get(
        "summary",
        {}
    )

    total = summary.get(
        "total",
        0
    )

    satisfied = summary.get(
        "satisfied",
        0
    )

    if total > 0:

        compliance_percentage = round(
            (satisfied / total) * 100,
            1
        )

    else:

        compliance_percentage = 0

    buffer = io.BytesIO()

    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=15 * mm,

        leftMargin=15 * mm,

        topMargin=15 * mm,

        bottomMargin=18 * mm

    )

    styles = get_styles()

    story = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "ProcureAI",
            styles["ReportTitle"]
        )
    )

    story.append(
        Paragraph(
            "Tender & Bid Compliance Intelligence Report",
            styles["ReportSubtitle"]
        )
    )

    # --------------------------------------------------
    # DOCUMENT INFORMATION
    # --------------------------------------------------

    generated_at = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    info_data = [

        [
            Paragraph(
                "<b>Tender</b>",
                styles["SmallText"]
            ),
            Paragraph(
                safe_text(tender_name),
                styles["SmallText"]
            )
        ],

        [
            Paragraph(
                "<b>Bidder</b>",
                styles["SmallText"]
            ),
            Paragraph(
                safe_text(bidder_name),
                styles["SmallText"]
            )
        ],

        [
            Paragraph(
                "<b>Generated</b>",
                styles["SmallText"]
            ),
            Paragraph(
                generated_at,
                styles["SmallText"]
            )
        ],

        [
            Paragraph(
                "<b>Compliance</b>",
                styles["SmallText"]
            ),
            Paragraph(
                f"{compliance_percentage}%",
                styles["SmallText"]
            )
        ]

    ]

    info_table = Table(
        info_data,
        colWidths=[
            35 * mm,
            125 * mm
        ]
    )

    info_table.setStyle(
        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D1D5DB")
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#F3F4F6")
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )

    story.append(
        info_table
    )

    story.append(
        Spacer(
            1,
            12
        )
    )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Compliance Summary",
            styles["SectionHeading"]
        )
    )

    story.append(
        build_summary_table(
            summary,
            styles
        )
    )

    story.append(
        Spacer(
            1,
            12
        )
    )

    # --------------------------------------------------
    # INTERPRETATION
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Interpretation",
            styles["SectionHeading"]
        )
    )

    interpretation = (
        f"ProcureAI identified {total} tender requirements. "
        f"{satisfied} are currently marked as satisfied, "
        f"{summary.get('review', 0)} require manual review, "
        f"and {summary.get('missing', 0)} have no sufficient "
        f"supporting evidence in the submitted bidder documents."
    )

    story.append(
        Paragraph(
            interpretation,
            styles["SmallText"]
        )
    )

    story.append(
        Spacer(
            1,
            8
        )
    )

    story.append(
        Paragraph(
            "This report is an analytical aid. Final procurement "
            "and bid evaluation decisions should be made by the "
            "authorized human review team.",
            styles["SmallText"]
        )
    )

    # --------------------------------------------------
    # REQUIREMENT DETAILS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "Requirement-Level Compliance",
            styles["SectionHeading"]
        )
    )

    if results:

        story.append(
            build_compliance_table(
                results,
                styles
            )
        )

    else:

        story.append(
            Paragraph(
                "No compliance results are available.",
                styles["SmallText"]
            )
        )

    # --------------------------------------------------
    # FINAL NOTE
    # --------------------------------------------------

    story.append(
        Spacer(
            1,
            15
        )
    )

    story.append(
        Paragraph(
            "<b>Important:</b> Evidence references in this "
            "report should be verified against the original "
            "tender and bidder documents before any official "
            "procurement decision is made.",
            styles["SmallText"]
        )
    )

    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)

    return buffer