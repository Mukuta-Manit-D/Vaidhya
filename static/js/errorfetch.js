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