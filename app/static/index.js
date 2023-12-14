let sorting_options = document.getElementById("sorting_options");
sorting_options.onchange = async function (event) {
    event.preventDefault();
    let option = sorting_options.value;
    console.log(option);
    let data;
    if (option === "Newest first") {
        const response = await fetch("sort/" + "newest");
        data = await response.text();
        window.location.href = "/sort/newest";
    } else if (option === "Oldest first") {
        const response = await fetch("sort/" + "oldest");
        data = await response.text();
        window.location.href = "/sort/oldest";
    } else if (option === "Most popular") {
        const response = await fetch("sort/" + "popular");
        data = await response.text();
        window.location.href = "/sort/popular";
    } else {
        const response = await fetch("home");
        data = await response.text();
        window.location.href = "home";
    }
};
