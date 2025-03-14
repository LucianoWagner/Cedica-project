$(document).ready(function () {
    function fetchJyasBehindPayments() {
        const url = "/reports/behind-payments";

        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                const tableBody = $("#behind-payment-table-body");
                tableBody.empty();

                if (response.length === 0) {
                    const noDataRow = `
                        <tr>
                            <td colspan="6" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                                No hay J&As en deuda.
                            </td>
                        </tr>`;
                    tableBody.append(noDataRow);
                    return;
                }

                response.forEach(jya => {
                    const row = `
                        <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                            <td class="px-6 py-4">${jya.dni}</td>
                            <td class="px-6 py-4">${jya.name}</td>
                            <td class="px-6 py-4">${jya.surname}</td>
                            <td class="px-6 py-4">${jya.age}</td>
                            <td class="px-6 py-4">${jya.telephone || "N/A"}</td>
                            <td class="px-6 py-4">${jya.address || "N/A"}</td>
                        </tr>`;
                    tableBody.append(row);
                });
            },
            error: function () {
                console.error("Error fetching J&As behind payment.");
            }
        });
    }

    // Initial fetch when page loads
    fetchJyasBehindPayments();
});
