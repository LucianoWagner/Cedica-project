$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);

  const payment_methodParam = urlParams.get("payment_method");
  console.log(payment_methodParam);
  const memberNameParam = urlParams.get("member_name");
  const memberSurnameParam = urlParams.get("member_surname");
  const startDateParam = urlParams.get("start_date");
  const endDateParam = urlParams.get("end_date");

  function removeAccents(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  function formatPaymentMethod(method) {
    let formattedMethod = removeAccents(method.replace(/\s+/g, "-"));
    // Eliminar el "de" de tarjeta de credito y tarjeta de debito
    if (formattedMethod.includes("Tarjeta-de-Credito")) {
      formattedMethod = "Tarjeta-Credito";
    } else if (formattedMethod.includes("Tarjeta-de-Debito")) {
      formattedMethod = "Tarjeta-Debito";
    }
    return formattedMethod;
  }

  if (memberNameParam !== "") {
    $("#search-member-name-input").val(memberNameParam);
  }
  if (memberSurnameParam !== "") {
    $("#search-member-surname-input").val(memberSurnameParam);
  }

  if (payment_methodParam) {
    const selectedPayments = payment_methodParam.split(",");
    selectedPayments.forEach((payment_method) => {
      const formattedMethod = formatPaymentMethod(payment_method);
      console.log("lista" + formattedMethod);
      $(`#payment-method-filter-${payment_method}`).prop("checked", true);
    });
  }
  if (startDateParam) {
    $("#datepicker-range-start").val(startDateParam);
  }
  if (endDateParam) {
    $("#datepicker-range-end").val(endDateParam);
  }

  $("#search-member-form").on("submit", function (event) {
    event.preventDefault();
    const memberName = $("#search-member-name-input").val();
    const memberSurname = $("#search-member-surname-input").val();
    updateUrlParams({ member_name: memberName, member_surname: memberSurname });
  });

  $("#payment-method-filter-form input[name='payment_method']").on(
    "change",
    function () {
      $("#payment-method-filter-form").submit();
    },
  );
  $("#payment-method-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const selectedPayment = formData.getAll("payment_method");
    console.log("ji" + selectedPayment);
    if (selectedPayment.length > 0) {
      updateUrlParams({ payment_method: selectedPayment.join(",") });
    } else {
      updateUrlParams({ payment_method: "" });
    }
  });
  $("#date-filter-form").on("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const startDate = formData.get("start-date");
    const endDate = formData.get("end-date");
    updateUrlParams({ start_date: startDate, end_date: endDate });
  });
});
