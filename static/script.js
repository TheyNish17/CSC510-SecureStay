document.getElementById('bookingForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const resultBox = document.getElementById('bookingResult');
    const resultStatus = document.getElementById('resultStatus');
    const resultMessage = document.getElementById('resultMessage');
    const assignmentDetails = document.getElementById('assignmentDetails');

    try {
        const response = await fetch('/book', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Reveal the result box
        resultBox.classList.remove('hidden');

        if (data.status === "APPROVED") {
            resultBox.className = "result-box approved";
            resultStatus.innerText = "✅ Booking Approved!";
            resultMessage.innerText = data.message;
            
            // Show Room Assignation properties
            assignmentDetails.classList.remove('hidden');
            document.getElementById('assignedRoom').innerText = data.room_id;
            document.getElementById('assignedFloor').innerText = `Floor ${data.floor}`;

            // Real-time update grid values manually without refresh for beautiful UI experience
            setTimeout(() => {
                location.reload(); // Quick refresh to update the HTML sets beautifully
            }, 1800);
            
        } else {
            resultBox.className = "result-box denied";
            resultStatus.innerText = "❌ Booking Denied";
            resultMessage.innerText = data.message;
            assignmentDetails.classList.add('hidden');
        }

    } catch (error) {
        console.error("Submission error:", error);
        alert("Communications error connecting to host application.");
    }
});