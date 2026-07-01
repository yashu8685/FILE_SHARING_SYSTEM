document.addEventListener("DOMContentLoaded", function () {

    const button = document.getElementById("theme-toggle");

    if (!button) return;

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        button.innerHTML = "☀️";
    }

    button.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            localStorage.setItem("theme", "dark");

            button.innerHTML = "☀️";

        } else {

            localStorage.setItem("theme", "light");

            button.innerHTML = "🌙";

        }

    });

});