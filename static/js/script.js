function myFunction(color) {
    /* Get the text field */
    var copyText = document.getElementById(color);

    /* Select the text field */
    // console.log(copyText.innerHTML.trim());
    color_to_copy = copyText.innerHTML.trim()
    /* Copy the text inside the text field */
    navigator.clipboard.writeText(color_to_copy);

    /* Alert the copied text */
    alert("Copied the color: " + color_to_copy);
}


const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))