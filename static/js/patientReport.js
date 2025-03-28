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


function fetchdetails(){
    var patientid = document.getElementById("patientid").value;
    var key = document.getElementById("key").value;

    if (!patientid || !key) {
        alert("Username and password are required.");
        return false;
    }

    return true;
}


function downloadReport(name, pid, age, sfeel, stest, docid, docname) {
    var url = '/generatereport?' +
        'name=' + encodeURIComponent(name) +
        '&pid=' + encodeURIComponent(pid) +
        '&age=' + encodeURIComponent(age) +
        '&sfeel=' + encodeURIComponent(sfeel) +
        '&stest=' + encodeURIComponent(stest) +
        '&docid=' + encodeURIComponent(docid) +
        '&docname=' + encodeURIComponent(docname);
    window.location.href = url;
}





