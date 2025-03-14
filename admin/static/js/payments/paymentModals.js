$(document).ready(function () {
    $('[id^="edit-button-"]').on("click", function () {
        const form_data = [
            {form_name: "id", value: $(this).data("id")},
            {form_name: "date", value: formatDate($(this).data("date"))}, // Reformat date
            {form_name: "amount", value: $(this).data("amount")},
            {form_name: "member", value: $(this).data("member")},
            {form_name: "description", value: $(this).data("description")},
            {form_name: "url", value: $(this).data("url")},
            {form_name: "type", value: $(this).data("type")},
            {form_name: "created_at", value: $(this).data("created_at")},
        ];

        form_data.forEach((item) => {
            $(`#edit_${item.form_name}`).val(item.value);
        });

        // Trigger the change event to enable/disable member select
        $("#edit_type").val($(this).data("type")).trigger("change");
    });

    $("#edit_type").on("change", function () {
        // Use jQuery to select
        // Log the length of the selection
        const memberSelect = $("#edit_member");
        const selectedType = $(this).val();
        if (selectedType === "Honorarios") {
            memberSelect.prop("disabled", false); // Enable if type is "Honorarios"
            memberSelect.prop("required", true);  // Make required
        } else {
            memberSelect.prop("disabled", true);  // Disable otherwise
            memberSelect.prop("required", false); // Remove required attribute
            memberSelect.val("");                 // Clear the selection when disabling
        }
    });

    $("#addType").on("change", function () {
        // Use jQuery to select
        // Log the length of the selection
        const memberSelect = $("#addMember");
        const selectedType = $(this).val();
        if (selectedType === "Honorarios") {
            memberSelect.prop("disabled", false); // Enable if type is "Honorarios"
            memberSelect.prop("required", true);  // Make required
        } else {
            memberSelect.prop("disabled", true);  // Disable otherwise
            memberSelect.prop("required", false); // Remove required attribute
            memberSelect.val("");                 // Clear the selection when disabling
        }
    });

    $('[id^="view-button-"]').on("click", function () {
        const form_data = [
            {form_name: "id", value: $(this).data("id")},
            {form_name: "date", value: formatDate($(this).data("date"))}, // Reformat date
            {form_name: "amount", value: $(this).data("amount")},
            {form_name: "member", value: $(this).data("member")},
            {form_name: "description", value: $(this).data("description")},
            {form_name: "url", value: $(this).data("url")},
            {form_name: "type", value: $(this).data("type")},
            {form_name: "created_at", value: $(this).data("created_at")},
        ];

        form_data.forEach((item) => {
            $(`#view_${item.form_name}`).val(item.value);
        });
    });

    function formatDate(date) {
        const dbDate = new Date(date);
        const day = String(dbDate.getDate()).padStart(2, "0");
        const month = String(dbDate.getMonth() + 1).padStart(2, "0"); // Months are 0-based
        const year = dbDate.getFullYear();
        return `${day}/${month}/${year}`; // Return in dd-mm-yyyy format
    }
});
