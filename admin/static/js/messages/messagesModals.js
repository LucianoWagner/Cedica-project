$(document).ready(function () {
    function handleViewButtonClick() {
        const messageId = $(this).data("id");
        handleAjaxRequest(
            `/messages/${messageId}`,
            {},
            function (response) {
                updateFormFields(response, "view");
            },
            function (error) {
                console.error("Error fetching message data:", error);
            },
        );
    }

    function handleEditButtonClick() {
        const messageId = $(this).data("id");
        handleAjaxRequest(
            `/messages/${messageId}`,
            {},
            function (response) {
                updateFormFields(response, "edit");
            },
            function (error) {
                console.error("Error fetching message data:", error);
            },
        );
    }

    $(document).on("click", '[id^="view-button-"]', handleViewButtonClick);
    $(document).on("click", '[id^="edit-button-"]', handleEditButtonClick);
});
