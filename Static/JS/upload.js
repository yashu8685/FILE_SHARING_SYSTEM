document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.querySelector('input[type="file"]');
    const fileName = document.getElementById("file-name");
    const preview = document.getElementById("preview-image");
    const removeBtn = document.getElementById("remove-file");
    const progressBar = document.getElementById("progress-bar");
    const form = document.getElementById("upload-form");
    const dropArea = document.getElementById("drop-area");

    function showFile(file) {

        fileName.innerHTML = "📄 " + file.name;

        removeBtn.style.display = "inline-block";

        if (file.type.startsWith("image")) {

            preview.style.display = "block";

            preview.src = URL.createObjectURL(file);

        } else {

            preview.style.display = "none";

        }

    }

    fileInput.addEventListener("change", function () {

        if (fileInput.files.length > 0) {

            showFile(fileInput.files[0]);

        }

    });

    removeBtn.addEventListener("click", function () {

        fileInput.value = "";

        preview.style.display = "none";

        removeBtn.style.display = "none";

        fileName.innerHTML = "No file selected";

    });

    dropArea.addEventListener("dragover", function (e) {

        e.preventDefault();

        dropArea.classList.add("dragover");

    });

    dropArea.addEventListener("dragleave", function () {

        dropArea.classList.remove("dragover");

    });

    dropArea.addEventListener("drop", function (e) {

        e.preventDefault();

        dropArea.classList.remove("dragover");

        fileInput.files = e.dataTransfer.files;

        if (fileInput.files.length > 0) {

            showFile(fileInput.files[0]);

        }

    });

    form.addEventListener("submit", function () {

        let width = 0;

        progressBar.style.width = "0%";

        progressBar.innerHTML = "0%";

        const interval = setInterval(function () {

            if (width >= 100) {

                clearInterval(interval);

            } else {

                width += 5;

                progressBar.style.width = width + "%";

                progressBar.innerHTML = width + "%";

            }

        }, 80);

    });

});

function copyLink(link){

    navigator.clipboard.writeText(link);

    alert("Share link copied!");

}

document.querySelectorAll(".copy-btn").forEach(button => {
    button.addEventListener("click", function () {
        const link = this.dataset.link;
        navigator.clipboard.writeText(link);
        alert("Share link copied!");
    });
});