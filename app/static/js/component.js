console.log("window checking: ", typeof jQuery);
if (typeof jQuery === "undefined") {
  console.error("jQuery is required for components.js");
}

console.log("window checking: ", typeof Chart);
if (typeof Chart === "undefined") {
  console.error("Chart.js is required for chart components");
}

function addCard(
  containerId,
  title,
  value,
  variance,
  imgUrl,
  subtext,
  url = null
) {
  if (typeof $ === "undefined") {
    console.error("jQuery is required to use addCard");
    return;
  }
  const cardHtml = `
              <div class="p-3">
              <a class="card-anchor" href="${url}"target="_blank">
                <div class="card-parent rounded py-5 px-3">
                  <div class="d-inline-flex align-items-center ms-md-3 mb-4">
                      <h3 class="card-title fw-bold mb-0">${title}</h3>
                      <i style="color: #3d3d3d" class="fa-solid fa-circle-info ms-2"></i>
                  </div>
                  <div class="d-flex flex-column">
                      <div class="d-flex flex-column mb-3">
                          <div class="ms-md-3 mb-md-4">
                              <p class="value truncate-multiline">${value}</p>
                          </div>
                          <div class="ms-md-3 mb-md-4">
                          ${
                            variance
                              ? `<div class="variance-container rounded-5 py-1 px-4">
                                    <h6 class="d-inline">${variance}</h6>
                                </div>`
                              : ``
                          }
                          ${
                            subtext
                              ? `<div class="subtext-container py-1 px-4">
                                    <p class="d-inline">${subtext}</p>
                                </div>`
                              : ``
                          }
                              
                          </div>
                      </div>
                      <div class="d-block">
                        <img src="${imgUrl}" alt="chart-placeholder" class="h-100 rounded">
                      </div>
                  </div>
                </div>
                </a>
            </div>
            `;

  // Append the card to the specified container
  $(containerId).append(cardHtml);
}

function addCardWithChart(
  containerId,
  title,
  value,
  variance,
  chartData,
  chartType = "doughnut",
  subtext
) {
  if (typeof Chart === "undefined") {
    console.error("Chart.js is required to use addCardWithChart");
    return;
  }
  const cardId = `chart-${Math.random().toString(36).substr(2, 9)}`;
  const cardHtml = `
              <div class="p-3">
                <div class="card-parent rounded py-5 px-3">
                  <div class="d-inline-flex align-items-center ms-md-3 mb-4">
                      <h3 class="card-title fw-bold mb-0">${title}</h3>
                      <i style="color: #3d3d3d" class="fa-solid fa-circle-info ms-2"></i>
                  </div>
                  <div class="row">
                      <div class="d-flex flex-column justify-content-center col-md-4 mb-3">
                          <div class="ms-md-3 mb-md-4">
                              <h1 class="value">${value}</h1>
                          </div>
                          <div class="ms-md-3 mb-md-4">
                          ${
                            variance
                              ? `<div class="variance-container rounded-5 py-1 px-4">
                                    <h6 class="d-inline">${variance}</h6>
                                </div>`
                              : ``
                          }
                              ${
                                subtext
                                  ? `<div class="subtext-container py-1 px-4">
                                    <p class="d-inline">${subtext}</p>
                                </div>`
                                  : ``
                              }
                              
                          </div>
                      </div>
                      <div class="col-md-8">
                         <canvas id="${cardId}" class="w-100 rounded card-chart"></canvas>
                      </div>
                  </div>
                </div>
            </div>
            `;

  // Append the card to the specified container
  $(containerId).append(cardHtml);

  const ctx = document.getElementById(cardId).getContext("2d");
  new Chart(ctx, {
    type: chartType,
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
    },
  });
}

const getCardImages = (cardGraphic) => {
  switch (cardGraphic) {
    case "contracted":
      return "https://media.istockphoto.com/id/1973365581/vector/sample-ink-rubber-stamp.webp?s=2048x2048&w=is&k=20&c=-nRicEMFco-wjZrqf2MTWa5dlmVM312tNFy7Mw3Rj4I=";
      break;
    case "disbursement":
      return "https://media.istockphoto.com/id/1973365581/vector/sample-ink-rubber-stamp.webp?s=2048x2048&w=is&k=20&c=-nRicEMFco-wjZrqf2MTWa5dlmVM312tNFy7Mw3Rj4I=";
      break;
    default:
      return "https://media.istockphoto.com/id/1973365581/vector/sample-ink-rubber-stamp.webp?s=2048x2048&w=is&k=20&c=-nRicEMFco-wjZrqf2MTWa5dlmVM312tNFy7Mw3Rj4I=";
      break;
  }
};

