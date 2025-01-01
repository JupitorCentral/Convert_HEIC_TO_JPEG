import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif
import os

class HEICToJPGConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("HEIC to JPG Converter")

        # Center the window on the screen
        self.center_window()

        self.heic_files = []

        # Select HEIC Files Button
        self.select_button = tk.Button(master, text="Select HEIC Files", command=self.select_heic_files)
        self.select_button.pack(pady=10)

        # Display Selected Files
        self.files_label = tk.Label(master, text="No HEIC files selected.")
        self.files_label.pack()

        # Convert Button
        self.convert_button = tk.Button(master, text="Convert to JPG", command=self.convert_files, state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

    def center_window(self):
        self.master.update_idletasks()  # Update to get correct window dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

    def select_heic_files(self):
        self.heic_files = filedialog.askopenfilenames(
            title="Select HEIC Files",
            filetypes=(("HEIC files", "*.heic"), ("All files", "*.*"))
        )
        if self.heic_files:
            self.files_label.config(text=f"{len(self.heic_files)} HEIC files selected.")
            self.update_convert_button_state()
        else:
            self.files_label.config(text="No HEIC files selected.")
            self.update_convert_button_state()

    def update_convert_button_state(self):
        if self.heic_files:
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)

    def convert_files(self):
        if not self.heic_files:
            messagebox.showerror("Error", "No HEIC files selected.")
            return

        self.status_label.config(text="Converting...", fg="blue")
        self.master.update()  # Force update to show "Converting..."

        def convert_files(self):
            if not self.heic_files:
                messagebox.showerror("Error", "No HEIC files selected.")
                return

        self.status_label.config(text="Converting...", fg="blue")
        self.master.update()

        try:
            for heic_file_path in self.heic_files:
                try:
                    print(f"Processing: {heic_file_path}")
                    heif_file = pillow_heif.open_heif(heic_file_path)
                    width, height = heif_file.size
                    mode = heif_file.mode

                    # Calculate stride manually
                    if mode == "RGB":
                        stride = width * 3
                    elif mode == "RGBA":
                        stride = width * 4
                    elif mode == "L":
                        stride = width * 1
                    else:
                        print(f"Warning: Unknown mode '{mode}', assuming RGB stride.")
                        stride = width * 3  # Fallback

                    print(f"Calculated Stride: {stride}") # Debugging

                    image = Image.frombytes(
                        mode,
                        (width, height),
                        heif_file.data,
                        "raw",
                        mode, stride
                    )

                    base_name = os.path.splitext(os.path.basename(heic_file_path))[0]
                    output_directory = os.path.dirname(heic_file_path)
                    jpg_path = os.path.join(output_directory, f"{base_name}.jpg")

                    image.save(jpg_path, "JPEG")
                    print(f"Successfully converted '{heic_file_path}' to '{jpg_path}'")

                except Exception as e:
                    print(f"Error converting '{heic_file_path}': {e}")
                    messagebox.showerror("Conversion Error", f"Error converting '{os.path.basename(heic_file_path)}': {e}")
                    self.status_label.config(text="Conversion failed (see console for details)", fg="red")
                    return

            self.status_label.config(text="Conversion completed successfully!", fg="green")
            messagebox.showinfo("Success", "HEIC to JPG conversion completed!")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.status_label.config(text="An unexpected error occurred", fg="red")
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HEICToJPGConverterApp(root)
    root.mainloop()