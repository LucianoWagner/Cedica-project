$(document).ready(function () {
    // Function to update the search input placeholder
    function updateSearchPlaceholder(criteria) {
        let placeholder = "Buscar por criterio...";
        switch (criteria) {
            case "dni":
                placeholder = "Buscar por DNI...";
                break;
            case "nombre":
                placeholder = "Buscar por nombre...";
                break;
            case "apellido":
                placeholder = "Buscar por apellido...";
                break;
            case "email":
                placeholder = "Buscar por email...";
                break;
        }
        $("#search-input").attr("placeholder", placeholder);
    }

    const urlParams = new URLSearchParams(window.location.search);
    const criteriaParam = urlParams.get("criteria");
    const searchParam = urlParams.get("search");
    const job_positionParam = urlParams.get("job_position");

    if (criteriaParam === "dni") {
        $("#dni-filter").prop("checked", true);
    } else if (criteriaParam === "nombre") {
        $("#name-filter").prop("checked", true);
    } else if (criteriaParam === "apellido") {
        $("#surname-filter").prop("checked", true);
    } else if (criteriaParam === "email") {
        $("#email-filter").prop("checked", true);
    }

    // Update the search input placeholder based on the criteria parameter
    if (criteriaParam) {
        updateSearchPlaceholder(criteriaParam);
    }

    if (searchParam) {
        $("#search-input").val(searchParam);
    }

    if (job_positionParam) {
        const selectedJobs = job_positionParam.split(",");
        selectedJobs.forEach((job_position) => {
            $(`#job-${job_position.trim().replace(/ /g, '_')}`).prop("checked", true);
        });
    }

    // Submit forms for filtering users
    $('#search-button').on("click", function () {
        $("#search-form").submit();
    });

    $('input[name="criteria-filter"]').on("click", function () {
        const formData = new FormData($("#criteria-filter-form")[0]);
        const criteria = formData.get("criteria-filter");
        console.log(criteria)

        if (criteria) {
            updateUrlParams({criteria: criteria.toLowerCase()});
            // Update the placeholder when criteria is selected
            updateSearchPlaceholder(criteria.toLowerCase());
        } else {
            updateUrlParams({criteria: ""});
            // Reset the placeholder if no criteria is selected
            $("#search-input").attr("placeholder", "Buscar por criterio...");
        }
    });

    $('input[name="job-filter"]').on("click", function () {
        $("#job-filter-form").submit();
    });

    $("#job-filter-form").on("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const selectedJobs = formData.getAll("job-filter");

        if (selectedJobs.length > 0) {
            updateUrlParams({job_position: selectedJobs.join(",")});
        } else {
            updateUrlParams({job_position: ""});
        }
    });

    $("#criteria-filter-form").on("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const criteria = formData.get("criteria-filter").toLowerCase();
        updateUrlParams({criteria: criteria});
    });

    $("#search-form").on("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const search = formData.get("search-input");
        updateUrlParams({search: search});
    });

    // Ensure only one checkbox is selected at a time and update URL params
    document.querySelectorAll('.criteria-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                document.querySelectorAll('.criteria-checkbox').forEach(cb => {
                    if (cb !== this) cb.checked = false;
                });
                updateUrlParams({criteria: this.value.toLowerCase()});
                // Update the placeholder when criteria checkbox changes
                updateSearchPlaceholder(this.value.toLowerCase());
            } else {
                updateUrlParams({criteria: ""});
                // Reset the placeholder if no criteria is selected
                $("#search-input").attr("placeholder", "Buscar por cualquier criterio...");
            }
        });
    });
});
