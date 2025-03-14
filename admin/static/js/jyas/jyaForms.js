$(document).ready(function () {
    // Función para validar la selección de profesionales
    function validateProfessionalsSelection(checkboxes, errorMessageContainer, message) {
        const isSelected = checkboxes.filter(":checked").length > 0;
        if (!isSelected) {
            errorMessageContainer.text(message).show();
        }
        return isSelected;
    }

    function validateProfessionalsSelectionEdit(checkboxes, errorMessageContainer, message) {
        const isSelected = checkboxes.filter(":checked").length > 0;
        if (!isSelected) {
            errorMessageContainer.text(message).show();
        }
        return isSelected;
    }

    // Manejar la presentación del formulario de agregar
    $("#addForm").on("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const addJyaButton = document.getElementById("addJyaButton"); // ID del botón que abre el formulario
        const url = addJyaButton.getAttribute("data-url");
        const granted = formData.get("granted") === "on";
        formData.set("granted", granted);
        const behind_payment = formData.get("behind_payment") === "on";
        formData.set("behind_payment", behind_payment);

        // Obtener los checkboxes de profesionales y el contenedor de mensajes de error
        const professionalsCheckboxes = $('#professionals_list input[type="checkbox"]');
        const errorMessageContainer = $("#addErrorMessageContainer");

        // Resetear mensajes de error
        errorMessageContainer.hide().empty();

        // Validar que al menos un profesional esté seleccionado
        const isProfessionalsSelected = validateProfessionalsSelection(professionalsCheckboxes, errorMessageContainer, "Seleccione al menos un profesional.");

        if (!isProfessionalsSelected) {
            return; // Detener la presentación si la validación falla
        }

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
                $("#jya_added_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.error;
                $("#addErrorMessage").text(errors);
                $("#addErrorMessageContainer").show();
            },
        });
    });

    // Manejar la presentación del formulario de edición
    $("#editForm").on("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const url = formData.get("url");
        const granted = formData.get("granted") === "on";
        formData.set("granted", granted);
        const behind_payment = formData.get("behind_payment") === "on";
        formData.set("behind_payment", behind_payment);

        // Obtener los checkboxes de profesionales en el formulario de edición
        const editProfessionalsCheckboxes = $('#edit_professionals_list input[type="checkbox"]');
        const editErrorMessageContainer = $("#edit_error_message_container");

        // Resetear mensajes de error
        editErrorMessageContainer.hide().empty();

        // Validar que al menos un profesional esté seleccionado

        const isEditProfessionalsSelected = validateProfessionalsSelectionEdit(editProfessionalsCheckboxes, editErrorMessageContainer, "Seleccione al menos un profesional.");


        if (!isEditProfessionalsSelected) {
            return; // Detener la presentación si la validación falla
        }


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
                $("#jya_updated_alert").show();
            },
            error: function (xhr) {
                const errors = xhr.responseJSON.error;
                $("#editErrorMessage").text(errors);
                $("#editErrorMessageContainer").show();
            },
        });
    });

    // Función para habilitar/deshabilitar el porcentaje de beca
    function toggleScholarshipPercentage() {
        var checkbox = $('#addScholarship');
        var input = $('#addScholarshipPercentage');
        console.log(input)
        input.prop('disabled', !checkbox.is(':checked'));
        input.prop('required', checkbox.is(':checked'));
        if (!checkbox.is(':checked')) {
            input.val(''); // Limpiar el valor si el checkbox está desmarcado
        }
    }

    // Función para habilitar/deshabilitar el porcentaje de beca
    function toggleScholarshipPercentageEdit() {
        var checkbox = $('#edit_scholarship');
        var input = $('#edit_grant_percentage');
        console.log(input)
        input.prop('disabled', !checkbox.is(':checked'));
        input.prop('required', checkbox.is(':checked'));
        if (!checkbox.is(':checked')) {
            input.val(''); // Limpiar el valor si el checkbox está desmarcado
        }
    }

    // Llamar a la función cuando cambie el estado del checkbox
    $('#edit_scholarship').on('change', toggleScholarshipPercentageEdit);
    $('#addScholarship').on('change', toggleScholarshipPercentage);

    // Manejar el envío del formulario
    $('form').on('submit', function () {
        var checkbox = $('#addScholarship');
        var hiddenInput = $('#addScholarshipPercentage');
        if (!checkbox.is(':checked')) {
            hiddenInput.val(0);
        } else {
            var inputValue = hiddenInput.val();
            hiddenInput.val(inputValue || 0); // Usar el valor del input o 0 si está vacío
        }
    });

    // Función para actualizar el valor de la deuda
    function updateDebtValue(form) {
        const debtCheckbox = form.find('input[name="behind_payment"]');
        debtCheckbox.prop('checked', debtCheckbox.is(':checked'));
        form.data('behind_payment', debtCheckbox.is(':checked')); // Puedes usar data para guardar el valor booleano
    }

    // Manejar cambios en los checkboxes de deuda
    $('#addDeudaField').on('change', function () {
        updateDebtValue($("#addForm"));
    });

    $('#edit_deuda_field').on('change', function () {
        updateDebtValue($("#editForm"));
    });
});
