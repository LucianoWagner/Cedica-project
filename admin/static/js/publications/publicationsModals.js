$(document).ready(function () {
    function handleViewButtonClick() {
        const publicationId = $(this).data("id");
        handleAjaxRequest(
            `/publications/${publicationId}`,
            {},
            function (response) {
                updateFormFields(response, "view");
            },
            function (error) {
                console.error("Error fetching publication data:", error);
            },
        );
    }

    function handleEditButtonClick() {
        const publicationId = $(this).data("id");
        handleAjaxRequest(
            `/publications/${publicationId}`,
            {},
            function (response) {
                updateFormFields(response, "edit");
            },
            function (error) {
                console.error("Error fetching publication data:", error);
            },
        );
    }

    $(document).on("click", '[id^="view-button-"]', handleViewButtonClick);
    $(document).on("click", '[id^="edit-button-"]', handleEditButtonClick);
});
