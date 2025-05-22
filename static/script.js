document.querySelector("form").addEventListener("submit", function(event) {
    let species = document.getElementById("species").value.trim();
    let breed = document.getElementById("breed").value.trim();
    let age = document.getElementById("age").value;
    let weight = document.getElementById("weight").value.trim();
    let errorMessage = document.getElementById("error-message");

    if (species === "" || breed === "" || weight === "" || isNaN(age) || age <= 0) {
        event.preventDefault();
        errorMessage.innerHTML = "❌ Please fill all fields correctly!";
        errorMessage.style.color = "red";
    } else {
        errorMessage.innerHTML = "";
    }
});
