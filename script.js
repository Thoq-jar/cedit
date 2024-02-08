// Function to save the file
function saveFile() {
    var textToSave = document.getElementById("editor").value;
    var blob = new Blob([textToSave], { type: "text/plain" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = "cedit_cloud.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    showMessage("File saved successfully!", "green");
}

// Function to clear the editor
function clearEditor() {
    var confirmation = confirm("Are you sure you want to clear the editor?");
    if (confirmation) {
        document.getElementById("editor").value = "";
    }
}

// Function to display a message
function showMessage(message, color) {
    var messageBox = document.createElement("div");
    messageBox.style.position = "fixed";
    messageBox.style.top = "10px";
    messageBox.style.left = "50%";
    messageBox.style.transform = "translateX(-50%)";
    messageBox.style.padding = "10px 20px";
    messageBox.style.backgroundColor = color;
    messageBox.style.color = "white";
    messageBox.style.borderRadius = "5px";
    messageBox.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.2)";
    messageBox.style.zIndex = "9999";
    messageBox.textContent = message;
    document.body.appendChild(messageBox);
    setTimeout(function () {
        document.body.removeChild(messageBox);
    }, 3000);
}

// Function for smooth typing animation
function smoothTyping() {
    clearTimeout(timer);
    var timer = setTimeout(function () {
        document.querySelector(".container").style.animation = "none";
    }, 500);
    document.querySelector(".container").style.animation = "pageSlideUp 0.5s ease";
}

function toggleHighContrast() {
    var body = document.body;
    var editor = document.getElementById("editor");
    if (body.style.backgroundColor === "black") {
        body.style.backgroundColor = "";
        editor.style.backgroundColor = "";
    } else {
        body.style.backgroundColor = "black";
        editor.style.backgroundColor = "black";
        body.style.color = white;
        editor.style.color = white;
    }
}

function toggleLightMode() {
    var body = document.body;
    var editor = document.getElementById("editor");
    if (body.classList.contains("light-mode")) {
        // Switch to default mode
        body.classList.remove("light-mode");
        editor.classList.remove("light-mode");
    } else {
        // Switch to light mode
        body.classList.add("light-mode");
        editor.classList.add("light-mode");
    }
}

// Auto-save functionality
setInterval(function () {
    var textToSave = document.getElementById("editor").value;
    localStorage.setItem("cedit_cloud_autosave", textToSave);
}, AUTO_SAVE_INTERVAL);

function changeBackgroundColor() {
    var color = document.getElementById("bgColorPicker").value;
    document.body.style.backgroundColor = color;
    document.getElementById("editor").style.backgroundColor = color;
}

// Restore auto-saved content
window.onload = function () {
    var autosavedContent = localStorage.getItem("cedit_cloud_autosave");
    if (autosavedContent) {
        document.getElementById("editor").value = autosavedContent;
    }

};


