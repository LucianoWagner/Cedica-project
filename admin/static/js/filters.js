// static/js/filters.js
function updateUrlParams(params) {
  var url = new URL(window.location);
  var urlParams = new URLSearchParams(url.search);

  // Loop through the params object and update the query string
  for (const [key, value] of Object.entries(params)) {
    if (value === "") {
      urlParams.delete(key); // Remove param if value is empty
    } else {
      urlParams.set(key, value); // Set or update param
    }
  }

  var newUrl = url.pathname + "?" + urlParams.toString();

  // Redirect to the new URL (this will trigger a new GET request)
  window.location.href = newUrl;
}
