/* Use the exported functions to call the API.
 * If necessary, adjust the backend address below:
 */
const backend = "http://localhost:5000";

export function predict() {
  return postJson("/predict").then(parseJSON);
}

export function getPath(params) {
  return getJson("/path", params).then(parseJSON);
}

export function getSensors() {
  return getJson("/sensors").then(parseJSON);
}

export function getSensorData(sensorId) {
  return getJson(`/sensors/${sensorId}`).then(parseJSON);
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

function getJson(endpoint, params) {
  return fetch(`${backend}${endpoint}`, {
    params: params,
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  }).then(checkStatus);
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