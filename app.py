import os
import uuid

from flask import Flask, render_template, request, send_file, session

from services.document_parser import extract_text_from_pdf
from services.requirement_extractor import extract_requirements
from services.compilance_checker import check_compliance
from services.report_generator import generate_compliance_report
from database import (
    init_database,
    create_analysis,
    get_analysis,
    update_bidder_data,
    delete_analysis,
)


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "procureai-local-development-key"
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_database()


def save_uploaded_file(file):
    extension = os.path.splitext(file.filename)[1].lower()

    filename = f"{uuid.uuid4().hex}{extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(file_path)

    return file_path


def is_pdf(file):
    if not file:
        return False

    if not file.filename:
        return False

    return file.filename.lower().endswith(".pdf")


@app.route("/", methods=["GET", "POST"])
def index():

    error = None

    if request.method == "POST":

        tender_file = request.files.get("tender")

        if not tender_file or not tender_file.filename:
            error = "Please upload a tender PDF."

        elif not is_pdf(tender_file):
            error = "Only PDF files are supported."

        else:

            try:
                file_path = save_uploaded_file(tender_file)

                tender_pages = extract_text_from_pdf(
                    file_path
                )

                requirements = extract_requirements(
                    tender_pages
                )

                analysis_id = uuid.uuid4().hex

                create_analysis(
                    analysis_id=analysis_id,
                    tender_name=tender_file.filename,
                    tender_pages=tender_pages,
                    requirements=requirements
                )

                session["analysis_id"] = analysis_id

                return render_template(
                    "index.html",
                    analysis_id=analysis_id,
                    tender_name=tender_file.filename,
                    requirements=requirements,
                    compliance_report=None,
                    bidder_name=None,
                    error=None
                )

            except Exception as exc:
                error = f"Unable to process tender: {exc}"

    analysis_id = session.get("analysis_id")

    if analysis_id:

        analysis = get_analysis(analysis_id)

        if analysis:

            return render_template(
                "index.html",
                analysis_id=analysis["id"],
                tender_name=analysis["tender_name"],
                requirements=analysis["requirements"],
                compliance_report=analysis["compliance_report"],
                bidder_name=analysis["bidder_name"],
                error=error
            )

    return render_template(
        "index.html",
        analysis_id=None,
        tender_name=None,
        requirements=[],
        compliance_report=None,
        bidder_name=None,
        error=error
    )


@app.route("/upload-bidder", methods=["POST"])
def upload_bidder():

    analysis_id = session.get("analysis_id")

    if not analysis_id:

        return render_template(
            "index.html",
            analysis_id=None,
            tender_name=None,
            requirements=[],
            compliance_report=None,
            bidder_name=None,
            error="Please upload a tender before uploading bidder documents."
        )

    analysis = get_analysis(analysis_id)

    if not analysis:

        session.pop("analysis_id", None)

        return render_template(
            "index.html",
            analysis_id=None,
            tender_name=None,
            requirements=[],
            compliance_report=None,
            bidder_name=None,
            error="Analysis not found. Please upload the tender again."
        )

    bidder_files = request.files.getlist(
        "bidder_documents"
    )

    valid_files = []

    for file in bidder_files:

        if is_pdf(file):
            valid_files.append(file)

    if not valid_files:

        return render_template(
            "index.html",
            analysis_id=analysis["id"],
            tender_name=analysis["tender_name"],
            requirements=analysis["requirements"],
            compliance_report=analysis["compliance_report"],
            bidder_name=analysis["bidder_name"],
            error="Please upload at least one bidder PDF."
        )

    try:

        bidder_pages = []
        bidder_names = []

        for bidder_file in valid_files:

            file_path = save_uploaded_file(
                bidder_file
            )

            pages = extract_text_from_pdf(
                file_path
            )

            for page in pages:

                bidder_pages.append(
                    {
                        "document": bidder_file.filename,
                        "page": page["page"],
                        "text": page["text"]
                    }
                )

            bidder_names.append(
                bidder_file.filename
            )

        compliance_report = check_compliance(
            analysis["requirements"],
            bidder_pages
        )

        bidder_name = ", ".join(
            bidder_names
        )

        update_bidder_data(
            analysis_id=analysis_id,
            bidder_name=bidder_name,
            bidder_pages=bidder_pages,
            compliance_report=compliance_report
        )

        return render_template(
            "index.html",
            analysis_id=analysis["id"],
            tender_name=analysis["tender_name"],
            requirements=analysis["requirements"],
            compliance_report=compliance_report,
            bidder_name=bidder_name,
            error=None
        )

    except Exception as exc:

        return render_template(
            "index.html",
            analysis_id=analysis["id"],
            tender_name=analysis["tender_name"],
            requirements=analysis["requirements"],
            compliance_report=None,
            bidder_name=None,
            error=f"Unable to process bidder documents: {exc}"
        )


@app.route("/download-report")
def download_report():

    analysis_id = session.get("analysis_id")

    if not analysis_id:
        return "No analysis available.", 404

    analysis = get_analysis(
        analysis_id
    )

    if not analysis:
        return "Analysis not found.", 404

    if not analysis["compliance_report"]:
        return "No compliance report available.", 400

    try:

        report_path = generate_compliance_report(
            tender_name=analysis["tender_name"],
            bidder_name=analysis["bidder_name"],
            compliance_report=analysis["compliance_report"]
        )

        return send_file(
            report_path,
            as_attachment=True,
            download_name="ProcureAI_Compliance_Report.pdf"
        )

    except Exception as exc:

        return (
            f"Unable to generate report: {exc}",
            500
        )


@app.route("/reset")
def reset():

    analysis_id = session.get("analysis_id")

    if analysis_id:
        delete_analysis(analysis_id)

    session.pop(
        "analysis_id",
        None
    )

    return render_template(
        "index.html",
        analysis_id=None,
        tender_name=None,
        requirements=[],
        compliance_report=None,
        bidder_name=None,
        error=None
    )


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )