from flask import (
    Flask,
    render_template,
    request,
    send_file,
    session
)

from services.document_parser import extract_text_from_pdf
from services.requirement_extractor import extract_requirements
from services.compilance_checker import check_compliance
from services.report_generator import generate_compliance_report

import os
import uuid


# ==================================================
# APP CONFIGURATION
# ==================================================

app = Flask(__name__)

app.secret_key = "procureai-local-development-key"


UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==================================================
# IN-MEMORY ANALYSIS STORAGE
# ==================================================

analysis_store = {}


# ==================================================
# HELPER — SAVE FILE
# ==================================================

def save_uploaded_file(file):

    if not file:
        return None

    if not file.filename:
        return None

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    unique_name = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_name
    )

    file.save(
        file_path
    )

    return file_path


# ==================================================
# HELPER — VALIDATE PDF
# ==================================================

def is_pdf(file):

    if not file:
        return False

    if not file.filename:
        return False

    return (
        file.filename
        .lower()
        .endswith(".pdf")
    )


# ==================================================
# MAIN DASHBOARD
# ==================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    extracted_pages = None

    requirements = None

    compliance_report = None

    analysis_id = None

    error = None

    tender_name = None

    bidder_name = None


    # ==================================================
    # PROCESS TENDER
    # ==================================================

    if request.method == "POST":

        tender_file = request.files.get(
            "tender"
        )


        if not tender_file:

            error = (
                "Please select a tender PDF."
            )


        elif not is_pdf(
            tender_file
        ):

            error = (
                "Only PDF files are supported."
            )


        else:

            try:

                print(
                    "\n===================================="
                )

                print(
                    "PROCUREAI TENDER ANALYSIS"
                )

                print(
                    "===================================="
                )


                # ------------------------------------------
                # SAVE TENDER
                # ------------------------------------------

                tender_path = save_uploaded_file(
                    tender_file
                )

                tender_name = (
                    tender_file.filename
                )


                # ------------------------------------------
                # STEP 1 — PDF EXTRACTION
                # ------------------------------------------

                print(
                    "\n[1/3] Extracting tender text..."
                )

                extracted_pages = (
                    extract_text_from_pdf(
                        tender_path
                    )
                )


                if not extracted_pages:

                    error = (
                        "No readable text was found "
                        "in the tender PDF."
                    )

                else:

                    # --------------------------------------
                    # STEP 2 — REQUIREMENT EXTRACTION
                    # --------------------------------------

                    print(
                        "[2/3] Detecting requirements..."
                    )

                    requirements = (
                        extract_requirements(
                            extracted_pages
                        )
                    )


                    print(
                        f"Found {len(requirements)} "
                        f"requirements."
                    )


                    # --------------------------------------
                    # STEP 3 — CREATE ANALYSIS SESSION
                    # --------------------------------------

                    analysis_id = (
                        uuid.uuid4().hex
                    )


                    analysis_store[
                        analysis_id
                    ] = {

                        "tender_name":
                            tender_name,

                        "tender_pages":
                            extracted_pages,

                        "requirements":
                            requirements,

                        "bidder_name":
                            None,

                        "bidder_pages":
                            [],

                        "compliance_report":
                            None

                    }


                    session[
                        "analysis_id"
                    ] = analysis_id


                    print(
                        "\nTender analysis complete."
                    )


            except Exception as e:

                print(
                    f"\nApplication error: {e}"
                )

                error = (
                    "Something went wrong while "
                    "processing the tender."
                )


    # ==================================================
    # LOAD EXISTING ANALYSIS
    # ==================================================

    if not requirements:

        analysis_id = session.get(
            "analysis_id"
        )

        if analysis_id:

            stored_analysis = (
                analysis_store.get(
                    analysis_id
                )
            )

            if stored_analysis:

                extracted_pages = (
                    stored_analysis.get(
                        "tender_pages"
                    )
                )

                requirements = (
                    stored_analysis.get(
                        "requirements"
                    )
                )

                compliance_report = (
                    stored_analysis.get(
                        "compliance_report"
                    )
                )

                tender_name = (
                    stored_analysis.get(
                        "tender_name"
                    )
                )

                bidder_name = (
                    stored_analysis.get(
                        "bidder_name"
                    )
                )


    # ==================================================
    # RENDER DASHBOARD
    # ==================================================

    return render_template(

        "index.html",

        extracted_pages=
            extracted_pages,

        requirements=
            requirements,

        compliance_report=
            compliance_report,

        analysis_id=
            analysis_id,

        tender_name=
            tender_name,

        bidder_name=
            bidder_name,

        error=
            error

    )


# ==================================================
# BIDDER DOCUMENT UPLOAD
# ==================================================

