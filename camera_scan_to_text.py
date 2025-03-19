import cv2
import pytesseract
import os

# Cấu hình đường dẫn đến Tesseract (chỉ cần trên Windows)
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"


def capture_image_from_camera(save_folder="captured_images"):
    """
    Hàm chụp ảnh từ camera và lưu vào thư mục.
    :param save_folder: Thư mục để lưu ảnh đã chụp.
    :return: Hình ảnh chụp từ camera.
    """
    # Tạo thư mục nếu nó không tồn tại
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Mở camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ValueError("Không thể mở camera. Hãy kiểm tra kết nối camera.")

    print("Nhấn phím 'c' để chụp ảnh và 'q' để thoát.")

    while True:
        # Đọc khung hình từ camera
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            raise ValueError(
                "Không thể đọc khung hình từ camera. Hãy kiểm tra lại camera."
            )

        # Hiển thị khung hình
        cv2.imshow("Camera", frame)

        # Chờ phím nhấn
        key = cv2.waitKey(1) & 0xFF

        # Nhấn 'c' để chụp ảnh
        if key == ord("c"):
            captured_image = frame
            # Lưu ảnh đã chụp
            image_path = os.path.join(
                save_folder, f"captured_{len(os.listdir(save_folder)) + 1}.png"
            )
            cv2.imwrite(image_path, captured_image)
            print(f"Ảnh đã được lưu tại: {image_path}")
            break

        # Nhấn 'q' để thoát
        if key == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            return None

    # Giải phóng camera và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()

    return captured_image


def scan_image_to_text(image, lang="vie"):
    """
    Hàm quét hình ảnh và trích xuất văn bản.
    :param image: Hình ảnh cần quét.
    :param lang: Ngôn ngữ sử dụng cho OCR (mặc định là tiếng Việt).
    :return: Văn bản trích xuất từ hình ảnh.
    """
    # Chuyển đổi hình ảnh sang grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sử dụng Tesseract để trích xuất văn bản
    text = pytesseract.image_to_string(gray_image, lang=lang)

    return text


def save_text_to_file(text, output_file="output.txt"):
    """
    Hàm lưu văn bản vào file.
    :param text: Văn bản cần lưu.
    :param output_file: Tên file đầu ra.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Văn bản đã được lưu vào file: {output_file}")


def main():
    # Bước 1: Chụp ảnh từ camera
    captured_image = capture_image_from_camera()

    if captured_image is None:
        print("Không có hình ảnh được chụp.")
        return

    # Bước 2: Quét hình ảnh thành văn bản
    extracted_text = scan_image_to_text(captured_image, lang="vie")
    print("Văn bản trích xuất:\n", extracted_text)

    # Bước 3: Lưu văn bản vào file
    save_text_to_file(extracted_text, output_file="output.txt")


if __name__ == "__main__":
    main()
