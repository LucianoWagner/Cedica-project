$(document).ready(function () {
  let data_id;
  let url;

  // Use event delegation to target all delete buttons dynamically
  $(document).on("click", "[id^=delete-btn-]", function () {
    data_id = $(this).data("id"); // Get the data-id from the clicked button
    url = $(this).data("url"); // Get the data-url from the clicked button
    console.log("URL: " + url);
  });

  // Confirm delete button
  $("#confirm-delete").on("click", function () {
    deleteData(data_id).then(() => {
      window.location.reload(); // Reload the page after deletion
    });
  });

  // Function to delete data
  function deleteData(data_id) {
    return fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (response.status === 204) {
        document.getElementById(`row-${data_id}`).remove(); // Remove the row if delete is successful
      }
    });
  }
});
