import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Tk, Label, PhotoImage
from PIL import Image, ImageTk
import numpy as np

# Global variable for image path
image_path = ""

def encode_data(image_path, text=None):
    # Load the cover image
    image = Image.open(image_path)
    image_array = np.array(image)

    binary_data = ""

    # Encode text
    if text:
        binary_text = ''.join([format(ord(char), '08b') for char in text])
        binary_data += binary_text + '1111111111111110'  # Delimiter to indicate the end of text

    # Get the dimensions of the image
    rows, cols, _ = image_array.shape

    # Encoding the data into the image
    binary_index = 0
    for i in range(rows):
        for j in range(cols):
            pixel = image_array[i][j]
            for k in range(3):  # Loop through RGB
                if binary_index < len(binary_data):
                    pixel[k] = int(format(pixel[k], '08b')[:-1] + binary_data[binary_index], 2)
                    binary_index += 1
                else:
                    break
        if binary_index >= len(binary_data):
            break

    # Save the modified image
    encoded_image = Image.fromarray(image_array)
    return encoded_image

def decode_data(image_path):
    # Load image
    image = Image.open(image_path)
    image_array = np.array(image)

    binary_data = ""

    # Get the dimensions of the image
    rows, cols, _ = image_array.shape

    # Extracting the LSBs to retrieve the hidden data
    for i in range(rows):
        for j in range(cols):
            pixel = image_array[i][j]
            for k in range(3):  # Loop through RGB
                binary_data += format(pixel[k], '08b')[-1]

    # Separate text data
    data_parts = binary_data.split('1111111111111110', 1)
    text_data = data_parts[0]

    # Decode text
    decoded_text = ""
    for i in range(0, len(text_data), 8):
        decoded_text += chr(int(text_data[i:i + 8], 2))

    return decoded_text

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if image_path:
        img = Image.open(image_path)
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img

def encode():
    if not image_path:
        output_label.config(text="Error: Please select an image first.", fg="red")
        return

    text = text_entry.get()
    if not text:
        output_label.config(text="Error: Please enter text to encode.", fg="red")
        return

    encoded_image = encode_data(image_path, text=text)
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        encoded_image.save(save_path)
        output_label.config(text="Success: Data encoded and saved successfully!", fg="green")

def encode_text_file():
    if not image_path:
        output_label.config(text="Error: Please select an image first.", fg="red")
        return

    file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        output_label.config(text="Error: Please select a text file.", fg="red")
        return

    with open(file_path, 'r') as file:
        text = file.read()

    encoded_image = encode_data(image_path, text=text)
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        encoded_image.save(save_path)
        output_label.config(text="Success: Text file encoded and saved successfully!", fg="green")

def save_decoded_text(decoded_text):
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write(decoded_text)
        messagebox.showinfo("Save Successful", "Text saved as a file successfully!")

def decode():
    if not image_path:
        output_label.config(text="Error: Please select an image first.", fg="red")
        return

    decoded_text = decode_data(image_path)

    if decoded_text:
        output_label.config(text="Decoded Text:", fg="green")
        decoded_text_box.config(state=tk.NORMAL)
        decoded_text_box.delete(1.0, tk.END)
        decoded_text_box.insert(tk.END, decoded_text)
        decoded_text_box.config(state=tk.DISABLED)

        save_button = tk.Button(root, text="Save Decoded Text", command=lambda: save_decoded_text(decoded_text))
        save_button.pack(pady=5)
    else:
        output_label.config(text="No hidden text found in the image.", fg="orange")

def show_main_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Add heading
    heading_label = tk.Label(root, text="Steganography Tool", font=("Helvetica", 16, "bold"))
    heading_label.pack(pady=20)

    # Main menu buttons
    encode_button = tk.Button(root, text="Encode Data into Image", command=show_encode_menu)
    encode_button.pack(pady=10)

    decode_button = tk.Button(root, text="Decode Data from Image", command=show_decode_menu)
    decode_button.pack(pady=10)

def show_encode_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Image selection
    global image_label
    image_label = tk.Label(root, text="No image selected", width=30, height=15)
    image_label.pack(pady=10)

    select_button = tk.Button(root, text="Select Image", command=select_image)
    select_button.pack()

    # Text entry for encoding
    text_label = tk.Label(root, text="Enter text to encode:")
    text_label.pack()

    global text_entry
    text_entry = tk.Entry(root, width=50)
    text_entry.pack(pady=10)

    # Encode button
    encode_button = tk.Button(root, text="Encode", command=encode)
    encode_button.pack(pady=5)

    # Text file encoding button
    encode_file_button = tk.Button(root, text="Encode Text File into Image", command=encode_text_file)
    encode_file_button.pack(pady=10)

    # Output label
    global output_label
    output_label = tk.Label(root, text="", wraplength=400)
    output_label.pack(pady=10)

    # Back button
    back_button = tk.Button(root, text="Back to Main Menu", command=show_main_menu)
    back_button.pack(pady=10)

def show_decode_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Image selection
    global image_label
    image_label = tk.Label(root, text="No image selected", width=30, height=15)
    image_label.pack(pady=10)

    select_button = tk.Button(root, text="Select Image", command=select_image)
    select_button.pack()

    # Decode button
    decode_button = tk.Button(root, text="Decode", command=decode)
    decode_button.pack(pady=5)

    # Output label
    global output_label
    output_label = tk.Label(root, text="", wraplength=400)
    output_label.pack(pady=10)

    # Decoded text box with scroll bar
    global decoded_text_box
    decoded_text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED)
    decoded_text_box.pack(pady=10)

    # Back button
    back_button = tk.Button(root, text="Back to Main Menu", command=show_main_menu)
    back_button.pack(pady=10)

# GUI setup
root = tk.Tk()
root.geometry("700x700")
root.title("Steganography Tool")

# Show the main menu
show_main_menu()

# Start the GUI event loop
root.mainloop()
