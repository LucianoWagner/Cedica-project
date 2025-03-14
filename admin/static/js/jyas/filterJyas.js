$(document).ready(function () {
  // Function to update the search input placeholder
  function updateSearchPlaceholder(criteria) {
    let placeholder = "Buscar por criterio...";
    switch (criteria) {
      case "dni":
        placeholder = "Buscar por DNI...";
        break;
      case "nombre":
        placeholder = "Buscar por Nombre...";
        break;
      case "apellido":
        placeholder = "Buscar por Apellido...";
        break;
    }
    $("#search-input").attr("placeholder", placeholder);
  }

  const urlParams = new URLSearchParams(window.location.search);
  const criteriaParam = urlParams.get("criteria");
  const searchParam = urlParams.get("search");
  const professionalParam = urlParams.get("professional");

  console.log(professionalParam);

  if (criteriaParam) {
    $(`#${criteriaParam}-filter`).prop("checked", true);
    updateSearchPlaceholder(criteriaParam);
  }

  if (professionalParam) {
    const selectedProfessionals = professionalParam.split(",");
    selectedProfessionals.forEach((professional) => {
      console.log(professional.trim().replace(/ /g, "_")); // Print each professional value
      $(`#professional-${professional.trim().replace(/ /g, "_")}`).prop(
        "checked",
        true,
      );
    });
  }

  if (searchParam) {
    $("#search-input").val(searchParam);
  }

  // Submit forms for filtering users
  $("#search-button").on("click", function () {
    $("#search-form").submit();
  });

  $('input[name="criteria-filter"]').on("click", function () {
    const formData = new FormData($("#criteria-filter-form")[0]);
    const criteria = formData.get("criteria-filter");
    console.log(criteria);

    if (criteria) {
      updateUrlParams({ criteria: criteria.toLowerCase() });
      updateSearchPlaceholder(criteria.toLowerCase());
    } else {
      updateUrlParams({ criteria: "" });
      $("#search-input").attr("placeholder", "Buscar por criterio...");
    }
  });

  $('input[name="professional-filter"]').on("click", function () {
    $("#professionals-filter-form").submit();
  });

  $("#professionals-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const professionals = formData.getAll("professional-filter");

    if (professionals.length > 0) {
      updateUrlParams({ professional: professionals.join(",") });
    } else {
      updateUrlParams({ professional: "" });
    }
  });

  $("#criteria-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const criteria = formData.get("criteria-filter").toLowerCase();
    updateUrlParams({ criteria: criteria });
  });

  $("#search-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const search = formData.get("search-input");
    updateUrlParams({ search: search });
  });

  // Ensure only one checkbox is selected at a time and update URL params
  document.querySelectorAll(".criteria-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", function () {
      if (this.checked) {
        document.querySelectorAll(".criteria-checkbox").forEach((cb) => {
          if (cb !== this) cb.checked = false;
        });
        updateUrlParams({ criteria: this.value.toLowerCase() });
        updateSearchPlaceholder(this.value.toLowerCase());
      } else {
        updateUrlParams({ criteria: "" });
        $("#search-input").attr(
          "placeholder",
          "Buscar por cualquier criterio...",
        );
      }
    });
  });
});
