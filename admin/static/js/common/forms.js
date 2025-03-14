function handleAjaxRequest(url, data, successCallback, errorCallback) {
  console.log(url);

  $.ajax({
    url: url,
    type: "GET",
    data: data,
    success: successCallback,
    error: errorCallback,
  });
}

function updateFormFields(response, prefix) {
  Object.keys(response).forEach(function (key) {
    const inputId = `#${prefix}_${key}`;
    if ($(inputId).length) {
      $(inputId).val(response[key]);
    }
  });
}

function updateSelectOptions(selectId, options) {
  $(selectId).empty();
  options.forEach(function (option) {
    $(selectId).append(
      `<option value="${option.id}">${option.name} ${option.surname}</option>`,
    );
  });
  $(selectId).trigger("change");
}

function updateToggle(toggleId, value) {
  $(toggleId).prop("checked", value);
}

$(document).ready(function () {
  $("#files-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const url = formData.get("url");
    console.log(url);
    handleAjaxRequest(
      url,
      {
        title: formData.get("title"),
        type: formData.get("type"),
      },
      function (response) {
        console.log(response);
        updateFileUploadContainer(
          "#view-file-upload-container",
          response,
          true,
        );
      },
      function (xhr) {
        console.error(xhr);
      },
    );
  });
});