function generateComponent(
  container,
  lineItems,
  showfigure = false,
  title = "Running Projects",
  hasMultiple = false,
  linkToMore = null
) {
  // Create the card structure
  const card = $(`
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title">${title}</h5>
            ${
              hasMultiple
                ? `
            <div class="dropdown">
              <button class="btn btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                Disbursement Info
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Option 1</a></li>
                <li><a class="dropdown-item" href="#">Option 2</a></li>
              </ul>
            </div>`
                : ""
            }
          </div>
          <div class="card-body">
            <ul class="project-list"></ul>
          </div>
          ${
            linkToMore
              ? `
          <div class="card-footer text-center">
            <a href="#" class="btn btn-link">Show all projects</a>
          </div>
        </div>`
              : ""
          }
      `);

  // Loop through the line items and add them to the card
  lineItems.forEach((item) => {
    console.log("line items: ", item);

    const projectIconColor = getRandomHexColor(); // Generate random color for icon

    const maxNameLength = 15; // Set a character limit
    const displayName =
      item.name.length > maxNameLength
        ? item.name.substring(0, maxNameLength) + "..."
        : item.name;
    const tooltip =
      item.name.length > maxNameLength ? `title="${item.name}"` : "";

    const listItem = $(`
          <li class="project-item d-flex align-items-center">
           <div class="project-icon" style="background-color: ${projectIconColor};">
            ${
              item.icon
                ? `<i class="${item.icon}" aria-hidden="true"></i>`
                : item.name.charAt(0).toUpperCase()
            }
            </div>
            <div class="project-details">
                <h6 ${tooltip}>${displayName} 
                ${
                  showfigure
                    ? `<span title="the disbursement completion percentage" class="badge bg-primary disbursement-completion-percentage">${item.percentage.toFixed(
                        2
                      )}%</span>`
                    : ""
                }
                </h6>
            </div>
           ${
             showfigure
               ? `<div class="project-time">$${item.dollarValue.toLocaleString()}</div>`
               : ""
           }
            <div class="progress-bar-container">
              <div class="progress">
                <div title="the disbursement completion percentage" class="progress-bar bg-primary" style="width: ${item.percentage.toFixed(
                  2
                )}%;"></div>
              </div>
            </div>
          </li>
        `);

    card.find(".project-list").append(listItem);
  });

  // Append the card to the specified container
  $(container).append(card);
}

const runningProjects = (container, lineItems, showfigure) => {
  var RPBody = $(`
    <div class="p-3">
          <div id="running-projects-card" class="card-parent rounded-3">
            <div
              class="d-inline-flex justify-content-between align-items-center w-100 px-5 py-3 card-header rounded-top-3"
            >
              <div id="card-title-container">
                <h5 id="card-title" class="mb-0">Running Projects</h5>
              </div>
              ${
                showfigure
                  ? ` <div id="filter" class="dropdown">
                <button
                  class="btn btn-secondary dropdown-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Working Time
                </button>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#">Action</a></li>
                  <li><a class="dropdown-item" href="#">Another action</a></li>
                  <li>
                    <a class="dropdown-item" href="#">Something else here</a>
                  </li>
                </ul>
              </div>`
                  : ""
              }
            </div>

            <div id="card-body" class="d-flex flex-column py-3">

            </div>

             ${
               showfigure
                 ? `<div class="card-footer d-flex justify-content-center px-5 py-3">
              <a class="cs-next text-decoration-none" href="#"
                >Show all projects<i class="fa-solid fa-arrow-right ms-2"></i
              ></a>
            </div>`
                 : ""
             }
          </div>
        </div>
        `);
  lineItems.forEach((item) => {
    value = Math.max(0, Math.min(100, item.percentage));
    let els = $(`              <div id ="rp-data"
                class="d-flex justify-content-around py-3 border-bottom border-primary-subtle rp-data"
              >
                <div class="d-inline-flex align-items-center col-5">
                  <img
                    id="cs-thumbnail"
                    class="img-thumbnail rounded-5 p-3"
                    src="${item.icon}"
                    alt="thumbnail"
                  />
                  <h6 class="card-title ms-3">${item.name}</h6>
                  ${
                    item.variance
                      ? `<div id="variance-container" class="rounded-5 ms-3 py-1 px-4">
                    <h6 id="variance" class="d-inline">${item.variance}</h6>
                  </div>`
                      : ""
                  }
                </div>

                <div class="d-inline-flex align-items-center col-5">
                  ${
                    item.value
                      ? `<h5 class="time-elapsed mb-0">${item.value}</h5>`
                      : ""
                  }
                  <div class="progress-container ms-3">
                    <div class="progress-bar" style="width:${value}%" id="progress-bar"></div>
                  </div>
                </div>
              </div>`);
    RPBody.find("#card-body").append(els);
  });
  $(container).append(RPBody);
};

const getRandomHexColor = () => {
  const hue = Math.floor(Math.random() * 360);
  const pastelColor = `hsl(${hue}, 70%, 85%)`;
  return pastelColor;
};

function abbreviateNumber(numberString) {
  console.log("called abbreviate number: ", numberString);
  let number = parseFloat(numberString);
  console.log("number: ", number);
  if (isNaN(number)) return numberString;

  if (number >= 1_000_000_000) return (number / 1_000_000_000).toFixed(1) + "B";
  if (number >= 1_000_000) return (number / 1_000_000).toFixed(1) + "M";
  if (number >= 1_000) return (number / 1_000).toFixed(1) + "K";

  return number.toFixed(0);
}
