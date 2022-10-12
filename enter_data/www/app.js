console.log("Hello world");

var url = `${window.location.protocol}//${window.location.host}/data`;
console.log(url);
const button = document.getElementById("post-btn");

button.addEventListener("click", async (_) => {
  try {
    const response = await fetch(url, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "post",
      body: JSON.stringify({
        username: document.getElementById("input-username").value,
        password: document.getElementById("input-password").value,
        workout: {
          start_timestamp: document.getElementById("start-timestamp").value,
          end_timestamp: document.getElementById("end-timestamp").value,
          calories_burned: parseInt(document.getElementById("calories-burned").value),
          peak_heart_rate: parseInt(document.getElementById("peak_heart_rate").value),
          minimum_heart_rate: parseInt(document.getElementById("minimum_heart_rate").value),
        },
      }),
    });
    console.log("Completed!", response);
  } catch (err) {
    console.error(`Error: ${err}`);
  }
});
