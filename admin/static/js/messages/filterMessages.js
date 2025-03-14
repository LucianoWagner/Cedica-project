$(document).ready(function () {
    function updateUrlParams(params) {
        const url = new URL(window.location.href);
        Object.keys(params).forEach(key => {
            if (params[key]) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        window.history.pushState({}, '', url);
        location.reload(); // Refresh the page with the updated URL
    }

    const urlParams = new URLSearchParams(window.location.search);
    const statusParam = urlParams.get("status");

    if (statusParam) {
        $(`#${statusParam.toLowerCase()}-filter`).prop("checked", true);
    }

    // Handle status filter checkbox selection
    $(".status-checkbox").on("change", function () {
        if (this.checked) {
            $(".status-checkbox").not(this).prop("checked", false);
            updateUrlParams({status: this.value});
        } else {
            updateUrlParams({status: ""});
        }
    });

    // Submit the form on filter change
    $("#status-filter-form").on("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const selectedStatus = formData.get("status-filter");

        if (selectedStatus) {
            updateUrlParams({status: selectedStatus});
        } else {
            updateUrlParams({status: ""});
        }
    });
});
