document.getElementById("upload-form").addEventListener("submit", async function (event) {
    event.preventDefault();  // Prevent the default form submission

    let formData = new FormData();
    formData.append("image", document.getElementById("image").files[0]);

    // Show loading status
    document.getElementById("status").innerHTML = "Uploading and detecting... Please wait.";

    // Fetch request to send image to Flask backend
    let response = await fetch("/", {
        method: "POST",
        body: formData
    });

    // Wait for the response from Flask backend
    let result = await response.json();

    if (response.ok) {
        // Display the uploaded image
        document.getElementById("uploaded-img").src = URL.createObjectURL(document.getElementById("image").files[0]);
        document.getElementById("uploaded-img").style.display = "block";

        // Display the result image
        document.getElementById("detected-img").src = result.result_image_url;
        document.getElementById("detected-img").style.display = "block";
        document.getElementById("status").innerHTML = "Detection complete!";
    } else {
        document.getElementById("status").innerHTML = "Error occurred. Please try again.";
    }
});
