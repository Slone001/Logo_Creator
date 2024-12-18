const uploadArea = document.getElementById("upload-area");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const uploadCon = document.getElementById("upload-con");

let selectedFiles = [];

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

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
});

uploadArea.addEventListener("click", (e) => {
    fileInput.click();
})

fileInput.addEventListener("change", (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
})

// Handle selected files
function handleFiles(files) {
    files.forEach((file) => {
        if (!file.type.startsWith("image/")) {
            alert("Nur Bilder erlaubt!");
            return;
        }
        selectedFiles.push(file);
        displayPreview(file);
    });
}


function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const previewItem = document.createElement("div");
        previewItem.classList.add("preview-item");

        const img = document.createElement("img");
        img.src = e.target.result;

        const removeBtn = document.createElement("button");
        removeBtn.classList.add("remove-btn");
        removeBtn.textContent = "X";

        removeBtn.addEventListener("click", () => {
            const index = selectedFiles.indexOf(file);
            if (index >= 0) {
                selectedFiles.splice(index, 1);
            }
            previewItem.remove();
        });

        previewItem.appendChild(img);
        previewItem.appendChild(removeBtn);
        preview.appendChild(previewItem);
    };
    reader.readAsDataURL(file);
}

//Upload Images
uploadCon.addEventListener("click", (e) => {
    const season_name = document.getElementById("season_name").value;

    if (selectedFiles.length === 0) {
        alert("Keine Bilder zum Upload ausgewählt!");
        return;
    }

    const formData = new FormData();
    formData.append("season_name", season_name);

    selectedFiles.forEach((file) => {
        formData.append("files[]", file);
    });

    fetch("/upload", {
        method: "POST",
        body: formData,
    })
        .then((response) => {
            if (!response.ok){
                throw new Error("Upload fehlgeschlagen");
            }
            return response.text();
        })
        .then((data) => {
            alert("Bilder erfolgreich hochgeladen");
            console.log(data);
            window.location.reload();
        })
        .catch((error) => {
            console.error("Error uploading images: ", error);
            alert("Fehler beim hochladen der Bilder");
        });
});


