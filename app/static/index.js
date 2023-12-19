let sorting_options = document.getElementById("sorting_options");
sorting_options.onchange = async function (event) {
    let option;
    console.log(option);
    if (option === "Newest first") {
        const response = await fetch("sort/" + "newest");
        await response.text();
        window.location.href = "/sort/newest";
    }
    else if (option === "Oldest first") {
        const response = await fetch("sort/" + "oldest");
        await response.text();
        window.location.href = "/sort/oldest";
    } else if (option === "Most popular") {
        const response = await fetch("sort/" + "popular");
        await response.text();
        window.location.href = "/sort/popular";
    }
    else {
        const response = await fetch("home");
        await response.text();
        window.location.href = "home";
    }
};

//sorting_options.addEventListener("change", async function(event) {
//    event.preventDefault()
//    console.log(this.value)
//    if (this.value === "Newest first") {
//        const response = await fetch("sort/" + "newest");
//        await response.text();
//        window.location.href = "/sort/newest";
//    }
//    else if (this.value === "Oldest first") {
//        const response = await fetch("sort/" + "oldest");
//        await response.text();
//        window.location.href = "/sort/oldest";
//    } else if (this.value === "Most popular") {
//        const response = await fetch("sort/" + "popular");
//        await response.text();
//        window.location.href = "/sort/popular";
//    }
//    else {
//        const response = await fetch("home");
//        await response.text();
//        window.location.href = "home";
//    }
//});


sorting_options.addEventListener("change", async function(event) {
    let url;
    if (this.value === "Newest first") {
        window.location.href = "/sort/newest";
    } else if (this.value === "Oldest first") {
         window.location.href = "/sort/oldest";
    } else if (this.value === "Most popular") {
        window.location.href = "/sort/popular";
    } else {
        window.location.href = "/home";
    }
});






//document.querySelectorAll("select").forEach(function(selectElement) {
//    selectElement.addEventListener("change", async function(e) {
//        e.preventDefault()
//        var newValue = e.detail.value;
//        var oldValue = e.detail.prevValue;
//        console.log(selectElement.value, newValue, oldValue);
//    let option = sorting_options.value;
//    console.log(option);
//    let data;
//    if (option === "Newest first") {
//        const response = await fetch("sort/" + "newest");
//        data = await response.text();
//        window.location.href = "/sort/newest";
//    } else if (option === "Oldest first") {
//        const response = await fetch("sort/" + "oldest");
//        data = await response.text();
//        window.location.href = "/sort/oldest";
//    } else if (option === "Most popular") {
//        const response = await fetch("sort/" + "popular");
//        data = await response.text();
//        window.location.href = "/sort/popular";
//    } else {
//        const response = await fetch("home");
//        data = await response.text();
//        window.location.href = "home";
//    }
//    });
//});
