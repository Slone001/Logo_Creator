const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");

// Handle drag-and-drop functionality
uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragging");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragging");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragging");

    const files = e.dataTransfer.files;
    handleFiles(files);
});

// Handle click to upload
document.getElementById("upload-btn").addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (e) => {
    const files = e.target.files;
    handleFiles(files);
});

// Handle selected files
function handleFiles(files) {
    Array.from(files).forEach((file) => {
        if (!file.type.startsWith("image/")) {
            alert("Only image files are allowed!");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.createElement("img");
            img.src = e.target.result;
            preview.appendChild(img);
        };
        reader.readAsDataURL(file);
    });
}
