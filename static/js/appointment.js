var selectedDate = null;

if (localStorage.getItem('targetedLanguage') != 'en') {
    let originalEnglishText = [];
    let translatedText = [];

    function collectInitialText() {
        originalEnglishText = [];
        document.querySelectorAll('[data-translate]').forEach(element => {
            originalEnglishText.push(element.textContent);
        });
    }
    collectInitialText();

    function translateAllElements() {
        const selectedLanguage = localStorage.getItem('targetedLanguage');
        if (selectedLanguage === 'en') {
            window.location.reload();
        }
        sessionStorage.setItem('targetedLanguage', selectedLanguage);
        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                texts: originalEnglishText,
                target_lang: selectedLanguage,
            }),
        })
            .then(response => response.json())
            .then(data => {
                translatedText = data.translated_texts || [];
                document.querySelectorAll('[data-translate]').forEach((element, index) => {
                    element.textContent = translatedText[index] || '';
                });
            })
            .catch(error => {
                console.error('Translation error:', error);
            });
    }
    translateAllElements();
}

function opentime(evt, date) {
    var i, tabcontent, tablinks;
    selectedDate = date;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(date).style.display = "block";
    evt.currentTarget.className += " active";
}

function appointment_get(date) {
    // Get form field values
    var name = document.getElementById("name_" + date).value.trim();
    var pid = document.getElementById("pid_" + date).value.trim();
    var timeSlot = document.querySelector('input[name="timeSlot"]:checked');
    var mode = document.querySelector('input[name="mode"]:checked');

    // Debugging logs
    console.log("Name:", name);
    console.log("PID:", pid);
    console.log("Time Slot:", timeSlot ? timeSlot.value : "None selected");
    console.log("Mode:", mode ? mode.value : "None selected");

    // Validate required fields
    if (!name || !pid || !timeSlot || !mode) {
        const errorMessage = "Please fill all required fields.";
        console.error(errorMessage);
        document.getElementById("error-message").textContent = errorMessage;
        document.getElementById("error-message").style.display = "block";
        return false; // Prevent form submission
    }

    // Clear any previous error messages
    document.getElementById("error-message").style.display = "none";

    // Prepare data for submission
    var data = {
        name: name,
        pid: pid,
        timeSlot: timeSlot.value,
        mode: mode.value,
        dates: date,
    };

    // Debugging log for data
    console.log("Data to be submitted:", data);

    // Send data using fetch
    fetch('/appointment/submitted', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to submit appointment.");
            }
            return response.json();
        })
        .then(data => {
            console.log("Response from server:", data);
            alert(data.message || "Appointment submitted successfully!");
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = "An error occurred while submitting the appointment.";
            document.getElementById("error-message").textContent = errorMessage;
            document.getElementById("error-message").style.display = "block";
        });

    return false; // Prevent default form submission
}

function handleResize() {
    if (window.innerWidth < 768) {
        console.log('Mobile view');
    } else {
        console.log('PC view');
    }
}

handleResize();
window.addEventListener('resize', handleResize);