# fractal-project
Fractal dimension reveals the hidden complexity of patterns that look chaotic at first glance. It is used in fields like image processing, nature analysis, medical imaging, and computer graphics to better understand patterns and structure
# Fractal Dimension Analyzer

This project is a web-based application that calculates the **fractal dimension** of complex structures using the **Box Counting Method**.

## 🔍 Features

- Upload any image
- Convert image to binary using adjustable threshold
- Apply box-counting algorithm
- Calculate fractal dimension accurately
- Display:
  - Original image
  - Binary image
  - Box-counting graph
- User review system with ratings

## 🧠 Concept

Fractal dimension measures how complex a structure is. Unlike traditional dimensions (1D, 2D, 3D), fractals can have non-integer values.

This project uses the **Box Counting Method**, where:
- The image is divided into grids of different sizes
- Count how many boxes contain part of the structure
- Use log-log graph to compute slope → fractal dimension

## 🛠️ Technologies Used

- Python (Flask)
- OpenCV
- NumPy
- Matplotlib
- HTML, CSS, JavaScript

## 📂 Project Structure