@app.route(
    "/upload-bidder",
    methods=["POST"]
)
def upload_bidder():

    analysis_id = session.get(
        "analysis_id"
    )


    if not analysis_id:

        return render_template(
            "index.html",
            error=(
                "No tender analysis was found. "
                "Please analyze a tender first."
            )
        )


    analysis = analysis_store.get(
        analysis_id
    )


    if not analysis:

        return render_template(
            "index.html",
            error=(
                "The analysis session has expired. "
                "Please upload the tender again."
            )
        )


    bidder_files = request.files.getlist(
        "bidder_documents"
    )


    valid_files = [

        file

        for file in bidder_files

        if file
        and file.filename
        and is_pdf(file)

    ]


    if not valid_files:

        return render_template(

            "index.html",

            extracted_pages=
                analysis.get(
                    "tender_pages"
                ),

            requirements=
                analysis.get(
                    "requirements"
                ),

            compliance_report=
                analysis.get(
                    "compliance_report"
                ),

            analysis_id=
                analysis_id,

            tender_name=
                analysis.get(
                    "tender_name"
                ),

            bidder_name=
                analysis.get(
                    "bidder_name"
                ),

            error=(
                "Please upload at least "
                "one bidder PDF."
            )

        )


    try:

        print(
            "\n===================================="
        )

        print(
            "PROCUREAI BIDDER ANALYSIS"
        )

        print(
            "===================================="
        )


        bidder_pages = []


        # ------------------------------------------
        # PROCESS EACH BIDDER PDF
        # ------------------------------------------

        for file in valid_files:

            print(
                f"\nProcessing: "
                f"{file.filename}"
            )


            file_path = save_uploaded_file(
                file
            )


            pages = extract_text_from_pdf(
                file_path
            )


            if not pages:
                continue


            for page in pages:

                bidder_pages.append({

                    "page": page.get(
                        "page"
                    ),

                    "text": page.get(
                        "text",
                        ""
                    ),

                    "document":
                        file.filename

                })


        if not bidder_pages:

            raise ValueError(
                "No readable text was found "
                "in the bidder documents."
            )


        # ------------------------------------------
        # COMPLIANCE CHECK
        # ------------------------------------------

        print(
            "\nChecking bidder compliance..."
        )


        requirements = analysis.get(
            "requirements",
            []
        )


        compliance_report = (
            check_compliance(

                requirements,

                bidder_pages

            )
        )


        # ------------------------------------------
        # STORE RESULT
        # ------------------------------------------

        analysis[
            "bidder_pages"
        ] = bidder_pages


        analysis[
            "bidder_name"
        ] = "Uploaded Bidder"


        analysis[
            "compliance_report"
        ] = compliance_report


        print(
            "\nCompliance analysis complete."
        )


        print(
            compliance_report.get(
                "summary",
                {}
            )
        )


    except Exception as e:

        print(
            f"\nBidder analysis error: {e}"
        )


        return render_template(

            "index.html",

            extracted_pages=
                analysis.get(
                    "tender_pages"
                ),

            requirements=
                analysis.get(
                    "requirements"
                ),

            compliance_report=
                analysis.get(
                    "compliance_report"
                ),

            analysis_id=
                analysis_id,

            tender_name=
                analysis.get(
                    "tender_name"
                ),

            bidder_name=
                analysis.get(
                    "bidder_name"
                ),

            error=(
                "Something went wrong while "
                "processing bidder documents."
            )

        )


    return render_template(

        "index.html",

        extracted_pages=
            analysis.get(
                "tender_pages"
            ),

        requirements=
            analysis.get(
                "requirements"
            ),

        compliance_report=
            compliance_report,

        analysis_id=
            analysis_id,

        tender_name=
            analysis.get(
                "tender_name"
            ),

        bidder_name=
            analysis.get(
                "bidder_name"
            ),

        error=None

    )


# ==================================================
# DOWNLOAD REPORT
# ==================================================

@app.route(
    "/download-report"
)
def download_report():

    analysis_id = session.get(
        "analysis_id"
    )


    if not analysis_id:

        return (
            "No analysis available.",
            404
        )


    analysis = analysis_store.get(
        analysis_id
    )


    if not analysis:

        return (
            "Analysis session expired.",
            404
        )


    compliance_report = (
        analysis.get(
            "compliance_report"
        )
    )


    if not compliance_report:

        return (
            "No compliance report is available yet.",
            404
        )


    tender_name = (
        analysis.get(
            "tender_name"
        )
        or "Tender"
    )


    bidder_name = (
        analysis.get(
            "bidder_name"
        )
        or "Bidder"
    )


    try:

        pdf_buffer = (
            generate_compliance_report(

                compliance_report,

                tender_name=
                    tender_name,

                bidder_name=
                    bidder_name

            )
        )


        return send_file(

            pdf_buffer,

            mimetype="application/pdf",

            as_attachment=True,

            download_name=(
                "procureai_compliance_report.pdf"
            )

        )


    except Exception as e:

        print(
            f"Report generation error: {e}"
        )

        return (
            "Could not generate the report.",
            500
        )


# ==================================================
# RESET ANALYSIS
# ==================================================

@app.route(
    "/reset"
)
def reset():

    analysis_id = session.get(
        "analysis_id"
    )


    if analysis_id:

        analysis_store.pop(
            analysis_id,
            None
        )


    session.clear()


    return (
        render_template(
            "index.html"
        )
    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )