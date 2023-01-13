import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import cv2

def open_image():
    filepath = filedialog.askopenfilename()
    if filepath:
        image = cv2.imread(filepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 0
        params.maxThreshold = 256
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 100
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.5
        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.5
        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.5
        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        # Detect blobs
        keypoints = detector.detect(gray)
        # Initialize list to store dimensions of each object
        dimensions = []
        # Iterate over objects and draw rectangle around them
        for keypoint in keypoints:
            x = int(keypoint.pt[0])
            y = int(keypoint.pt[1])
            w = int(keypoint.size)
            h = int(keypoint.size)
            dimensions.append((w, h))
            cv2.rectangle(image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
            cv2.putText(image, f'Object {len(dimensions)}: {w}x{h}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        # Create a new Tkinter window to display the image
        window = tk.Toplevel()
        window.geometry("800x800")
        window.configure(bg='white')
        window.title("Processed Image")
        # Convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(Image.fromarray(image))
        # Add the image to a Label widget
        label = tk.Label(window, image=photo, bg='white')
        label.image = photo
        label.pack()
        # Save the dimensions to a text file
        with open("dimensions.txt", "w") as file:
            for idx, dim in enumerate(dimensions):
                file.write(f"Object {idx + 1}: {dim[0]}x{dim[1]}\n")
        messagebox.showinfo("Success", "Objects detected and saved to dimensions.txt")

root = tk.Tk()
root.title("Object Detector")
root.configure(bg='white')
root.geometry("300x150")
open_button = tk.Button(root, text="Open Image", command=open_image, bg='#00bfff',fg='white')
open_button.pack(pady=10)
root.mainloop()

