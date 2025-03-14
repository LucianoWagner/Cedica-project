$(document).ready(function () {
  $("#addForm").on("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const addChargeButton = document.getElementById("addChargeButton"); //va el id que te abre el formulario la cual esta en el table header
    const url = addChargeButton.getAttribute("data-url");

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
        $("#charge_added_alert").show();
      },
      error: function (xhr) {
        const errors = xhr.responseJSON.error;
        $("#addErrorMessage").text(errors);
        $("#addErrorMessageContainer").show();
      },
    });
  });
  $("#editForm").on("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const chargeId = $(this).data("id");
    const url = formData.get("url"); // Es la url del input hidden q se encuentra en charges_edit_modal cuyo name ="url"

    console.log("Charge ID:", chargeId);
    console.log("URL:", url);
    console.log(formData);
    formData.delete("url");
    formData.delete("id");

    $.ajax({
      type: "PUT",
      url: url,
      data: formData,
      processData: false,
      contentType: false,
      success: function () {
        // Cierra el modal, resetea el formulario, y recarga la página
        $("#editForm")[0].reset();
        $("#editModal").hide();
        location.reload();
      },
      error: function (xhr) {
        const errors = xhr.responseJSON
          ? xhr.responseJSON.message
          : "Error al actualizar el registro.";
        $("#editErrorMessage").text(errors);
        $("#editErrorMessageContainer").show();
      },
    });
  });
});
