/* Use the exported functions to call the API.
 * If necessary, adjust the backend address below:
 */
const backend = "http://localhost:8080";

export function predict() {
  return postJson("/predict").then(parseJSON);
}

export function getGlassContainers() {
  return getJson("/glasscontainers").then(parseJSON);
}

export function getGlassContainer(id) {
  return getJson("/glasscontainers/" + id).then(parseJSON);
}

export function getGlassContainerHistory(id) {
  return getJson("/glasscontainers/" + id + "/history").then(parseJSON);
}

export function getGlassContainerPrediction(id) {
  return getJson("/glasscontainers/" + id + "/prediction").then(parseJSON);
}

// helper functions
function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  } else {
    const error = new Error(response.statusText);
    error.response = response;
    throw error;
  }
}

function parseJSON(response) {
  return response.json();
}

function postJson(endpoint, params) {
  return fetch(`${backend}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(params),
  }).then(checkStatus);
}
