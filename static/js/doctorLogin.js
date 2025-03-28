localStorage.setItem('targetedLanguage', 'en');

let originalTexts = [];
let translatedTexts = [];

function collectInitialText() {
    originalTexts = [];
    document.querySelectorAll('[data-translate]').forEach(element => {
        originalTexts.push(element.textContent);
    });
}

function translateAllElements() {
    const selectedLanguage = document.getElementById('language-select').value;
    localStorage.setItem('targetedLanguage', selectedLanguage)

    if (selectedLanguage == 'en') {
        window.location.reload();
        return;
    }

    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texts: originalTexts,
            target_lang: selectedLanguage,
        }),
    })
    .then(response => response.json())
    .then(data => {
        translatedTexts = data.translated_texts || [];
        document.querySelectorAll('[data-translate]').forEach((element, index) => {
            element.textContent = translatedTexts[index] || '';
        });
    })
    .catch(error => {
        console.error('Translation error:', error);
    });
}

document.getElementById('language-select').addEventListener('change', function () {
    translateAllElements();
});

document.addEventListener('DOMContentLoaded', function() {
    collectInitialText();
});

function login_fun() {
    var username = document.getElementById("login-username").value;
    var password = document.getElementById("login-password").value;

    if (!username || !password) {
        alert("Username and password are required.");
        return false;
    }

    return true;
}

