$(document).ready(function () {
    const addRidersButton = $("#dropdownRidersButton");
    const addTrainersButton = $("#dropdownTrainersButton");
    const addRidersCheckboxes = $('#dropdownRiders input[type="checkbox"]');
    const addTrainersCheckboxes = $('#dropdownTrainers input[type="checkbox"]');

    const editRidersButton = $("#editDropdownRidersButton");
    const editTrainersButton = $("#editDropdownTrainersButton");
    const editRidersCheckboxes = $('#editDropdownRiders input[type="checkbox"]');
    const editTrainersCheckboxes = $('#editDropdownTrainers input[type="checkbox"]');

    function updateButton(button, checkboxes) {
        const selected = checkboxes
            .filter(":checked")
            .map(function () {
                return $(this).next("label").text().trim();
            })
            .get()
            .join(", ");
        button.find("span").text(selected || "Seleccionar");
    }

    addRidersCheckboxes.change(function () {
        updateButton(addRidersButton, addRidersCheckboxes);
    });

    addTrainersCheckboxes.change(function () {
        updateButton(addTrainersButton, addTrainersCheckboxes);
    });

    editRidersCheckboxes.change(function () {
        updateButton(editRidersButton, editRidersCheckboxes);
    });

    editTrainersCheckboxes.change(function () {
        updateButton(editTrainersButton, editTrainersCheckboxes);
    });

    // Initial update
    updateButton(addRidersButton, addRidersCheckboxes);
    updateButton(addTrainersButton, addTrainersCheckboxes);
    updateButton(editRidersButton, editRidersCheckboxes);
    updateButton(editTrainersButton, editTrainersCheckboxes);

    function validateSelection(checkboxes, errorMessageContainer, message) {
        const isSelected = checkboxes.filter(":checked").length > 0;
        if (!isSelected) {
            errorMessageContainer.html(message).show();
        }
        return isSelected;
    }

    $("#addForm").on("submit", function (e) {
        e.preventDefault();
        const errorMessageContainer = $("#addErrorMessageContainer");

        // Reset error messages
        errorMessageContainer.hide().empty();

        // Validate selections
        const isRidersSelected = validateSelection(addRidersCheckboxes, errorMessageContainer, "Seleccione al menos un corredor.");
        const isTrainersSelected = validateSelection(addTrainersCheckboxes, errorMessageContainer, "Seleccione al menos un entrenador.");

        if (!isRidersSelected || !isTrainersSelected) {
            return; // Stop submission if validation fails
        }

        const formData = new FormData(this);
        const addHorseButton = document.getElementById("addHorseButton");
        const url = addHorseButton.getAttribute("data-url");

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
        const errorMessageContainer = $("#editErrorMessageContainer");

        // Reset error messages
        errorMessageContainer.hide().empty();

        // Validate selections
        const isRidersSelected = validateSelection(editRidersCheckboxes, errorMessageContainer, "Seleccione al menos un corredor.");
        const isTrainersSelected = validateSelection(editTrainersCheckboxes, errorMessageContainer, "Seleccione al menos un entrenador.");

        if (!isRidersSelected || !isTrainersSelected) {
            return; // Stop submission if validation fails
        }

        const formData = new FormData(this);
        const url = formData.get("url");
        formData.delete("url");

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
                $("#payment_edited_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.error;
                $("#editerrorMessage").text(errors);
                $("#editerrorMessageContainer").show();
            },
        });
    });
});
