function updateFileLabel() {
	const fileInput = document.getElementById("files");
	const label = document.querySelector(".custom-file-upload");
	const processFilesButton = document.getElementById("process-files-button");

	if (fileInput.files.length > 0) {
		label.innerText = "Files Selected";
		processFilesButton.style.display = "inline-block";
	} else {
		label.innerText = "Choose File";
		processFilesButton.style.display = "none";
	}
}

function processFiles() {
	const fileInput = document.getElementById("files");
	const files = fileInput.files;

	if (files.length === 0) {
		alert("Please select files to upload");
		return;
	}

	const formData = new FormData();
	for (const file of files) {
		formData.append("files[]", file);
	}

	showProgressBar();

	fetch("/upload", {
		method: "POST",
		body: formData,
	})
		.then((response) => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error("File upload failed");
			}
		})
		.then((data) => {
			if (data.status === "Files uploaded successfully") {
				fetch("/process_files", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
				})
					.then((response) => response.json())
					.then((data) => {
						hideProgressBar();
						if (data.status) {
							alert(data.status);
							document.getElementById(
								"plot-options"
							).style.display = "block";
						} else {
							alert(data.error);
						}
					});
			} else {
				throw new Error("File upload failed");
			}
		})
		.catch((error) => {
			hideProgressBar();
			alert(error.message);
		});
}

function generatePlot(plotType, title) {
	const storedImage = localStorage.getItem(plotType);
	if (storedImage) {
		displayImage(storedImage, title);
	} else {
		showProgressBar();
		fetch("/plot", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ plot_type: plotType }),
		})
			.then((response) => response.json())
			.then((data) => {
				hideProgressBar();
				if (data.image_path) {
					localStorage.setItem(plotType, data.image_path);
					displayImage(data.image_path, title);
				} else {
					alert(data.error);
				}
			});
	}
}

function displayImage(imagePath, title) {
	const img = document.createElement("img");
	img.src = imagePath;
	img.alt = title;
	img.style.maxWidth = "100%";
	img.style.marginTop = "20px";

	const plotDiv = document.getElementById("plot");
	plotDiv.innerHTML = "";
	plotDiv.appendChild(img);

	const downloadLink = document.getElementById("download-link");
	downloadLink.href = imagePath;
	downloadLink.download = `${title}.png`;
	downloadLink.style.display = "block";
}

function showProgressBar() {
	const progressBar = document.getElementById("progress-bar");
	const progress = document.getElementById("progress");
	progress.style.width = "0%";
	progressBar.style.display = "block";
	let width = 0;
	const interval = setInterval(() => {
		if (width >= 100) {
			clearInterval(interval);
		} else {
			width += 10;
			progress.style.width = width + "%";
		}
	}, 100);
}

function hideProgressBar() {
	const progressBar = document.getElementById("progress-bar");
	progressBar.style.display = "none";
}
