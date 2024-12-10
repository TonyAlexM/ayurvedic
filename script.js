document.getElementById("leafForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById("leafImage");
    const file = fileInput.files[0];
  
    if (!file) {
        alert("Please upload an image.");
        return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
  
    try {
        const response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData,
        });
  
        if (!response.ok) {
            throw new Error("Failed to identify leaf.");
        }
  
        const data = await response.json();
        document.getElementById("result").innerHTML = `
            <h2>Species: ${data.species}</h2>
            <p><strong>Uses:</strong> ${data.uses}</p>
        `;
    } catch (error) {
        document.getElementById("result").innerHTML = `<p style="color: red;">${error.message}</p>`;
    }
});
