document.addEventListener("DOMContentLoaded", () => {

    /* ==================================================
       TENDER ELEMENTS
       ================================================== */

    const tenderInput =
        document.getElementById("tender");

    const tenderDropZone =
        document.getElementById(
            "tender-drop-zone"
        );

    const selectedFile =
        document.getElementById(
            "selected-file"
        );

    const analyzeButton =
        document.getElementById(
            "analyze-button"
        );

    const tenderForm =
        document.getElementById(
            "tender-form"
        );


    /* ==================================================
       BIDDER ELEMENTS
       ================================================== */

    const bidderInput =
        document.getElementById(
            "bidder_documents"
        );

    const bidderDropZone =
        document.getElementById(
            "bidder-drop-zone"
        );

    const bidderSelectedFiles =
        document.getElementById(
            "bidder-selected-files"
        );

    const bidderButton =
        document.getElementById(
            "bidder-button"
        );

    const bidderForm =
        document.getElementById(
            "bidder-form"
        );


    /* ==================================================
       TENDER FILE SELECTION
       ================================================== */

    if (tenderInput) {

        tenderInput.addEventListener(
            "change",
            () => {

                const file =
                    tenderInput.files[0];


                if (!file) {

                    if (selectedFile) {

                        selectedFile.textContent =
                            "";

                    }

                    return;

                }


                if (
                    !file.name
                        .toLowerCase()
                        .endsWith(".pdf")
                ) {

                    if (selectedFile) {

                        selectedFile.textContent =
                            "Please select a PDF file.";

                    }

                    tenderInput.value = "";

                    return;

                }


                if (selectedFile) {

                    selectedFile.textContent =
                        `${file.name} · ${formatFileSize(
                            file.size
                        )}`;

                }

            }
        );

    }


    /* ==================================================
       TENDER DRAG & DROP
       ================================================== */

    if (tenderDropZone) {

        [
            "dragenter",
            "dragover"
        ].forEach(
            eventName => {

                tenderDropZone.addEventListener(
                    eventName,
                    event => {

                        event.preventDefault();

                        tenderDropZone.classList.add(
                            "drag-over"
                        );

                    }
                );

            }
        );


        [
            "dragleave",
            "drop"
        ].forEach(
            eventName => {

                tenderDropZone.addEventListener(
                    eventName,
                    event => {

                        event.preventDefault();

                        tenderDropZone.classList.remove(
                            "drag-over"
                        );

                    }
                );

            }
        );


        tenderDropZone.addEventListener(
            "drop",
            event => {

                const files =
                    event.dataTransfer.files;


                if (
                    !files ||
                    !files.length
                ) {
                    return;
                }


                const file =
                    files[0];


                if (
                    !file.name
                        .toLowerCase()
                        .endsWith(".pdf")
                ) {

                    if (selectedFile) {

                        selectedFile.textContent =
                            "Only PDF files are supported.";

                    }

                    return;

                }


                try {

                    const dataTransfer =
                        new DataTransfer();


                    dataTransfer.items.add(
                        file
                    );


                    tenderInput.files =
                        dataTransfer.files;

                } catch (error) {

                    console.error(
                        "Could not assign dropped file:",
                        error
                    );

                }


                if (selectedFile) {

                    selectedFile.textContent =
                        `${file.name} · ${formatFileSize(
                            file.size
                        )}`;

                }

            }
        );

    }


    /* ==================================================
       TENDER FORM SUBMISSION
       ================================================== */

    if (tenderForm) {

        tenderForm.addEventListener(
            "submit",
            event => {

                const file =
                    tenderInput
                        ? tenderInput.files[0]
                        : null;


                if (!file) {

                    event.preventDefault();


                    if (selectedFile) {

                        selectedFile.textContent =
                            "Please select a tender PDF.";

                    }

                    return;

                }


                if (
                    !file.name
                        .toLowerCase()
                        .endsWith(".pdf")
                ) {

                    event.preventDefault();


                    if (selectedFile) {

                        selectedFile.textContent =
                            "Only PDF files are supported.";

                    }

                    return;

                }


                if (analyzeButton) {

                    analyzeButton.disabled =
                        true;


                    analyzeButton.innerHTML = `
                        <span class="loading-spinner"></span>
                        <span>Analyzing tender...</span>
                    `;

                }

            }
        );

    }


    /* ==================================================
       BIDDER FILE SELECTION
       ================================================== */

    if (bidderInput) {

        bidderInput.addEventListener(
            "change",
            () => {

                updateBidderFileDisplay();

            }
        );

    }


    /* ==================================================
       BIDDER DRAG & DROP
       ================================================== */

    if (bidderDropZone) {

        [
            "dragenter",
            "dragover"
        ].forEach(
            eventName => {

                bidderDropZone.addEventListener(
                    eventName,
                    event => {

                        event.preventDefault();

                        bidderDropZone.classList.add(
                            "drag-over"
                        );

                    }
                );

            }
        );


        [
            "dragleave",
            "drop"
        ].forEach(
            eventName => {

                bidderDropZone.addEventListener(
                    eventName,
                    event => {

                        event.preventDefault();

                        bidderDropZone.classList.remove(
                            "drag-over"
                        );

                    }
                );

            }
        );


        bidderDropZone.addEventListener(
            "drop",
            event => {

                const files =
                    event.dataTransfer.files;


                if (
                    !files ||
                    !files.length
                ) {
                    return;
                }


                const pdfFiles =
                    Array.from(files).filter(
                        file =>
                            file.name
                                .toLowerCase()
                                .endsWith(".pdf")
                    );


                if (!pdfFiles.length) {

                    if (bidderSelectedFiles) {

                        bidderSelectedFiles.textContent =
                            "Only PDF files are supported.";

                    }

                    return;

                }


                try {

                    const dataTransfer =
                        new DataTransfer();


                    pdfFiles.forEach(
                        file => {

                            dataTransfer.items.add(
                                file
                            );

                        }
                    );


                    bidderInput.files =
                        dataTransfer.files;


                } catch (error) {

                    console.error(
                        "Could not assign bidder files:",
                        error
                    );

                }


                updateBidderFileDisplay();

            }
        );

    }


    /* ==================================================
       BIDDER FORM SUBMISSION
       ================================================== */

    if (bidderForm) {

        bidderForm.addEventListener(
            "submit",
            event => {

                const files =
                    bidderInput
                        ? Array.from(
                            bidderInput.files
                        )
                        : [];


                if (!files.length) {

                    event.preventDefault();


                    if (bidderSelectedFiles) {

                        bidderSelectedFiles.textContent =
                            "Please select at least one bidder PDF.";

                    }

                    return;

                }


                const invalidFiles =
                    files.filter(
                        file =>
                            !file.name
                                .toLowerCase()
                                .endsWith(".pdf")
                    );


                if (invalidFiles.length) {

                    event.preventDefault();


                    if (bidderSelectedFiles) {

                        bidderSelectedFiles.textContent =
                            "Only PDF files are supported.";

                    }

                    return;

                }


                if (bidderButton) {

                    bidderButton.disabled =
                        true;


                    bidderButton.innerHTML = `
                        <span class="loading-spinner"></span>
                        <span>Verifying bidder...</span>
                    `;

                }

            }
        );

    }


    /* ==================================================
       DISPLAY BIDDER FILES
       ================================================== */

    function updateBidderFileDisplay() {

        if (
            !bidderInput ||
            !bidderSelectedFiles
        ) {
            return;
        }


        const files =
            Array.from(
                bidderInput.files
            );


        if (!files.length) {

            bidderSelectedFiles.textContent =
                "";

            return;

        }


        const pdfFiles =
            files.filter(
                file =>
                    file.name
                        .toLowerCase()
                        .endsWith(".pdf")
            );


        if (!pdfFiles.length) {

            bidderSelectedFiles.textContent =
                "Only PDF files are supported.";

            return;

        }


        const totalSize =
            pdfFiles.reduce(
                (total, file) =>
                    total + file.size,
                0
            );


        if (pdfFiles.length === 1) {

            bidderSelectedFiles.textContent =
                `${pdfFiles[0].name} · ${formatFileSize(
                    pdfFiles[0].size
                )}`;

            return;

        }


        bidderSelectedFiles.textContent =
            `${pdfFiles.length} PDF documents · ${formatFileSize(
                totalSize
            )}`;

    }


    /* ==================================================
       NAVIGATION
       ================================================== */

    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );


    navItems.forEach(
        item => {

            item.addEventListener(
                "click",
                () => {

                    navItems.forEach(
                        navItem => {

                            navItem.classList.remove(
                                "active"
                            );

                        }
                    );


                    item.classList.add(
                        "active"
                    );

                }
            );

        }
    );


    /* ==================================================
       ACTIVE NAVIGATION ON SCROLL
       ================================================== */

    const sections =
        document.querySelectorAll(
            ".dashboard-section"
        );


    if (
        sections.length &&
        navItems.length &&
        "IntersectionObserver" in window
    ) {

        const observer =
            new IntersectionObserver(
                entries => {

                    entries.forEach(
                        entry => {

                            if (
                                !entry.isIntersecting
                            ) {
                                return;
                            }


                            const sectionId =
                                entry.target.id;


                            navItems.forEach(
                                item => {

                                    const target =
                                        item.getAttribute(
                                            "href"
                                        );


                                    if (
                                        target ===
                                        `#${sectionId}`
                                    ) {

                                        navItems.forEach(
                                            navItem => {

                                                navItem.classList.remove(
                                                    "active"
                                                );

                                            }
                                        );


                                        item.classList.add(
                                            "active"
                                        );

                                    }

                                }
                            );

                        }
                    );

                },
                {
                    rootMargin:
                        "-20% 0px -65% 0px"
                }
            );


        sections.forEach(
            section => {

                observer.observe(
                    section
                );

            }
        );

    }


    /* ==================================================
       FILE SIZE FORMATTER
       ================================================== */

    function formatFileSize(bytes) {

        if (!bytes) {
            return "0 KB";
        }


        const units = [
            "B",
            "KB",
            "MB",
            "GB"
        ];


        const index =
            Math.floor(
                Math.log(bytes) /
                Math.log(1024)
            );


        const safeIndex =
            Math.min(
                index,
                units.length - 1
            );


        const size =
            bytes /
            Math.pow(
                1024,
                safeIndex
            );


        return `${size.toFixed(
            safeIndex === 0
                ? 0
                : 1
        )} ${units[safeIndex]}`;

    }


    /* ==================================================
       LOADING SPINNER
       ================================================== */

    const spinnerStyle =
        document.createElement(
            "style"
        );


    spinnerStyle.textContent = `

        .loading-spinner {

            width: 13px;
            height: 13px;

            border: 2px solid
                rgba(255, 255, 255, 0.35);

            border-top-color:
                #ffffff;

            border-radius: 50%;

            animation:
                procureai-spin 0.7s
                linear infinite;

        }


        @keyframes procureai-spin {

            to {
                transform: rotate(360deg);
            }

        }

    `;


    document.head.appendChild(
        spinnerStyle
    );


    /* ==================================================
       INITIAL STATE
       ================================================== */

    if (selectedFile) {

        selectedFile.textContent =
            "";

    }


    if (bidderSelectedFiles) {

        bidderSelectedFiles.textContent =
            "";

    }

});