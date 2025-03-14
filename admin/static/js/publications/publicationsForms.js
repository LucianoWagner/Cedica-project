$(document).ready(function () {
    // Handle the Add Publication Form submission
    $("#addForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const addPublicationButton = document.getElementById("addPublicationButton");
        const url = addPublicationButton.getAttribute("data-url");

        $.ajax({
            type: "POST",
            url: url,
            processData: false,
            contentType: false,
            data: formData,
            success: function () {
                $("#addForm")[0].reset();
                $("#addModal").hide();
                location.reload();
                $("#publication_added_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.message || "Ocurrió un error inesperado al agregar la publicación";
                $("#errorMessage").text(errors);
                $("#errorMessageContainer").show();
            },
        });
    });

    // Handle the Edit Publication Form submission
    $("#editForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        const publicationId = $("#edit_id").val(); // Get the publication ID from the hidden input
        const url = `/publications/${publicationId}`; // Construct the URL for the edit endpoint

        $.ajax({
            type: "PUT",
            url: url,
            processData: false,
            contentType: false,
            data: formData,
            success: function () {
                $("#editForm")[0].reset();
                $("#editModal").hide();
                location.reload();
                $("#publication_updated_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.message || "Ocurrió un error inesperado al actualizar la publicación";
                $("#editErrorMessage").text(errors);
                $("#editErrorMessageContainer").show();
            },
        });
    });
});
