document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function () {
        // Function to fetch data and populate the reports
        function fetchAndRenderReports() {
            $.ajax({
                url: '/reports/job-and-profession-reports',
                method: 'GET',
                success: function (data) {
                    if (data.message) {
                        console.warn(data.message);
                        return;
                    }

                    const jobPositions = data.job_positions;
                    const professions = data.professions;

                    // Populate the Job Positions table
                    const jobPositionTableBody = $('#job-position-table-body');
                    jobPositionTableBody.empty();
                    jobPositions.forEach(item => {
                        jobPositionTableBody.append(`
                            <tr>
                                <td class="px-6 py-3">${item.job_position}</td>
                                <td class="px-6 py-3">${item.count}</td>
                            </tr>
                        `);
                    });

                    // Populate the Professions table
                    const professionTableBody = $('#profession-table-body');
                    professionTableBody.empty();
                    professions.forEach(item => {
                        professionTableBody.append(`
                            <tr>
                                <td class="px-6 py-3">${item.profession}</td>
                                <td class="px-6 py-3">${item.count}</td>
                            </tr>
                        `);
                    });
                },
                error: function (xhr) {
                    console.error("Error fetching data:", xhr.responseJSON.message || xhr.statusText);
                }
            });
        }

        // Fetch and render reports on page load
        fetchAndRenderReports();
    });
});
