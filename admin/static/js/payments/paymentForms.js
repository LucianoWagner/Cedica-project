$(document).ready(function () {
    $("#addForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const addPaymentButton = document.getElementById("addPaymentButton");
        const url = addPaymentButton.getAttribute("data-url");
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
                $("#payment_added_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.error;
                $("#adderrorMessage").text(errors);
                $("#adderrorMessageContainer").show();
            },
        });
    });

    $("#editForm").on("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const url = formData.get("url");
        const activeValue = formData.get("active");

        formData.delete("url");
        formData.delete("id");


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
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.error;
                $("#editErrorMessage").text(errors);
                $("#editErrorMessageContainer").show();
            },
        });
    });
});
