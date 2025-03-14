function formatDate(dateString) {
  const date = new Date(dateString); // Convierte la cadena a un objeto Date
  const day = String(date.getDate()).padStart(2, "0"); // Obtiene el día y lo formatea
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Obtiene el mes y lo formatea
  const year = date.getFullYear(); // Obtiene el año

  return `${day}/${month}/${year}`; // Retorna la fecha en el formato deseado
}

$(document).ready(function () {
  // Evento click para el botón de edición
  $('[id^="edit-button-"]').on("click", function () {
    const dataGetUrl = $(this).data("get-url"); // La URL de la API para obtener los datos del cobro
    const chargeId = $(this).data("id"); // El ID del cobro

    // Verifica que dataGetUrl y chargeId no sean nulos o indefinidos
    if (!dataGetUrl || !chargeId) {
      alert("Error: URL o ID del cobro no válidos.");
      return;
    }

    // Realiza la solicitud AJAX
    $.ajax({
      url: dataGetUrl,
      type: "GET",
      data: { charge_id: chargeId },
      success: function (response) {
        console.log(response); // Para depuración

        // Actualizar los campos del formulario con los datos recibidos
        $("#edit_jya").val(response.jya);
        $("#edit_amount").val(response.amount);
        $("#edit_observations").val(response.observations);
        $("#edit_member").val(response.member);
        $("#edit_payment_method").val(response.payment_method);

        //carga en el input con id edit_url la url porque sino no se envia en el formulario y por eso daba vacio
        $("#edit_url").val(dataGetUrl);
        $("#edit_date").val(formatDate(response.date)); // Formatear la fecha

        // Mostrar la ventana modal después de cargar los datos
        $("#editModal").modal("show");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
        alert("Error al recuperar los datos del cobro.");
      },
    });
  });

  // Evento click para el botón de visualización
  $('[id^="view-button-"]').on("click", function () {
    const dataGetUrl = $(this).data("get-url"); // La URL de la API para obtener los datos del cobro
    const chargeId = $(this).data("id"); // El ID del cobro

    // Verifica que dataGetUrl y chargeId no sean nulos o indefinidos
    if (!dataGetUrl || !chargeId) {
      alert("Error: URL o ID del cobro no válidos.");
      return;
    }

    // Realiza la solicitud AJAX
    $.ajax({
      url: dataGetUrl,
      type: "GET",
      data: { charge_id: chargeId },
      success: function (response) {
        console.log(response); // Para depuración

        // Actualizar los campos del formulario con los datos recibidos
        $("#view_jya").val(response.jya_name);
        $("#view_date").val(formatDate(response.date)); // Formatear la fecha
        $("#view_amount").val(response.amount);
        $("#view_observations").val(response.observations);
        $("#view_member").val(response.member_name);
        $("#view_payment_method").val(response.payment_method);

        // Mostrar la ventana modal después de cargar los datos
        $("#viewModal").modal("show");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error("Error en la solicitud AJAX:", textStatus, errorThrown);
        alert("Error al recuperar los datos del cobro.");
      },
    });
  });
});
