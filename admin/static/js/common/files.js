$(document).ready(function () {
  const $addFileUploadContainer = $("#file-upload-container");
  const $addFileUploadButton = $("#add-file-upload");
  const $addLinkUploadButton = $("#add-link-upload");

  const $editFileUploadContainer = $("#edit-file-upload-container");
  const $editFileUploadButton = $("#edit-file-upload");
  const $editLinkUploadButton = $("#edit-link-upload");

  function addFileUploadItem(container) {
    const fileTypeOptions = fileTypes
      .map((fileType) => `<option value="${fileType}">${fileType}</option>`)
      .join("");
    const $fileUploadItem = $(`
      <div class="file-upload-item mb-4 flex space-x-4">
        <input type="text" name="file_name[]" placeholder="Nombre del archivo" required
               class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-1/3 p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <select name="file_type[]" required
                class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-1/3 p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          <option value="" selected>Seleccione el tipo</option>
          ${fileTypeOptions}
        </select>
        <input class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
               name="file_upload[]" type="file" accept="image/*,application/pdf" required>
        <button type="button" class="delete-file-upload text-red-600">✖</button>
      </div>
    `);

    container.append($fileUploadItem);
  }

  function addLinkUploadItem(container) {
    const fileTypeOptions = fileTypes
      .map((fileType) => `<option value="${fileType}">${fileType}</option>`)
      .join("");
    const $linkUploadItem = $(`
      <div class="link-upload-item mb-4 flex space-x-4">
        <input type="text" name="link_name[]" placeholder="Nombre del enlace" required
               class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-1/3 p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <select name="link_type[]" required
                class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-1/3 p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          <option value="" selected>Seleccione el tipo</option>
          ${fileTypeOptions}
        </select>
        <input class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
               name="link_url[]" type="url" placeholder="URL del enlace" required>
        <button type="button" class="delete-link-upload text-red-600">✖</button>
      </div>
    `);

    container.append($linkUploadItem);
  }

  $addFileUploadButton.on("click", function () {
    addFileUploadItem($addFileUploadContainer);
  });

  $addLinkUploadButton.on("click", function () {
    addLinkUploadItem($addFileUploadContainer);
  });

  $editFileUploadButton.on("click", function () {
    addFileUploadItem($editFileUploadContainer);
  });

  $editLinkUploadButton.on("click", function () {
    addLinkUploadItem($editFileUploadContainer);
  });

  $addFileUploadContainer.on("click", ".delete-file-upload", function () {
    $(this).closest(".file-upload-item").remove();
  });

  $addFileUploadContainer.on("click", ".delete-link-upload", function () {
    $(this).closest(".link-upload-item").remove();
  });

  $editFileUploadContainer.on("click", ".delete-file-upload", function () {
    $(this).closest(".file-upload-item").remove();
  });

  $editFileUploadContainer.on("click", ".delete-link-upload", function () {
    $(this).closest(".link-upload-item").remove();
  });
});

function updateFileUploadContainer(containerId, files, isViewMode) {
  $(containerId).empty();
  files.forEach(function (file) {
    const fileTypeOptions = fileTypes
      .map(
        (fileType) =>
          `<option value="${fileType}" ${
            file.type === fileType ? "selected" : ""
          }>${fileType}</option>`,
      )
      .join("");
    $(containerId).append(
      `<div class="file-upload-item mb-4 flex space-x-4">
          <input type="text" name="link_name[]" placeholder="Nombre del archivo" required value="${file.title}"
            class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-1/3 p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
          <select name="link_type[]" required
            class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-1/3 p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            <option value="" selected>Seleccione el tipo</option>
            ${fileTypeOptions}
          </select>
          <a href="${file.url}" download="${file.title}" class="inline-flex items-center justify-center p-5 text-base font-medium text-gray-500 rounded-lg bg-gray-50 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:bg-gray-800 dark:hover:bg-gray-700 dark:hover:text-white">
            <svg class="h-4 w-4 text-white" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
              <path d="M12.5535 16.5061C12.4114 16.6615 12.2106 16.75 12 16.75C11.7894 16.75 11.5886 16.6615 11.4465 16.5061L7.44648 12.1311C7.16698 11.8254 7.18822 11.351 7.49392 11.0715C7.79963 10.792 8.27402 10.8132 8.55352 11.1189L11.25 14.0682V3C11.25 2.58579 11.5858 2.25 12 2.25C12.4142 2.25 12.75 2.58579 12.75 3V14.0682L15.4465 11.1189C15.726 10.8132 16.2004 10.792 16.5061 11.0715C16.8118 11.351 16.833 11.8254 16.5535 12.1311L12.5535 16.5061Z" fill="white"/>
              <path d="M3.75 15C3.75 14.5858 3.41422 14.25 3 14.25C2.58579 14.25 2.25 14.5858 2.25 15V15.0549C2.24998 16.4225 2.24996 17.5248 2.36652 18.3918C2.48754 19.2919 2.74643 20.0497 3.34835 20.6516C3.95027 21.2536 4.70814 21.5125 5.60825 21.6335C6.47522 21.75 7.57754 21.75 8.94513 21.75H15.0549C16.4225 21.75 17.5248 21.75 18.3918 21.6335C19.2919 21.5125 20.0497 21.2536 20.6517 20.6516C21.2536 20.0497 21.5125 19.2919 21.6335 18.3918C21.75 17.5248 21.75 16.4225 21.75 15.0549V15C21.75 14.5858 21.4142 14.25 21 14.25C20.5858 14.25 20.25 14.5858 20.25 15C20.25 16.4354 20.2484 17.4365 20.1469 18.1919C20.0482 18.9257 19.8678 19.3142 19.591 19.591C19.3142 19.8678 18.9257 20.0482 18.1919 20.1469C17.4365 20.2484 16.4354 20.25 15 20.25H9C7.56459 20.25 6.56347 20.2484 5.80812 20.1469C5.07435 20.0482 4.68577 19.8678 4.40901 19.591C4.13225 19.3142 3.9518 18.9257 3.85315 18.1919C3.75159 17.4365 3.75 16.4354 3.75 15Z" fill="white"/>
            </svg>
            <span class="w-full">Descargar</span>
            <input value="${file.real_url}" class="hidden" name="link_url[]">
          </a>
          ${isViewMode ? "" : '<button type="button" class="delete-file-upload text-red-600">✖</button>'}
        </div>`,
    );
  });
}
