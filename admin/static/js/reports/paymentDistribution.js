document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function () {
        const ctx = document.getElementById('payment-distribution-chart');
        const messageContainer = document.getElementById('message-container');  // Add a container for the message

        if (!ctx) {
            console.error("Canvas element not found!");
            return;
        }

        const chartCtx = ctx.getContext('2d');
        let chart;

        function fetchAndRenderChart(startDate, endDate) {
            $.ajax({
                url: `/reports/payments-distribution`,
                method: 'GET',
                data: {start_date: startDate, end_date: endDate},
                success: function (data) {
                    if (data.message && data.message === "No hay información disponible en este rango de fechas") {
                        // If no data is available, hide the chart and show the message
                        if (chart) chart.destroy();
                        messageContainer.style.display = 'block'; // Show the message container
                        messageContainer.innerHTML = `<p style="font-size: 24px; color: gray; text-align: center;">${data.message}</p>`;
                        ctx.style.display = 'none'; // Hide the canvas (chart)
                        return;
                    }

                    // Hide the message if data is available
                    messageContainer.style.display = 'none';
                    ctx.style.display = 'block'; // Show the canvas (chart)

                    const labels = data.map(item => item.type);
                    const amounts = data.map(item => item.total);

                    if (chart) chart.destroy();

                    chart = new Chart(chartCtx, {
                        type: 'pie',
                        data: {
                            labels,
                            datasets: [{
                                data: amounts,
                                backgroundColor: [
                                    'rgba(75, 192, 192, 0.6)',
                                    'rgba(255, 159, 64, 0.6)',
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(54, 162, 235, 0.6)',
                                    'rgba(153, 102, 255, 0.6)'
                                ]
                            }]
                        },
                        options: {
                            responsive: true,
                            aspectRatio: 1,
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    labels: {
                                        font: {
                                            size: 20
                                        }
                                    }
                                }
                            }
                        }
                    });
                },
                error: function (xhr) {
                    console.error("Error fetching data:", xhr.responseJSON.message || xhr.statusText);
                }
            });
        }

        // Initializing date range picker with default values (last 30 days)
        const today = new Date();
        const currentMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);  // First day of the current month
        const currentMonthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);  // Last day of the current month

        // Convert dates to dd/mm/yyyy format for the input fields
        const formatDate = (date) => {
            const day = ("0" + date.getDate()).slice(-2); // Ensure 2 digits for day
            const month = ("0" + (date.getMonth() + 1)).slice(-2); // Ensure 2 digits for month
            const year = date.getFullYear();
            return `${day}/${month}/${year}`;
        };

        // Format the dates as dd/mm/yyyy
        const startDate = formatDate(currentMonthStart);
        const endDate = formatDate(currentMonthEnd);

        // Set the values of the datepicker inputs
        $('#datepicker-range-start').val(startDate);
        $('#datepicker-range-end').val(endDate);

        // Fetch data and render chart for the current month
        fetchAndRenderChart(startDate, endDate);

        // Event listener for the date range picker (start and end date fields)
        $('#date-filter-form').on('submit', function (event) {
            event.preventDefault();

            // Get the selected start and end dates from the input fields
            const startDate = $('#datepicker-range-start').val();
            const endDate = $('#datepicker-range-end').val();

            // If both dates are selected, fetch and render the chart
            if (startDate && endDate) {
                fetchAndRenderChart(startDate, endDate);
            } else {
                console.error("Both start and end dates are required.");
            }
        });
    });
});
