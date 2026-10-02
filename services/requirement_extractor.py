import re


# --------------------------------------------------
# KEYWORDS USED TO IDENTIFY REQUIREMENTS
# --------------------------------------------------

REQUIREMENT_PATTERNS = {

    "Financial": [
        r"\bturnover\b",
        r"\bannual turnover\b",
        r"\baverage turnover\b",
        r"\bnet worth\b",
        r"\bfinancial capacity\b",
        r"\bfinancial capability\b",
        r"\bsolvency\b",
        r"\bprofit\b",
        r"\bfinancial statement\b",
        r"\baudited balance sheet\b",
    ],

    "Experience": [
        r"\bexperience\b",
        r"\byears of experience\b",
        r"\bprior experience\b",
        r"\bsimilar work\b",
        r"\bsimilar project\b",
        r"\bcompleted projects\b",
        r"\bwork order\b",
        r"\bcompletion certificate\b",
    ],

    "Certification": [
        r"\bISO\b",
        r"\bISO 9001\b",
        r"\bISO 14001\b",
        r"\bISO 45001\b",
        r"\bcertificate\b",
        r"\bcertification\b",
        r"\blicence\b",
        r"\blicense\b",
        r"\bregistration\b",
        r"\bregistered\b",
    ],

    "Documentation": [
        r"\bGST\b",
        r"\bPAN\b",
        r"\bGSTIN\b",
        r"\bregistration certificate\b",
        r"\bincorporation certificate\b",
        r"\bcertificate of incorporation\b",
        r"\bundertaking\b",
        r"\bdeclaration\b",
        r"\baffidavit\b",
        r"\bdocument\b",
        r"\bdocumentary evidence\b",
    ],

    "Technical": [
        r"\btechnical specification\b",
        r"\btechnical requirement\b",
        r"\btechnical qualification\b",
        r"\btechnical capability\b",
        r"\bspecification\b",
        r"\bcapacity\b",
        r"\bperformance\b",
        r"\bcompliance\b",
        r"\bstandards\b",
    ],

    "Manpower": [
        r"\bmanpower\b",
        r"\bpersonnel\b",
        r"\bengineer\b",
        r"\btechnical staff\b",
        r"\bqualified staff\b",
        r"\bskilled personnel\b",
        r"\bproject manager\b",
        r"\bsupervisor\b",
    ],

    "Equipment": [
        r"\bequipment\b",
        r"\btools\b",
        r"\bmachinery\b",
        r"\bvehicle\b",
        r"\bplant\b",
        r"\binfrastructure\b",
    ],

    "Delivery": [
        r"\bdelivery\b",
        r"\bcompletion period\b",
        r"\bcompletion time\b",
        r"\bdelivery period\b",
        r"\bexecution period\b",
        r"\btime limit\b",
        r"\bschedule\b",
    ],

    "Security": [
        r"\bEMD\b",
        r"\bearnet money\b",
        r"\bearnest money deposit\b",
        r"\bsecurity deposit\b",
        r"\bperformance security\b",
        r"\bperformance guarantee\b",
        r"\bbank guarantee\b",
        r"\bsecurity guarantee\b",
    ],

    "Eligibility": [
        r"\beligibility\b",
        r"\beligible bidder\b",
        r"\beligibility criteria\b",
        r"\bqualification criteria\b",
        r"\bqualifying criteria\b",
        r"\bbidder shall\b",
        r"\bbidder must\b",
        r"\bbidder should\b",
    ],
}


# --------------------------------------------------
# REQUIREMENT INDICATORS
# --------------------------------------------------

REQUIREMENT_WORDS = [
    "shall",
    "must",
    "required",
    "mandatory",
    "should",
    "minimum",
    "at least",
    "not less than",
    "eligible",
    "eligibility",
    "qualification",
    "criteria",
    "submit",
    "provide",
    "furnish",
    "comply",
]


# --------------------------------------------------
# SENTENCE SPLITTER
# --------------------------------------------------

def split_into_sentences(text):
    """
    Split extracted PDF text into reasonably useful
    sentence-like chunks.
    """

    if not text:
        return []

    text = text.replace("\r", "\n")

    # Normalize excessive whitespace
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Split on line breaks first
    lines = text.split("\n")

    sentences = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Split long lines at sentence boundaries
        parts = re.split(
            r"(?<=[.!?])\s+",
            line
        )

        for part in parts:

            part = part.strip()

            if part:
                sentences.append(part)

    return sentences


# --------------------------------------------------
# CATEGORY DETECTION
# --------------------------------------------------

