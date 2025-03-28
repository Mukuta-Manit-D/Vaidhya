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
        window.location.reload()
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

function docappointment_get() {
    var formData = {
        date: document.getElementById('calendarDate').value,
        timeSlots: [],
        customTimeSlot: {}
    };

    var checkboxes = document.querySelectorAll('.checkbox-input-container input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            formData.timeSlots.push(checkbox.labels[0].textContent);
        }
    });
    var customTimeSlotFrom = document.getElementById('timea').value;
    var customTimeSlotTo = document.getElementById('timeb').value;

    if (customTimeSlotFrom && customTimeSlotTo) {
        formData.customTimeSlot = {
            from: customTimeSlotFrom,
            to: customTimeSlotTo
        };
    }


    var jsonData = JSON.stringify(formData);


    fetch('/docappointment/submitted', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: jsonData,
    })
    .then(response => response.json()) 
    .then(data => {
        alert(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
  

    return false;
}


function handleResize() {
    if (window.innerWidth < 768) {
        console.log('Mobile view');
    } else {
        console.log('PC view');
    }
}

handleResize();

window.addEventListener('resize', handleResize);if (localStorage.getItem('targetedLanguage') != 'en') {

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
        window.location.reload()
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

function docappointment_get() {
    var formData = {
        date: document.getElementById('calendarDate').value,
        timeSlots: [],
        customTimeSlot: {}
    };

    var checkboxes = document.querySelectorAll('.checkbox-input-container input[type="checkbox"]');
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            formData.timeSlots.push(checkbox.labels[0].textContent);
        }
    });
    var customTimeSlotFrom = document.getElementById('timea').value;
    var customTimeSlotTo = document.getElementById('timeb').value;

    if (customTimeSlotFrom && customTimeSlotTo) {
        formData.customTimeSlot = {
            from: customTimeSlotFrom,
            to: customTimeSlotTo
        };
    }


    var jsonData = JSON.stringify(formData);


    fetch('/docappointment/submitted', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: jsonData,
    })
    .then(response => response.json()) 
    .then(data => {
        alert(data.message);
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
  

    return false;
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