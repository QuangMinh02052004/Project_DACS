import re


def process_extracted_text(text):
    """
    Hàm xử lý văn bản trích xuất để lấy thông tin hàng hóa.
    :param text: Văn bản trích xuất từ hình ảnh.
    :return: Mã sản phẩm và số lượng.
    """
    # Biểu thức chính quy để trích xuất mã sản phẩm và số lượng
    product_code_pattern = r"Mã SP: (\w+)"
    quantity_pattern = r"Số lượng: (\d+)"

    # Tìm kiếm thông tin
    product_code_match = re.search(product_code_pattern, text)
    quantity_match = re.search(quantity_pattern, text)

    if product_code_match and quantity_match:
        product_code = product_code_match.group(1)
        quantity = quantity_match.group(1)
        return product_code, quantity
    else:
        return None, None
