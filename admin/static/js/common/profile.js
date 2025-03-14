// Show the modal when "open-profile-modal" is clicked
document
  .getElementById("open-profile-modal")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default link behavior

    // Open the modal
    const profileModal = document.getElementById("profileModal");
    // profileModal.classList.remove("hidden");
    // profileModal.classList.add("flex");

    // Fetch the profile data via GET request
    const url = `/users/profile`;
    $.ajax({
      type: "GET",
      url: url,
      success: function (data) {
        // Populate the modal fields with the received data
        $("#profile-email").val(data.email);
        $("#profile-role").val(
          data.role.toLowerCase().replace(/\b\w/g, function (char) {
            return char.toUpperCase();
          }),
        );
        $("#profile-member").val(data.member.name + " " + data.member.surname);
        $("#profile-alias").val(data.alias);
      },
      error: function (xhr) {
        const errors =
          xhr.responseJSON.message ||
          "Ocurrió un error inesperado al obtener el perfil";
        $("#errorMessage").text(errors);
        $("#errorMessageContainer").show();
      },
    });
  });

// Hide modal when close button is clicked
// document.querySelector("[data-modal-hide='profileModal']").addEventListener("click", function () {
//     const profileModal = document.getElementById("profileModal");
//     profileModal.classList.add("hidden");
//     profileModal.classList.remove("flex");
// });

// Handle "cambiar contraseña" button click
document
  .getElementById("change-password-btn")
  .addEventListener("click", function () {
    const passwordSection = document.getElementById("password-fields");

    // Log the current class list before manipulation
    console.log("Current class list before toggle:", passwordSection.classList);

    // Toggle display style between block and none
    if (passwordSection.style.display === "block") {
      passwordSection.style.display = "none"; // Hide
      // Clear password fields and set them as not required
      document.getElementById("profile-original-password").value = "";
      document.getElementById("profile-new-password").value = "";
      document.getElementById("profile-confirm-password").value = "";
      document.getElementById("profile-original-password").required = false;
      document.getElementById("profile-new-password").required = false;
      document.getElementById("profile-confirm-password").required = false;
    } else {
      passwordSection.style.display = "block"; // Show
      // Set fields as required
      document.getElementById("profile-original-password").required = true;
      document.getElementById("profile-new-password").required = true;
      document.getElementById("profile-confirm-password").required = true;
    }

    // Log the current style after manipulation
    console.log(
      "Current display style after toggle:",
      passwordSection.style.display,
    );
  });

// Handle form submission to check if passwords match
document
  .getElementById("profileForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission and modal closing

    // Get the new password and confirmation password values
    const passwordSection = document.getElementById("password-fields");
    const newPassword = document.getElementById("profile-new-password").value;
    const confirmPassword = document.getElementById(
      "profile-confirm-password",
    ).value;

    // Clear any previous error message
    const errorMessageContainer = document.getElementById(
      "profileErrorMessageContainer",
    );
    const errorMessage = document.getElementById("profileErrorMessage");
    errorMessage.innerText = ""; // Clear the text
    errorMessageContainer.classList.remove("block"); // Hide the container
    errorMessageContainer.classList.add("hidden"); // Initially hide

    // Check if the password fields are visible before validating passwords
    if (!passwordSection.classList.contains("hidden")) {
      // Check if the new password is shorter than 6 characters
      if (newPassword.length < 6) {
        // Set and show the error message for short password
        errorMessage.innerText =
          "La contraseña debe tener al menos 6 caracteres";
        errorMessageContainer.classList.remove("hidden"); // Show the container
        errorMessageContainer.classList.remove("bg-green-50", "text-green-800"); // Remove success styles
        errorMessageContainer.classList.add("bg-red-50", "text-red-800"); // Add error styles
        return; // Exit the function
      } else if (newPassword !== confirmPassword) {
        // Set and show the error message for mismatched passwords
        errorMessage.innerText = "Las contraseñas no coinciden";
        errorMessageContainer.classList.remove("hidden"); // Show the container
        errorMessageContainer.classList.remove("bg-green-50", "text-green-800"); // Remove success styles
        errorMessageContainer.classList.add("bg-red-50", "text-red-800"); // Add error styles
        return; // Exit the function
      }
    }

    // Send the form data to the server if the password is valid
    const alias = document.getElementById("profile-alias").value;
    const originalPassword = document.getElementById(
      "profile-original-password",
    ).value;

    const data = {
      alias: alias,
      original_password: originalPassword ? originalPassword : null,
      new_password: newPassword ? newPassword : null,
    };

    // Send the POST request to update profile
    $.ajax({
      type: "POST",
      url: `/users/profile`,
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        // Display a success message in the modal without closing it
        const successMessage = "Perfil actualizado con éxito";
        errorMessageContainer.classList.remove("bg-red-50", "text-red-800"); // Remove error styles
        errorMessageContainer.classList.add("bg-green-50", "text-green-800"); // Add success styles
        errorMessage.innerText = successMessage;
        errorMessageContainer.classList.remove("hidden");
        errorMessageContainer.classList.add("block");
      },
      error: function (xhr) {
        // Handle errors
        const errorMessageText =
          xhr.responseJSON.message ||
          "Ocurrió un error inesperado al actualizar el perfil";
        errorMessageContainer.classList.remove("bg-green-50", "text-green-800"); // Remove success styles
        errorMessageContainer.classList.add("bg-red-50", "text-red-800"); // Add error styles
        errorMessage.innerText = errorMessageText;
        errorMessageContainer.classList.remove("hidden");
        errorMessageContainer.classList.add("block");
      },
    });
  });
