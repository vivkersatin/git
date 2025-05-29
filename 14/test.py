import fitz  # PyMuPDF

pdf_path = "資通安全管理法及子法彙編.pdf"
txt_path = "output.txt"

doc = fitz.open(pdf_path)
with open(txt_path, "w", encoding="utf-8") as txt_file:
    for page in doc:
        txt_file.write(page.get_text() + "\n")

print("轉換完成！")