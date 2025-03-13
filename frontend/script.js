document.getElementById("image-file").addEventListener("change", function (e) {
    const fileName = e.target.files[0].name;
    document.getElementById("file-name").textContent = fileName;

    // Display the uploaded image
    const reader = new FileReader();
    reader.onload = function (event) {
        const uploadedImage = document.getElementById("uploaded-image");
        uploadedImage.src = event.target.result;
        uploadedImage.style.display = "block";
    };
    reader.readAsDataURL(e.target.files[0]);
});

// Function to hide all output sections
function hideAllOutputs() {
    document.querySelectorAll(".output-section").forEach(section => {
        section.style.display = "none";
    });
}

document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const imageFile = document.getElementById("image-file").files[0];
    const analysisType = document.getElementById("analysis-type").value;

    if (!imageFile) {
        alert("Please select an image file.");
        return;
    }

    try {
        document.getElementById("result").style.display = "block";
        hideAllOutputs(); // Hide all sections before showing the relevant ones

        const formData = new FormData();
        formData.append("image", imageFile);

        let endpoint = "/caption";
        if (analysisType === "medical") endpoint = "/medical-analysis";
        else if (analysisType === "social") endpoint = "/social-media-analysis";
        else if (analysisType === "quick") endpoint = "/quick-analysis";

        const response = await fetch(endpoint, { method: "POST", body: formData });
        const data = await response.json();

        console.log("Backend response:", data); // Debugging

        // Show only the relevant output fields
        if (analysisType === "medical") {
            document.getElementById("medical-section").style.display = "block";
            document.getElementById("medical-description").textContent = data.medical_description || "No medical description.";
            document.getElementById("anatomy").innerHTML = data.detected_anatomy
                ? data.detected_anatomy.map(obj => `<li>${obj}</li>`).join("")
                : "<li>No anatomy detected.</li>";
        } else if (analysisType === "social") {
            document.getElementById("social-section").style.display = "block";
            document.getElementById("social-caption").textContent = data.caption || "No caption.";
            document.getElementById("hashtags").textContent = data.hashtags || "No hashtags.";
            document.getElementById("engagement-tips").textContent = data.engagement_tips || "No engagement tips.";
        } else if (analysisType === "quick") {
            document.getElementById("quick-section").style.display = "block";
            document.getElementById("quick-caption").textContent = data.caption || "No caption.";
            document.getElementById("quick-objects").innerHTML = data.objects
                ? data.objects.map(obj => `<li>${obj}</li>`).join("")
                : "<li>No objects detected.</li>";
        } else {
            // General analysis
            document.getElementById("general-section").style.display = "block";
            document.getElementById("general-caption").textContent = data.caption || "No caption.";
            document.getElementById("detailed-description").textContent = data.detailed_description || "No description.";
            document.getElementById("objects").innerHTML = data.objects
                ? data.objects.map(obj => `<li>${obj}</li>`).join("")
                : "<li>No objects detected.</li>";
            document.getElementById("context").textContent = data.context ? JSON.stringify(data.context) : "No context.";
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});