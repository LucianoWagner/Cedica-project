document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function () {
        const wordcloudContainer = document.getElementById('wordcloud-container');
        const wordcloudMessageContainer = document.getElementById('wordcloud-message-container');

        // Function to fetch and render the word cloud
        function fetchAndRenderWordCloud(startDate, endDate) {
            // Clear word cloud container and message before each request
            wordcloudContainer.innerHTML = '';  // Clear previous word cloud
            wordcloudMessageContainer.style.display = 'none';  // Hide message
            wordcloudContainer.style.display = 'none';  // Hide word cloud

            $.ajax({
                url: `/reports/wordcloud-data`, // URL for word cloud data
                method: 'GET',
                data: {start_date: startDate, end_date: endDate}, // Date parameters for the request
                success: function (data) {
                    // Handle the case when there is no data
                    if (!data.length) {
                        wordcloudMessageContainer.textContent = "No hay datos disponibles para este período.";
                        wordcloudMessageContainer.style.display = 'block'; // Show message
                        wordcloudContainer.style.display = 'none'; // Hide word cloud
                        return;
                    }

                    wordcloudMessageContainer.style.display = 'none'; // Hide message
                    wordcloudContainer.style.display = 'block'; // Show word cloud

                    WordCloud(wordcloudContainer, {
                        list: data.map(item => [item.text, item.weight]),
                        gridSize: 10, // Smaller grid size to fit more words
                        weightFactor: 10, // Increased weight factor to make smaller words more visible
                        fontFamily: 'Roboto, Arial, sans-serif',
                        color: 'random-dark',
                        backgroundColor: '#f9f9f9',
                        rotateRatio: 0, // Prevent word rotation, keep all horizontal
                        minSize: 8, // Minimum size of the words
                        maxSize: 80, // Maximum size of the words
                        drawOutOfBound: false, // Avoid words being drawn outside the canvas area
                        minWeight: 1, // Ensure words with weight 1 are visible
                    });
                },
                error: function (xhr) {
                    console.error("Error fetching word cloud data:", xhr.responseJSON?.message || xhr.statusText);
                    wordcloudMessageContainer.textContent = "Error al cargar los datos."; // Error message
                    wordcloudMessageContainer.style.display = 'block'; // Show error message
                    wordcloudContainer.style.display = 'none'; // Hide word cloud
                }
            });
        }

        // Initialize the date pickers with default values (last 30 days)
        const today = new Date();
        const lastMonth = new Date(today);
        lastMonth.setDate(today.getDate() - 30);

        const formatDate = (date) => {
            const day = ("0" + date.getDate()).slice(-2);
            const month = ("0" + (date.getMonth() + 1)).slice(-2);
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        };

        // Set default date values for the start and end date fields
        $('#wordcloud-datepicker-range-start').val(formatDate(lastMonth));
        $('#wordcloud-datepicker-range-end').val(formatDate(today));

        // Fetch and render the word cloud with default dates
        fetchAndRenderWordCloud(formatDate(lastMonth), formatDate(today));

        // Form submission handler
        $('#wordcloud-date-filter-form').on('submit', function (event) {
            event.preventDefault(); // Prevent the form from submitting normally

            // Get the selected start and end dates from the input fields
            const startDate = $('#wordcloud-datepicker-range-start').val();
            const endDate = $('#wordcloud-datepicker-range-end').val();

            // Debugging: Log the input values to make sure they are updated
            console.log('Start Date:', startDate);
            console.log('End Date:', endDate);

            // If both dates are selected, fetch and render the word cloud
            if (startDate && endDate) {
                fetchAndRenderWordCloud(startDate, endDate);
            } else {
                console.error("Start and end dates are required.");
                wordcloudMessageContainer.textContent = "Por favor, seleccione ambas fechas.";
                wordcloudMessageContainer.style.display = 'block';
                wordcloudContainer.style.display = 'none';
            }
        });
    });
});