def detect_category(text):

    text_lower = text.lower()

    category_scores = {}

    for category, patterns in REQUIREMENT_PATTERNS.items():

        score = 0

        for pattern in patterns:

            if re.search(
                pattern,
                text_lower,
                re.IGNORECASE
            ):
                score += 1

        if score > 0:
            category_scores[category] = score

    if not category_scores:
        return "Other"

    return max(
        category_scores,
        key=category_scores.get
    )


# --------------------------------------------------
# MANDATORY DETECTION
# --------------------------------------------------

def detect_mandatory(text):

    text_lower = text.lower()

    mandatory_patterns = [
        r"\bshall\b",
        r"\bmust\b",
        r"\bmandatory\b",
        r"\brequired\b",
        r"\bminimum\b",
        r"\bat least\b",
        r"\bnot less than\b",
        r"\bcompulsory\b",
        r"\bessential\b",
    ]

    for pattern in mandatory_patterns:

        if re.search(
            pattern,
            text_lower
        ):
            return True

    return False


# --------------------------------------------------
# CONFIDENCE
# --------------------------------------------------

def calculate_confidence(text):

    text_lower = text.lower()

    strong_indicators = [
        "shall",
        "must",
        "mandatory",
        "minimum",
        "not less than",
        "at least",
        "eligible bidder",
        "bidder shall",
    ]

    medium_indicators = [
        "required",
        "submit",
        "provide",
        "furnish",
        "qualification",
        "criteria",
        "compliance",
    ]

    strong_score = sum(
        1
        for word in strong_indicators
        if word in text_lower
    )

    medium_score = sum(
        1
        for word in medium_indicators
        if word in text_lower
    )

    if strong_score >= 2:
        return "High"

    if strong_score == 1:
        return "High"

    if medium_score >= 2:
        return "Medium"

    return "Low"


# --------------------------------------------------
# REQUIREMENT DETECTION
# --------------------------------------------------

def looks_like_requirement(text):

    text_lower = text.lower()

    # Very short lines are usually headings,
    # page numbers, or table fragments.
    if len(text_lower) < 25:
        return False

    # Ignore obvious page/header/footer noise
    ignored_patterns = [
        r"^page\s+\d+$",
        r"^\d+$",
        r"^contents$",
        r"^table of contents$",
        r"^annexure$",
        r"^schedule$",
    ]

    for pattern in ignored_patterns:

        if re.fullmatch(
            pattern,
            text_lower
        ):
            return False

    keyword_found = any(
        word in text_lower
        for word in REQUIREMENT_WORDS
    )

    category = detect_category(text)

    category_found = category != "Other"

    return keyword_found or category_found


# --------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------

def clean_requirement_text(text):

    text = text.strip()

    # Remove repeated whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove bullet characters
    text = re.sub(
        r"^[•●▪■○◦\-–—]+\s*",
        "",
        text
    )

    return text.strip()


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

def remove_duplicates(requirements):

    unique = []

    seen = set()

    for item in requirements:

        key = re.sub(
            r"\W+",
            " ",
            item["requirement"].lower()
        ).strip()

        if not key:
            continue

        if key in seen:
            continue

        seen.add(key)

        unique.append(item)

    return unique


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def extract_requirements(pages):
    """
    Extract procurement requirements using
    local rule-based document analysis.

    No API key.
    No paid service.
    No internet required.
    """

    if not pages:
        return []

    requirements = []

    for page in pages:

        page_number = page.get(
            "page"
        )

        page_text = page.get(
            "text",
            ""
        )

        if not page_text.strip():
            continue

        sentences = split_into_sentences(
            page_text
        )

        for sentence in sentences:

            sentence = clean_requirement_text(
                sentence
            )

            if not sentence:
                continue

            if not looks_like_requirement(
                sentence
            ):
                continue

            category = detect_category(
                sentence
            )

            mandatory = detect_mandatory(
                sentence
            )

            confidence = calculate_confidence(
                sentence
            )

            requirements.append({

                "requirement": sentence,

                "category": category,

                "mandatory": mandatory,

                "page": page_number,

                "evidence": sentence,

                "confidence": confidence,

                "status": "Pending"

            })

    # Remove duplicates
    requirements = remove_duplicates(
        requirements
    )

    # --------------------------------------------------
    # LIMIT EXTREMELY LONG RESULTS
    # --------------------------------------------------

    for item in requirements:

        if len(
            item["requirement"]
        ) > 500:

            item["requirement"] = (
                item["requirement"][:497]
                + "..."
            )

        if len(
            item["evidence"]
        ) > 500:

            item["evidence"] = (
                item["evidence"][:497]
                + "..."
            )

    print(
        f"Rule-based extractor found "
        f"{len(requirements)} requirements."
    )

    return requirements