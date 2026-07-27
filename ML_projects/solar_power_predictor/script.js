document.addEventListener("DOMContentLoaded", () => {
  const user_input = document.getElementById("capacity-input");
  const btn = document.getElementById("get-weather-btn");
  const description = document.getElementById("description");
  const weatherInfo = document.getElementById("weather-info");
  const error_message = document.getElementById("error-message");
  const temperature = document.getElementById("temperature");
  const head = document.getElementById("head");
  const Output = document.getElementById("output");
  const API_Key = "d392c977f47d0c36d7dc297b5b2242e2";

  async function sendData(values) {
    const response = await fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ features: values }),
    });

    const remark = await response.json();
    return remark;
  }

  async function getLocation() {
    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude, accuracy } = position.coords;
          resolve([latitude, longitude]);
        },
        (error) => {
          switch (error.code) {
            case error.PERMISSION_DENIED:
              reject(error);
              console.log("User denied location permission.");
              break;
            case error.POSITION_UNAVAILABLE:
              reject(error);
              console.log("Location information unavailable.");
              break;
            case error.TIMEOUT:
              reject(error);
              console.log("Location request timed out.");
              break;
            default:
              reject(error);
              console.log("Unknown error.");
          }
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0,
        },
      );
    });
  }

  btn.addEventListener("click", async () => {
    try {
      var [lat, lng] = await getLocation();
      const weatherdata = await fetchWeatherData(lat, lng);
      const dt = weatherdata.dt,
        sunrise = weatherdata.sys.sunrise,
        sunset = weatherdata.sys.sunset;
      const capacity = Number(user_input.value.trim());
      const localTimeMs = (weatherdata.dt + weatherdata.timezone) * 1000;
      const localDate = new Date(localTimeMs);
      const hour = localDate.getUTCHours();
      if (!capacity) return;
      let out = null;

      if (dt < sunrise || dt > sunset) {
        out = "0";
      } else {
        const values = [
          weatherdata.wind.speed,
          weatherdata.main.pressure,
          weatherdata.main.humidity,
          weatherdata.clouds.all,
          weatherdata.wind.deg,
          weatherdata.main.temp - 273,
          hour
        ];
        const remark = await sendData(values);
        out = energyError(capacity, remark.remark);
      }
      displayData(weatherdata, out);
    } catch (error) {
      console.log(error);
      show_error(error);
    }
  });

  function energyError(capacity, remark) {
    if (!capacity) return;
    const out = capacity - remark[0] * capacity;
    if (out < 0) {
      return 0;
    }
    return out.toFixed(2);
  }

  async function fetchWeatherData(latitude, longitude) {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${API_Key}`;
    const main_response = await fetch(url);
    const data = await main_response.json();
    console.log(data);
    return data;
  }

  function displayData(data, output) {
    if (!data || !output) return;
    error_message.classList.replace("active", "hidden");
    weatherInfo.classList.replace("hidden", "active");
    temperature.textContent = `Temperature : ${(data.main.temp - 273).toFixed(2)}°C`;
    description.textContent = `Weather : ${data.weather[0].main}`;
    head.textContent = `Weather Info`;
    Output.textContent = `${output} kw`;
  }

  function show_error(error) {
    weatherInfo.classList.replace("active", "hidden");
    error_message.classList.replace("hidden", "active");
    error_message.textContent = error;
  }
});
