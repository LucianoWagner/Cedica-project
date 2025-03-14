$(document).ready(function () {
  function handleViewButtonClick() {
    const dataGetUrl = $(this).data("get-url");
    const dataId = $(this).data("id");
    const fileFilterUrl = $(this).data("file-filter-url");
    $("#url_file_filter").val(fileFilterUrl);

    handleAjaxRequest(
      dataGetUrl,
      { horse_id: dataId },
      function (response) {
        console.log(response);
        updateFormFields(response, "view");
        updateSelectOptions("#view_trainers", response.trainers);
        updateSelectOptions("#view_riders", response.riders);
        updateFileUploadContainer(
          "#view-file-upload-container",
          response.files,
          true,
        );
        $("#name_file_filter").val("");
        $("#type_file_filter").val("");
      },
      function (error) {
        console.error("Error fetching horse data:", error);
      },
    );
  }

  function handleEditButtonClick() {
    const dataUrl = $(this).data("url");
    const dataId = $(this).data("id");

    handleAjaxRequest(
      dataUrl,
      { horse_id: dataId },
      function (response) {
        console.log(response);
        updateFormFields(response, "edit");
        response.trainers.forEach((trainer) => {
          $(`#edit-trainer-${trainer.id}`).prop("checked", true);
        });
        updateButton(
          $("#editDropdownTrainersButton"),
          $(`#editDropdownTrainers input[type="checkbox"]`),
        );
        response.riders.forEach((rider) => {
          $(`#edit-rider-${rider.id}`).prop("checked", true);
        });
        updateButton(
          $("#editDropdownRidersButton"),
          $(`#editDropdownRiders input[type="checkbox"]`),
        );
        updateFileUploadContainer(
          "#edit-file-upload-container",
          response.files,
          false,
        );
        $("#edit-url").val(dataUrl);
      },
      function (error) {
        console.error("Error fetching horse data:", error);
      },
    );
  }

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

  $('[id^="view-button-"]').on("click", handleViewButtonClick);
  $('[id^="edit-button-"]').on("click", handleEditButtonClick);
});
