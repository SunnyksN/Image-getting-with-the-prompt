async function generateImage() {

    const prompt =
        document.getElementById("prompt").value;

    const status =
        document.getElementById("status");

    const image =
        document.getElementById("generatedImage");

    if (!prompt.trim()) {
        status.innerText =
            "Please enter a description.";
        return;
    }

    status.innerHTML = '<span class="loading"></span>Generating image...';
    image.classList.remove("show");

    try {

        const response = await fetch("/generate", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                prompt: prompt
            })
        });

        const data = await response.json();

        if (data.error) {
            status.innerText = data.error;
            return;
        }

        image.src = data.image_url;

        image.onload = () => {
            image.classList.add("show");
        };

        status.innerText =
            `Generated for: ${data.prompt}`;

    } catch (error) {
        status.innerText = "An error occurred. Please try again.";
        console.error(error);
    }
}
