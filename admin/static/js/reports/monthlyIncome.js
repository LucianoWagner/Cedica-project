document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function () {
        const ctx = document.getElementById('monthly-income-chart').getContext('2d');
        let chart;

        function fetchAndRenderChart(startMonth, startYear, endMonth, endYear) {
            $.ajax({
                url: `/reports/monthly-income`,
                method: 'GET',
                data: {start_month: startMonth, start_year: startYear, end_month: endMonth, end_year: endYear},
                success: function (data) {
                    if (chart) chart.destroy();

                    if (!data.length) {
                        console.warn("No data available for the selected range.");
                        $('#lines-message-container')
                            .text('No hay datos disponibles para este período')
                            .show();
                        return;
                    } else
                        $('#lines-message-container').hide();

                    const labels = data.map(item => item.month); // Directly use the month from the response

                    const amounts = data.map(item => item.total);
                    chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels,
                            datasets: [{
                                label: 'Ingresos Mensuales',
                                data: amounts,
                                borderColor: 'rgba(54, 162, 235, 1)',
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                fill: true,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    display: true,
                                    position: 'top'
                                }
                            },
                            scales: {
                                x: {
                                    title: {
                                        display: true,
                                        text: 'Meses'
                                    }
                                },
                                y: {
                                    title: {
                                        display: true,
                                        text: 'Ingresos'
                                    }
                                }
                            }
                        }
                    });
                },
                error: function (xhr) {
                    console.error("Error fetching data:", xhr.responseJSON?.message || xhr.statusText);

                    // Hide the chart canvas
                    $('#monthly-income-chart').hide();

                    // Show error message in a dedicated container
                    $('#message-container')
                        .text('Rango de fechas inválido')
                        .addClass('text-red-600 text-xl font-bold text-center')
                        .show();
                }
            });
        }

        function validateDates() {
            const startMonth = parseInt($('#start-month').val());
            const startYear = parseInt($('#start-year').val());
            const endMonth = parseInt($('#end-month').val());
            const endYear = parseInt($('#end-year').val());

            if (startYear > endYear) {
                $('#end-year').val(startYear);
            } else if (startYear === endYear && startMonth > endMonth) {
                $('#end-month').val(startMonth);
            }

            return {
                startMonth,
                startYear,
                endMonth: parseInt($('#end-month').val()),
                endYear: parseInt($('#end-year').val())
            };
        }

        // Set defaults for current year and months
        const currentYear = new Date().getFullYear();
        $('#start-month').val(1); // January
        $('#start-year').val(currentYear);
        $('#end-month').val(12); // December
        $('#end-year').val(currentYear);

        // Fetch chart data with default values on page load
        fetchAndRenderChart(1, currentYear, 12, currentYear);

        $('#apply-dates-button').on('click', function () {
            const {startMonth, startYear, endMonth, endYear} = validateDates();

            if (startYear && endYear && startMonth && endMonth) {
                fetchAndRenderChart(startMonth, startYear, endMonth, endYear);
            } else {
                console.error("Please provide valid dates.");
            }
        });
    });
});
