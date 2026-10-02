import re


# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def normalize_text(text):
    """
    Normalize text so that comparisons are more reliable.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# --------------------------------------------------
# TOKENIZATION
# --------------------------------------------------

def get_keywords(text):
    """
    Extract meaningful keywords from a piece of text.
    """

    text = normalize_text(text)

    words = re.findall(
        r"[a-zA-Z0-9₹$%]+",
        text
    )

    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "for",
        "on",
        "with",
        "by",
        "is",
        "are",
        "be",
        "shall",
        "must",
        "should",
        "required",
        "bidder",
        "bidder's",
        "company",
        "provide",
        "submit",
        "submitted",
        "document",
        "documents"
    }

    return {
        word
        for word in words
        if len(word) > 2
        and word not in stop_words
    }


# --------------------------------------------------
# NUMBER EXTRACTION
# --------------------------------------------------

def extract_numbers(text):
    """
    Extract numbers and simple monetary values.

    Examples:

    5 crore
    10 lakh
    ₹5,00,000
    5000000
    5 years
    3 projects
    """

    if not text:
        return []

    text = normalize_text(text)

    patterns = [
        r"₹\s?[\d,]+(?:\.\d+)?",
        r"\$[\d,]+(?:\.\d+)?",
        r"\b\d+(?:,\d+)*(?:\.\d+)?\s*(?:crore|lakh|million|billion|thousand|years?|months?|projects?|%)?",
        r"\b\d+(?:\.\d+)?%",
    ]

    numbers = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:

            match = match.strip()

            if match and match not in numbers:
                numbers.append(match)

    return numbers


# --------------------------------------------------
# KEYWORD SIMILARITY
# --------------------------------------------------

def calculate_keyword_similarity(
    requirement_text,
    evidence_text
):
    """
    Calculate a simple keyword-overlap score.
    """

    requirement_keywords = get_keywords(
        requirement_text
    )

    evidence_keywords = get_keywords(
        evidence_text
    )

    if not requirement_keywords:
        return 0.0

    matching_keywords = (
        requirement_keywords
        .intersection(evidence_keywords)
    )

    score = (
        len(matching_keywords)
        /
        len(requirement_keywords)
    )

    return round(
        score,
        2
    )


# --------------------------------------------------
# NUMBER MATCH
# --------------------------------------------------

def numbers_match(
    requirement_text,
    evidence_text
):
    """
    Check whether important numeric values from
    the requirement appear in bidder evidence.
    """

    requirement_numbers = extract_numbers(
        requirement_text
    )

    evidence_numbers = extract_numbers(
        evidence_text
    )

    if not requirement_numbers:
        return True

    if not evidence_numbers:
        return False

    normalized_evidence = [
        normalize_text(number)
        for number in evidence_numbers
    ]

    matched = 0

    for number in requirement_numbers:

        normalized_number = normalize_text(
            number
        )

        if normalized_number in normalized_evidence:
            matched += 1

    return matched > 0


# --------------------------------------------------
# FIND BEST EVIDENCE
# --------------------------------------------------

def find_best_evidence(
    requirement,
    bidder_pages
):
    """
    Find the bidder-document page that has the
    strongest textual similarity to a requirement.
    """

    requirement_text = requirement.get(
        "requirement",
        ""
    )

    best_page = None
    best_text = ""
    best_score = 0.0

    for page in bidder_pages:

        page_number = page.get(
            "page"
        )

        page_text = page.get(
            "text",
            ""
        )

        if not page_text.strip():
            continue

        # Compare against individual chunks so a long
        # PDF page does not dilute the matching score.
        chunks = re.split(
            r"(?<=[.!?])\s+|\n+",
            page_text
        )

        for chunk in chunks:

            chunk = chunk.strip()

            if len(chunk) < 10:
                continue

            score = calculate_keyword_similarity(
                requirement_text,
                chunk
            )

            if score > best_score:

                best_score = score

                best_page = page_number

                best_text = chunk

    return {
        "page": best_page,
        "evidence": best_text,
        "score": best_score
    }


# --------------------------------------------------
# STATUS DETERMINATION
# --------------------------------------------------

def determine_status(
    requirement,
    evidence
):
    """
    Determine whether a requirement is:

    Satisfied
    Review
    Missing
    """

    score = evidence.get(
        "score",
        0.0
    )

    evidence_text = evidence.get(
        "evidence",
        ""
    )

    requirement_text = requirement.get(
        "requirement",
        ""
    )

    mandatory = requirement.get(
        "mandatory",
        False
    )

    if not evidence_text:

        return {
            "status": "Missing",
            "reason": (
                "No matching evidence was "
                "found in the bidder documents."
            ),
            "confidence": "High"
        }

    numeric_match = numbers_match(
        requirement_text,
        evidence_text
    )

    # --------------------------------------------------
    # STRONG MATCH
    # --------------------------------------------------

    if score >= 0.65 and numeric_match:

        return {
            "status": "Satisfied",
            "reason": (
                "Bidder evidence strongly matches "
                "the tender requirement."
            ),
            "confidence": "High"
        }

    # --------------------------------------------------
    # NUMERIC CONFLICT
    # --------------------------------------------------

    if score >= 0.45 and not numeric_match:

        return {
            "status": "Review",
            "reason": (
                "Related evidence was found, but "
                "important numeric information does "
                "not clearly match the requirement."
            ),
            "confidence": "Medium"
        }

    # --------------------------------------------------
    # MODERATE MATCH
    # --------------------------------------------------

    if score >= 0.40:

        return {
            "status": "Review",
            "reason": (
                "Potentially relevant evidence was "
                "found, but manual verification is "
                "recommended."
            ),
            "confidence": "Medium"
        }

    # --------------------------------------------------
    # WEAK MATCH
    # --------------------------------------------------

    if score >= 0.20:

        return {
            "status": "Review",
            "reason": (
                "Some related information was found, "
                "but it is insufficient to confirm "
                "compliance."
            ),
            "confidence": "Low"
        }

    # --------------------------------------------------
    # NO MEANINGFUL MATCH
    # --------------------------------------------------

    if mandatory:

        return {
            "status": "Missing",
            "reason": (
                "No sufficient evidence was found "
                "for this mandatory requirement."
            ),
            "confidence": "High"
        }

    return {
        "status": "Review",
        "reason": (
            "No strong evidence was found. "
            "Manual review is recommended."
        ),
        "confidence": "Low"
    }


# --------------------------------------------------
# CHECK SINGLE REQUIREMENT
# --------------------------------------------------

def check_requirement(
    requirement,
    bidder_pages
):
    """
    Check one tender requirement against bidder
    document pages.
    """

    evidence = find_best_evidence(
        requirement,
        bidder_pages
    )

    decision = determine_status(
        requirement,
        evidence
    )

    return {

        "requirement": requirement.get(
            "requirement",
            ""
        ),

        "category": requirement.get(
            "category",
            "Other"
        ),

        "mandatory": requirement.get(
            "mandatory",
            False
        ),

        "tender_page": requirement.get(
            "page"
        ),

        "status": decision["status"],

        "reason": decision["reason"],

        "confidence": decision["confidence"],

        "bidder_page": evidence.get(
            "page"
        ),

        "evidence": evidence.get(
            "evidence",
            ""
        ),

        "match_score": evidence.get(
            "score",
            0.0
        )
    }


# --------------------------------------------------
# CHECK ALL REQUIREMENTS
# --------------------------------------------------

def check_compliance(
    requirements,
    bidder_pages
):
    """
    Compare all tender requirements against
    bidder documents.

    Returns a structured compliance report.
    """

    if not requirements:

        return {
            "results": [],
            "summary": {
                "total": 0,
                "satisfied": 0,
                "review": 0,
                "missing": 0
            }
        }

    if not bidder_pages:

        results = []

        for requirement in requirements:

            results.append({

                "requirement": requirement.get(
                    "requirement",
                    ""
                ),

                "category": requirement.get(
                    "category",
                    "Other"
                ),

                "mandatory": requirement.get(
                    "mandatory",
                    False
                ),

                "tender_page": requirement.get(
                    "page"
                ),

                "status": "Missing",

                "reason": (
                    "No bidder documents were "
                    "provided for comparison."
                ),

                "confidence": "High",

                "bidder_page": None,

                "evidence": "",

                "match_score": 0.0

            })

        return {
            "results": results,
            "summary": {
                "total": len(results),
                "satisfied": 0,
                "review": 0,
                "missing": len(results)
            }
        }

    results = []

    for requirement in requirements:

        result = check_requirement(
            requirement,
            bidder_pages
        )

        results.append(
            result
        )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    satisfied = sum(
        1
        for result in results
        if result["status"] == "Satisfied"
    )

    review = sum(
        1
        for result in results
        if result["status"] == "Review"
    )

    missing = sum(
        1
        for result in results
        if result["status"] == "Missing"
    )

    summary = {

        "total": len(results),

        "satisfied": satisfied,

        "review": review,

        "missing": missing

    }

    return {

        "results": results,

        "summary": summary

    }


# --------------------------------------------------
# COMPLIANCE PERCENTAGE
# --------------------------------------------------

def calculate_compliance_percentage(
    compliance_report
):
    """
    Calculate the percentage of requirements
    currently marked as satisfied.
    """

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

    if total == 0:
        return 0

    return round(
        (satisfied / total) * 100,
        1
    )