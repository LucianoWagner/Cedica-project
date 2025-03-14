$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const activeParam = urlParams.get("active");
  const emailParam = urlParams.get("email");
  const rolesParam = urlParams.get("roles");

  if (activeParam === "true") {
    $("#filter-active-users").prop("checked", true);
  } else if (activeParam === "false") {
    $("#filter-inactive-users").prop("checked", true);
  } else {
    $("#filter-all-users").prop("checked", true);
  }

  if (emailParam) {
    $("#search-email-input").val(emailParam);
  }

  if (rolesParam) {
    const selectedRoles = rolesParam.split(",");
    selectedRoles.forEach((roleId) => {
      $(`#role-${roleId}`).prop("checked", true);
    });
  }

  // Submit forms for filtering users
  $('input[name="user-status-filter"]').on("click", function () {
    $("#user-filter-form").submit();
  });

  $('input[name="role-filter"]').on("click", function () {
    $("#role-filter-form").submit();
  });

  $("#role-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const selectedRoles = formData.getAll("role-filter");

    if (selectedRoles.length > 0) {
      updateUrlParams({ roles: selectedRoles.join(",") });
    } else {
      updateUrlParams({ roles: "" });
    }
  });

  $("#user-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const status = formData.get("user-status-filter");
    updateUrlParams({ active: status });
  });

  $("#search-email-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const email = formData.get("email");
    updateUrlParams({ email: email });
  });
});
