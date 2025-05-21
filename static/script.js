document.querySelector("form").addEventListener("submit", function(event) {
    let animalName = document.getElementById("animal_name").value.trim();
    let breed = document.getElementById("breed").value.trim();
    let age = document.getElementById("age").value;
    let healthStatus = document.getElementById("health_status").value.trim();

    if (animalName === "" || breed === "" || healthStatus === "" || age <= 0) {
        alert("Please fill in all fields correctly!");
        event.preventDefault();
    }
});
