$(document).ready(function () {
    function handleEditButtonClick() {
        const url = $(this).data("url");
        handleAjaxRequest(
            url,
            {},
            function (response) {
                updateFormFields(response, "edit");
                updateFileUploadContainer(
                    "#edit-file-upload-container",
                    response.files,
                    false,
                );
                console.log(response.granted)
                $("#edit_grant_percentage").prop("disabled", !response.granted).prop("required", response.granted);
                $("#edit_scholarship").prop("checked", response.granted);
                updateToggle("#edit_deuda_field", response.behind_payment);
                $("#edit_url").val(url);
                response.professionals.forEach((professional_id) => {
                    let id = `#edit_professional_${professional_id}`;
                    $(id).prop("checked", true);
                });
            },
            function (error) {
                console.error("Error fetching member data:", error);
            },
        );
    }

    function handleViewButtonClick() {
        const url = $(this).data("url");
        const fileFilterUrl = $(this).data("file-filter-url");
        $("#url_file_filter").val(fileFilterUrl);
        handleAjaxRequest(
            url,
            {},
            function (response) {
                updateFormFields(response, "view");
                updateFileUploadContainer(
                    "#view-file-upload-container",
                    response.files,
                    true,
                );
                updateToggle("#view_scholarship", response.granted);
                updateToggle("#view_deuda_field", response.behind_payment);
                response.professionals.forEach((professional_id) => {
                    let id = `#view_professional_${professional_id}`;
                    $(id).prop("checked", true);
                });

                $("#name_file_filter").val("");
                $("#type_file_filter").val("");
            },
            function (error) {
                console.error("Error fetching member data:", error);
            },
        );
    }

    $('[id^="edit-button-"]').on("click", handleEditButtonClick);
    $('[id^="view-button-"]').on("click", handleViewButtonClick);
});
