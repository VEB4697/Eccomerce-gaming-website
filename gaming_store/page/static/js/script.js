document.addEventListener("DOMContentLoaded", () => {
    console.log("Gaming Store homepage loaded.");

    // Animate the title with typewriter effect
    const title = document.querySelector(".animated-title");
    if (title) {
        const text = title.innerText;
        title.innerText = "";
        let index = 0;

        function typeWriter() {
            if (index < text.length) {
                title.innerText += text.charAt(index);
                index++;
                setTimeout(typeWriter, 60);
            }
        }
        typeWriter();
    }
});
