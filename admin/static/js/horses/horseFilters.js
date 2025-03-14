$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const nameParam = urlParams.get("name");
  const typeParam = urlParams.get("type");

  if (typeParam) {
    const selectedTypes = typeParam.split(",");
    selectedTypes.forEach((type) => {
      let formatted_type = type.toLowerCase().replace(/ /g, "-");
      $(`#type-input-${formatted_type}`).prop("checked", true);
    });
  }

  if (nameParam) {
    $("#name-search-input").val(nameParam);
  }

  $('#jya-type-filter-form input[name="type"]').on("change", function () {
    $("#jya-type-filter-form").submit();
  });

  $("#jya-type-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const selectedType = formData.getAll("type");
    if (selectedType.length > 0) {
      updateUrlParams({ type: selectedType.join(",") });
    } else {
      updateUrlParams({ type: "" });
    }
  });

  $("#name-search-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const name = formData.get("name");
    updateUrlParams({ name: name });
  });
});
