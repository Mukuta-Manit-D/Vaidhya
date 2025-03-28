if (localStorage.getItem("targetedLanguage") !== "en") {
  let originalEnglishText = [];
  let translatedText = [];

  function collectInitialText() {
      originalEnglishText = [];
      document.querySelectorAll("[data-translate]").forEach((element) => {
          originalEnglishText.push(element.textContent);
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
      collectInitialText();
      translateAllElements();
  });

  async function translateAllElements() {
      const selectedLanguage = localStorage.getItem("targetedLanguage");
      
      if (selectedLanguage === "en") {
          document.querySelectorAll("[data-translate]").forEach((element, index) => {
              element.textContent = originalEnglishText[index];
          });
          return;
      }

      localStorage.setItem("targetedLanguage", selectedLanguage);

      try {
          const response = await fetch("/translate", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ texts: originalEnglishText, target_lang: selectedLanguage }),
          });

          if (!response.ok) {
              throw new Error("Translation API failed");
          }

          const data = await response.json();
          translatedText = data.translated_texts || [];

          document.querySelectorAll("[data-translate]").forEach((element, index) => {
              element.textContent = translatedText[index] || originalEnglishText[index] || "Translation error";
          });

      } catch (error) {
          console.error("Translation error:", error);
      }
  }
}


const hamMenuBtn = document.querySelector(".header__main-ham-menu-cont");
const smallMenu = document.querySelector(".header__sm-menu");
const headerHamMenuBtn = document.querySelector(".header__main-ham-menu");
const headerHamMenuCloseBtn = document.querySelector(
  ".header__main-ham-menu-close"
);
const headerSmallMenuLinks = document.querySelectorAll(".header__sm-menu-link");

hamMenuBtn.addEventListener("click", () => {
  if (smallMenu.classList.contains("header__sm-menu--active")) {
    smallMenu.classList.remove("header__sm-menu--active");
  } else {
    smallMenu.classList.add("header__sm-menu--active");
  }
  if (headerHamMenuBtn.classList.contains("d-none")) {
    headerHamMenuBtn.classList.remove("d-none");
    headerHamMenuCloseBtn.classList.add("d-none");
  } else {
    headerHamMenuBtn.classList.add("d-none");
    headerHamMenuCloseBtn.classList.remove("d-none");
  }
});
async function contactFormSubmission(form) {
  console.log(form.name.value);
  const params = {
    email: form.email.value,
    name: form.name.value,
    message: form.message.value,
  };
  const options = {
    method: "POST",
    body: JSON.stringify(params),
  };
  fetch("http://localhost:8080/upload-contact", {
    mode: "cors",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });
}
for (let i = 0; i < headerSmallMenuLinks.length; i++) {
  headerSmallMenuLinks[i].addEventListener("click", () => {
    smallMenu.classList.remove("header__sm-menu--active");
    headerHamMenuBtn.classList.remove("d-none");
    headerHamMenuCloseBtn.classList.add("d-none");
  });
}

const headerLogoConatiner = document.querySelector(".header__logo-container");

headerLogoConatiner.addEventListener("click", () => {
  location.href = "index.html";
});

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function () {
    this.classList.toggle("active");
    this.parentElement.classList.toggle("active");

    var pannel = this.nextElementSibling;

    if (pannel.style.display === "block") {
      pannel.style.display = "none";
    } else {
      pannel.style.display = "block";
    }
  });
}


function sendEmail() {
  var name = document.getElementById("name").value;
  var email = document.getElementById("email").value;
  var message = document.getElementById("message").value;

  if (!name) {
    alert("Name is Required");
    return false;
  }

  if (!email) {
    alert("Email is Required");
    return false;
  }

  if (!message) {
    alert("Message is Required");
    return false;
  }

  var messageFromServer = "Thank you for contacting us, we will be reaching you soon !";
  alert(messageFromServer);
  return true;
}



