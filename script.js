//index.js
console.log("window checking: ", typeof jQuery);
if (typeof jQuery === "undefined") {
  console.error("jQuery is required for components.js");
}

const hamburger = document.getElementById("hamburger");
const menu = document.querySelector(".menu");

try {
  hamburger.addEventListener("click", function () {
    const hamIcon = this.querySelector(".hamburger-icon");
    const crossIcon = this.querySelector(".cross-icon");
    if (hamIcon.style.display === "none") {
      hamIcon.style.display = "inline-block";
      menu.style.display = "none";
      crossIcon.style.display = "none";
    } else {
      crossIcon.style.display = "inline-block";
      hamIcon.style.display = "none";
      menu.style.display = "block";
    }
  });
} catch {}

const jucktype = (containerId, textToType, typingSpeed = 100) => {
  if (typeof $ === "undefined") {
    console.error("jQuery is required to use jucktype");
    return;
  }

  const $target = $(
    containerId.startsWith("#") ? containerId : `#${containerId}`
  );
  if (!$target.length) {
    console.error("Target container not found");
    return;
  }

  let index = 0;
  let isMistyped = false;
  let correctionIndex = 0;
  const random = "rqdsd";

  function type() {
    if (index < textToType.length) {
      if (index / textToType.length >= 2 / 3 && !isMistyped) {
        isMistyped = true;
        setTimeout(mistype, typingSpeed);
        return;
      }

      $target.append(textToType[index]);
      index++;
      setTimeout(type, typingSpeed);
    }
  }

  function mistype() {
    if (correctionIndex < random.length) {
      $target.append(random[correctionIndex]);
      correctionIndex++;
      setTimeout(mistype, typingSpeed);
    } else {
      correctMistake();
    }
  }

  function correctMistake() {
    if (correctionIndex > 0) {
      let content = $target.html();
      $target.html(content.slice(0, -1)); // Remove the last character
      correctionIndex--;
      setTimeout(correctMistake, typingSpeed);
    } else {
      // isMistyped = false;
      setTimeout(type, typingSpeed);
    }
  }

  type();
};

// const jucktype2 = (containerId, textToType) => {
//   if (typeof $ === "undefined") {
//     console.error("jQuery is required to use jucktype");
//     return;
//   }

//   console.log("props: ", containerId, textToType);
//   for (let i = 0; i < textToType.length; i++) {
//     setTimeout(function () {
//       console.log("char: ", textToType[i]);
//       $(containerId).append(textToType[i]);
//     }, 200 * i); // Multiply the delay by the index
//   }
// };

// const jucktype3 = (containerId, textToType) => {
//   if (typeof $ === "undefined") {
//     console.error("jQuery is required to use jucktype");
//     return;
//   }
//   console.log("props: ", containerId, textToType);
//   for (let i = 0; i < textToType.length; i++) {
//     console.log("char: ", textToType[i]);
//     setTimeout(function () {
//       $(containerId).append(textToType[i]);
//     }, 20);
//   }
// };
