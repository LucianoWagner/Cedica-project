$(document).ready(function () {
  function handleViewButtonClick() {
    const memberId = $(this).data("id");
    const fileFilterUrl = $(this).data("file-filter-url");
    $("#url_file_filter").val(fileFilterUrl);
    handleAjaxRequest(
      `/members/${memberId}`,
      {},
      function (response) {
        updateFormFields(response, "view");
        updateFileUploadContainer(
          "#view-file-upload-container",
          response.files,
          true
        );
        if (response.active === 1) {
          $("#view_active").val("Si");
        } else {
          $("#view_active").val("No");
        }
        $("#name_file_filter").val("");
        $("#type_file_filter").val("");
      },
      function (error) {
        console.error("Error fetching member data:", error);
      }
    );
  }

  function handleEditButtonClick() {
    const memberId = $(this).data("id");
    handleAjaxRequest(
      `/members/${memberId}`,
      {},
      function (response) {
        updateFormFields(response, "edit");
        updateFileUploadContainer(
          "#edit-file-upload-container",
          response.files,
          false
        );
        updateSelectOptions();
      },
      function (error) {
        console.error("Error fetching member data:", error);
      }
    );
  }

  $('[id^="view-button-"]').on("click", handleViewButtonClick);
  $('[id^="edit-button-"]').on("click", handleEditButtonClick);
});
