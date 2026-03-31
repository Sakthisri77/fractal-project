from flask import Flask, render_template, request
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
GRAPH_FOLDER = "static/graphs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["GRAPH_FOLDER"] = GRAPH_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)


def fractal_dimension(image):
    image = image > 0

    sizes = []
    counts = []

    min_dim = min(image.shape)

    box_sizes = np.logspace(1, np.log10(min_dim), num=10, base=2).astype(int)
    box_sizes = np.unique(box_sizes)

    for size in box_sizes:
        if size < 2:
            continue

        count = 0
        for i in range(0, image.shape[0], size):
            for j in range(0, image.shape[1], size):
                if np.any(image[i:i+size, j:j+size]):
                    count += 1

        sizes.append(size)
        counts.append(count)

    sizes = np.array(sizes)
    counts = np.array(counts)

    mask = counts > 0
    sizes = sizes[mask]
    counts = counts[mask]

    x = np.log(1 / sizes)
    y = np.log(counts)

    coeffs = np.polyfit(x, y, 1)
    dimension = round(coeffs[0], 4)

    plt.figure()
    plt.scatter(x, y)
    plt.plot(x, np.polyval(coeffs, x))
    plt.xlabel("log(1/box size)")
    plt.ylabel("log(box count)")
    plt.title("Box Counting Graph")

    graph_path = os.path.join(GRAPH_FOLDER, "graph.png")
    plt.savefig(graph_path)
    plt.close()

    return dimension, graph_path


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/process", methods=["GET", "POST"])
def process():
    if request.method == "POST":
        file = request.files["image"]
        threshold_value = int(request.form.get("threshold", 128))

        if file.filename == "":
            return render_template("process.html")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        img = cv2.imread(filepath, 0)
        _, binary = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
        binary = cv2.medianBlur(binary, 3)

        binary_path = os.path.join(app.config["UPLOAD_FOLDER"], "binary.png")
        cv2.imwrite(binary_path, binary)

        dimension, graph_path = fractal_dimension(binary)

        return render_template(
            "process.html",
            image="/" + filepath.replace("\\", "/"),
            binary="/" + binary_path.replace("\\", "/"),
            graph="/" + graph_path.replace("\\", "/"),
            dimension=dimension
        )

    return render_template("process.html")


# 🔥 UPDATED ROUTE
@app.route("/review")
def review():
    return render_template("review.html")


if __name__ == "__main__":
    app.run(debug=True)