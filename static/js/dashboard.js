// Dashboard functionality
(function() {
    // Initialize trends chart
    if (typeof chartData !== 'undefined' && document.getElementById('trends-chart')) {
        try {
            const chartDataObj = typeof chartData === 'string' ? JSON.parse(chartData) : chartData;
            const ctx = document.getElementById('trends-chart').getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartDataObj.dates || [],
                    datasets: [
                        {
                            label: 'Sessions',
                            data: chartDataObj.sessions || [],
                            borderColor: '#3498db',
                            backgroundColor: 'rgba(52, 152, 219, 0.1)',
                            tension: 0.4
                        },
                        {
                            label: 'Anxiety Keywords',
                            data: chartDataObj.anxiety || [],
                            borderColor: '#e74c3c',
                            backgroundColor: 'rgba(231, 76, 60, 0.1)',
                            tension: 0.4
                        },
                        {
                            label: 'Depression Keywords',
                            data: chartDataObj.depression || [],
                            borderColor: '#9b59b6',
                            backgroundColor: 'rgba(155, 89, 182, 0.1)',
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } catch (e) {
            console.error('Error initializing chart:', e);
        }
    }

    // Update appointment status
    window.updateAppointment = async function(appointmentId, status) {
        if (!confirm(`Are you sure you want to mark this appointment as ${status}?`)) {
            return;
        }

        try {
            // Use authenticated fetch if Auth utility is available
            let response;
            if (typeof Auth !== 'undefined' && Auth.isAuthenticated()) {
                response = await Auth.authenticatedFetch(`/api/appointments/${appointmentId}/update/`, {
                    method: 'POST',
                    body: JSON.stringify({
                        status: status
                    })
                });
            } else {
                // Fallback to regular fetch (session-based)
                response = await fetch(`/api/appointments/${appointmentId}/update/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        status: status
                    })
                });
            }

            const data = await response.json();

            if (response.ok) {
                alert('Appointment updated successfully!');
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'Failed to update appointment'));
            }
        } catch (error) {
            alert('Connection error. Please try again.');
            console.error('Error:', error);
        }
    };
})();

