document.getElementById('bookingForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const resultBox = document.getElementById('bookingResult');
    const resultStatus = document.getElementById('resultStatus');
    const resultMessage = document.getElementById('resultMessage');
    const assignmentDetails = document.getElementById('assignmentDetails');

    // Extract the requested room type from the form for metric tracking
    const chosenRoomType = formData.get('room_type'); 

    try {
        const response = await fetch('/book', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        resultBox.classList.remove('hidden');

        if (data.status === "APPROVED") {
            resultBox.className = "result-box approved";
            resultStatus.innerText = "Booking Approved!";
            resultMessage.innerText = data.message;
            
            assignmentDetails.classList.remove('hidden');
            document.getElementById('assignedRoom').innerText = data.room_id;
            document.getElementById('assignedFloor').innerText = `Floor ${data.floor}`;

            // --- 1. DYNAMIC GRID CARD STATE UPDATE ---
            const roomCards = document.querySelectorAll('.room-card');
            let cardTarget = null;

            roomCards.forEach(card => {
                const roomIdElement = card.querySelector('.room-id');
                if (roomIdElement && roomIdElement.innerText.includes(data.room_id)) {
                    if (card.classList.contains('vacant')) {
                        card.classList.remove('vacant');
                        card.classList.add('occupied');
                        cardTarget = card;
                        
                        const indicator = card.querySelector('.status-indicator');
                        if (indicator) indicator.innerText = "Occupied";
                    }
                }
            });

            // --- 2. DYNAMIC LIVE BANNER METRICS RECALCULATION ---
            if (cardTarget) {
                // A. Update Global Stats
                const globalValElement = document.querySelector('.metric-card.global .metric-value');
                const globalRateElement = document.querySelector('.metric-card.global .metric-sub');
                
                if (globalValElement) {
                    let [occupied, total] = globalValElement.innerText.split('/').map(num => parseInt(num.trim()));
                    occupied += 1;
                    globalValElement.innerText = `${occupied} / ${total}`;
                    
                    if (globalRateElement && total > 0) {
                        const newRate = ((occupied / total) * 100).toFixed(1);
                        globalRateElement.innerText = `Global Rate: ${newRate}%`;
                    }
                }

                // B. Update Inventory Breakdown by Type
                const typeLabels = document.querySelectorAll('.metric-card.breakdown .metric-list div');
                typeLabels.forEach(div => {
                    if (div.innerText.toLowerCase().includes(chosenRoomType.toLowerCase())) {
                        const strongTag = div.querySelector('strong');
                        if (strongTag) {
                            let [tOcc, tTot] = strongTag.innerText.split('/').map(num => parseInt(num.trim()));
                            tOcc += 1;
                            strongTag.innerText = `${tOcc}/${tTot}`;
                        }
                    }
                });

                // C. Update Capacity by Level
                const floorLabels = document.querySelectorAll('.metric-card.floors .metric-list div');
                floorLabels.forEach(div => {
                    if (div.innerText.toLowerCase().includes(`floor ${data.floor}`)) {
                        const strongTag = div.querySelector('strong');
                        if (strongTag) {
                            let vacantCount = parseInt(strongTag.innerText);
                            if (!isNaN(vacantCount) && vacantCount > 0) {
                                vacantCount -= 1;
                                strongTag.innerText = `${vacantCount} vacant`;
                            }
                        }
                    }
                });
            }

            this.reset();
            
        } else {
            resultBox.className = "result-box denied";
            resultStatus.innerText = "Booking Denied";
            resultMessage.innerText = data.message;
            assignmentDetails.classList.add('hidden');
        }

    } catch (error) {
        console.error("Submission error:", error);
        alert("Communications error connecting to host application.");
    }
});

document.getElementById('btnReset').addEventListener('click', async function() {
    if (confirm("Are you sure you want to clear all bookings and reset the grid?")) {
        try {
            const response = await fetch('/reset-inventory', { method: 'POST' });
            const data = await response.json();
            if (data.status === "SUCCESS") {
                // Instantly refresh the view back to clean state
                window.location.reload();
            }
        } catch (error) {
            console.error("Failed to reset inventory tracker:", error);
        }
    }
});