$(document).ready(function () {
    const urlParams = new URLSearchParams(window.location.search);
    const typeParam = urlParams.get("type");
    const startDateParam = urlParams.get("start_date");
    const endDateParam = urlParams.get("end_date");

    if (typeParam) {
        const selectedTypes = typeParam.replace(/ /g, '-').split(",");
        selectedTypes.forEach((type) => {
            console.log(type);
            $(`#type-filter-${type}`).prop("checked", true);
        });
    }

    if (startDateParam) {
        $("#datepicker-range-start").val(startDateParam);
    }

    if (endDateParam) {
        $("#datepicker-range-end").val(endDateParam);
    }

    $('#type-filter-form input[name="type"]').on("change", function () {
        $("#type-filter-form").submit();
    });
    $("#type-filter-form").on("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const selectedType = formData.getAll("type");
        if (selectedType.length > 0) {
            updateUrlParams({type: selectedType.join(",")});
        } else {
            updateUrlParams({type: ""});
        }
    });

    $("#date-filter-form").on("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const startDate = formData.get("start-date");
        const endDate = formData.get("end-date");
        updateUrlParams({start_date: startDate, end_date: endDate});
    });
});
