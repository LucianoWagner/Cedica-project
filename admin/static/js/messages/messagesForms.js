$(document).ready(function () {

    // Handle the Edit Message Form submission
    $("#editForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        const messageId = $("#edit_id").val(); // Get the message ID from the hidden input
        const url = `/messages/${messageId}`; // Construct the URL for the edit endpoint

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
                $("#message_updated_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.message || "Ocurrió un error inesperado al actualizar la publicación";
                $("#editErrorMessage").text(errors);
                $("#editErrorMessageContainer").show();
            },
        });
    });
});
