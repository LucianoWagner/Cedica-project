$(document).ready(function () {
  $("#addUserForm").on("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const addUserButton = document.getElementById("addUserButton");
    const url = addUserButton.getAttribute("data-url");
    $.ajax({
      type: "POST",
      url: url,
      processData: false,
      contentType: false,
      data: formData,
      success: function () {
        $("#addUserForm")[0].reset();
        $("#addUserModal").hide();
        location.reload();
        $("#user_added_alert").show();
      },
      error: function (xhr) {
        const errors = xhr.responseJSON.error;
        $("#errorMessage").text(errors);
        $("#errorMessageContainer").show();
      },
    });
  });

  $("#editUserForm").on("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    const userId = formData.get("user-id");
    const isChecked = $("#change-password-checkbox").is(":checked");
    formData.set("change_password", isChecked);
    const isActiveChecked = $("#edit-user-active").is(":checked");
    formData.set("active", isActiveChecked);
    const url = $("#edit-user-url").val();
    formData.delete("user-id");
    formData.delete("check-password");
    formData.delete("url");

    $.ajax({
      type: "PUT",
      url: url,
      processData: false,
      contentType: false,
      data: formData,
      success: function () {
        $("#editUserForm")[0].reset();
        $("#editUserModal").hide();
        location.reload();
        $("#user_updated_alert").show();
      },
      error: function (xhr) {
        const errors = xhr.responseJSON.error || "An error occurred";
        console.log(errors);
        $("#editErrorMessage").text(errors);
        $("#editErrorMessageContainer").show();
      },
    });
  });

  $("#approveUserForm").on("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const url = $("#approve-user-url").val();
    formData.delete("url");

    $.ajax({
      type: "POST",
      url: url,
      processData: false,
      contentType: false,
      data: formData,
      success: function () {
        $("#addUserForm")[0].reset();
        $("#addUserModal").hide();
        location.reload();
        $("#user_added_alert").show();
      },
      error: function (xhr) {
        const errors = xhr.responseJSON.error;
        $("#errorMessage").text(errors);
        $("#errorMessageContainer").show();
      },
    });
  });

  // Checkbox for password change
  $("#change-password-checkbox").change(function () {
    if ($(this).is(":checked")) {
      $("#edit-user-password").prop("disabled", false);
    } else {
      $("#edit-user-password").prop("disabled", true).val("");
    }
  });
});
