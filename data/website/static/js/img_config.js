
const parts = window.location.href.split('/');
const imageName = parts.pop();
const folderName = parts.pop();
const statusEndpoint = `/image_status/${folderName}/${imageName}`;
const imageSrc = `/generated_preview/${folderName}/${imageName}`;

document.addEventListener("DOMContentLoaded", () => {
    // Image generation endpoint
    const imageContainer = document.getElementById("imageContainer");

    // Function to poll for the image
    async function pollForImage() {
        const interval = setInterval(async () => {
            try {
                console.log("Polling for image status...");
                const response = await fetch(statusEndpoint, { method: "HEAD" }); // Send a HEAD request to check image availability
                if (response.ok) {
                    // Image is ready, display it
                    clearInterval(interval); // Stop polling
                    console.log("Image is ready. Loading it now...");
                    imageContainer.innerHTML = `<img src="${imageSrc}" alt="Generated Image">`;
                }
            } catch (error) {
                console.error("Error checking image:", error);
            }}, 1000); // Check every 2 seconds
    }

    // Start polling for the image
    pollForImage();
});

