import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageEnhance, ImageTk, ImageFilter

# Create the main window
root = tk.Tk()
root.title("Photo Editor")
root.geometry("1000x600")
root.config(bg="white")

# Initialize global variables
file_path = None
img_display = None
original_image = None
current_image = None

# Function to open an image file
def upload_image():
    global file_path, img_display, original_image, current_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        original_image = Image.open(file_path)
        current_image = original_image.copy()
        display_image(original_image)
        reset_sliders()

# Function to display the image on the canvas
def display_image(image):
    global img_display
    # Resize image to fit within canvas dimensions if needed
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    image_width, image_height = image.size
    
    if image_width > canvas_width or image_height > canvas_height:
        # Scale down the image to fit within the canvas if it's larger
        scaling_factor = min(canvas_width / image_width, canvas_height / image_height)
        new_size = (int(image_width * scaling_factor), int(image_height * scaling_factor))
        image = image.resize(new_size, Image.LANCZOS)
    
    img_display = ImageTk.PhotoImage(image)
    canvas.config(width=img_display.width(), height=img_display.height())
    canvas.create_image(0, 0, anchor="nw", image=img_display)

# Reset sliders to default
def reset_sliders():
    brightness_slider.set(1)
    contrast_slider.set(1)
    color_slider.set(1)

# Function to apply adjustments in real-time
def apply_adjustments():
    global current_image
    if original_image:
        img = original_image.copy()

        # Apply brightness
        brightness_factor = brightness_slider.get()
        img = ImageEnhance.Brightness(img).enhance(brightness_factor)

        # Apply contrast
        contrast_factor = contrast_slider.get()
        img = ImageEnhance.Contrast(img).enhance(contrast_factor)

        # Apply color
        color_factor = color_slider.get()
        img = ImageEnhance.Color(img).enhance(color_factor)

        current_image = img
        display_image(img)

# Function to apply a filter to the image
def apply_filter(filter_type):
    global current_image
    if current_image:
        img = current_image.copy()

        if filter_type == "Blur":
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == "Grayscale":
            img = img.convert("L").convert("RGB")
        elif filter_type == "Edge Enhancement":
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == "Sharpen":
            img = img.filter(ImageFilter.SHARPEN)

        current_image = img
        display_image(img)

# Function to save the edited image
def save_image():
    if current_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if save_path:
            current_image.save(save_path)
            print("Image saved successfully!")

# Create the left panel for buttons and controls
left_frame = tk.Frame(root, width=200, height=600, bg="white")
left_frame.pack(side="left", fill="y")

# Upload image button
upload_button = tk.Button(left_frame, text="Upload Image", command=upload_image, bg="white")
upload_button.pack(pady=15)

# Filter combobox
filter_label = tk.Label(left_frame, text="Select Filter", bg="white")
filter_label.pack(pady=5)

filter_combobox = ttk.Combobox(left_frame, values=["Blur", "Grayscale", "Edge Enhancement", "Sharpen"])
filter_combobox.pack(padx=20)  # Add padding to the right

# Apply filter button
apply_button = tk.Button(left_frame, text="Apply Filter", command=lambda: apply_filter(filter_combobox.get()), bg="white")
apply_button.pack(pady=10)

# Brightness slider
brightness_label = tk.Label(left_frame, text="Brightness", bg="white")
brightness_label.pack()
brightness_slider = tk.Scale(left_frame, from_=0.5, to=2, resolution=0.1, orient="horizontal", command=lambda x: apply_adjustments())
brightness_slider.pack(pady=5)

# Contrast slider
contrast_label = tk.Label(left_frame, text="Contrast", bg="white")
contrast_label.pack()
contrast_slider = tk.Scale(left_frame, from_=0.5, to=2, resolution=0.1, orient="horizontal", command=lambda x: apply_adjustments())
contrast_slider.pack(pady=5)

# Color slider
color_label = tk.Label(left_frame, text="Color", bg="white")
color_label.pack()
color_slider = tk.Scale(left_frame, from_=0.5, to=2, resolution=0.1, orient="horizontal", command=lambda x: apply_adjustments())
color_slider.pack(pady=5)

# Save image button
save_button = tk.Button(left_frame, text="Save Image", command=save_image, bg="white")
save_button.pack(pady=10)

# Create the canvas where the image will be displayed
canvas = tk.Canvas(root, bg="white", scrollregion=(0, 0, 1000, 1000))
canvas.pack(side="right", fill="both", expand=True)

# Add scrollbars to the canvas
x_scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
x_scrollbar.pack(side="bottom", fill="x")
y_scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
y_scrollbar.pack(side="right", fill="y")

canvas.config(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

# Run the main loop
root.mainloop()