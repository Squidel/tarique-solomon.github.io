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

  let $target = $(containerId);
  let index = 0;

  function type() {
    if (index < textToType.length) {
      $target.append(textToType[index]);
      index++;
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
