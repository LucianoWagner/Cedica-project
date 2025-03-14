$(document).ready(function () {
  $('[id^="edit-button-user-"]').on("click", function () {
    const userId = $(this).data("user-id");
    const email = $(this).data("user-email");
    const role = $(this).data("user-role");
    const active = $(this).data("user-active");
    const member = $(this).data("user-member");
    const alias = $(this).data("user-alias");
    const url = $(this).data("url");

    $("#edit-user-id").val(userId);
    $("#edit-user-email").val(email);
    $("#edit-user-role").val(role);
    $("#edit-user-member").val(member);
    $("#edit-user-alias").val(alias);
    $("#edit-user-url").val(url);

    if (active === "True") {
      $("#edit-user-active").prop("checked", true);
    } else {
      $("#edit-user-active").prop("checked", false);
    }
  });

  $('[id^="view-button-user-"]').on("click", function () {
    const email = $(this).data("user-email");
    const role = $(this).data("user-role");
    const active = $(this).data("user-active");
    const member = $(this).data("user-member");
    const alias = $(this).data("user-alias");
    const created_at = $(this).data("user-created_at");

    $("#view-user-email").val(email);
    $("#view-user-role").val(role);
    $("#view-user-member").val(member);
    $("#view-user-alias").val(alias);

    if (active === "True") {
      $("#view-user-active").prop("checked", true);
    } else {
      $("#view-user-active").prop("checked", false);
    }

    const formattedDate = new Date(created_at).toLocaleDateString("es-ES", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
    $("#view-user-created-at").val(formattedDate);
  });

  $('[id^="approve-button-user-"]').on("click", function () {
    const url = $(this).data("url");
    $("#approve-user-url").val(url);
  });
});
