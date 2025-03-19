import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from image_processing import capture_image_from_camera, scan_image_to_text
from text_processing import process_extracted_text
import os
from text_processing import process_extracted_text


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Quét Hình Ảnh")
        self.root.geometry("600x400")

        # Tạo các thành phần giao diện
        self.label = tk.Label(root, text="Quét hình ảnh từ camera", font=("Arial", 16))
        self.label.pack(pady=20)

        self.capture_button = tk.Button(
            root, text="Chụp Ảnh", command=self.capture_image
        )
        self.capture_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def capture_image(self):
        # Chụp ảnh từ camera
        captured_image = capture_image_from_camera(
            save_folder=os.path.expanduser("~/Documents/Project_DACS")
        )

        if captured_image is None:
            messagebox.showwarning("Cảnh báo", "Không có hình ảnh được chụp.")
            return

        # Quét hình ảnh thành văn bản
        extracted_text = scan_image_to_text(captured_image)
        self.result_label.config(text=f"Văn bản trích xuất:\n{extracted_text}")

        # Xử lý văn bản để lấy thông tin hàng hóa
        product_code, quantity = process_extracted_text(extracted_text)

        if product_code and quantity:
            messagebox.showinfo(
                "Thông tin", f"Mã sản phẩm: {product_code}, Số lượng: {quantity}"
            )
        else:
            messagebox.showwarning(
                "Cảnh báo", "Không thể trích xuất thông tin từ hình ảnh."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
