$(document).ready(function () {
    // Handle the Add Member Form submission
    $("#addForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const addMemberButton = document.getElementById("addMemberButton");
        const url = addMemberButton.getAttribute("data-url");

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
                $("#member_added_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.message || "Ocurrió un error inesperado al agregar el miembro";
                console.log(errors)
                $("#errorMessage").text(errors);
                $("#errorMessageContainer").show();
            },
        });
    });

    // Handle the Edit Member Form submission
    $("#editForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        const memberId = $("#edit_id").val();  // Get the member ID from the hidden input
        formData.delete("url");
        formData.delete("id");
        const activeValue = formData.get("active") === "1"; // true if "1", false otherwise
        formData.set("active", activeValue); // Set it as a boolean in FormData

        // Construct the URL with the user ID
        const url = `/members/${memberId}`;  // Make sure this matches your Flask route

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
                $("#member_updated_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.message || "Ocurrió un error inesperado al actualizar el miembro";
                $("#editErrorMessage").text(errors);
                $("#editErrorMessageContainer").show();
            },
        });
    });


});
