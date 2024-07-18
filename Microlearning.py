import os
import random
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import messagebox, font

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Microlearning")
        self.root.geometry("800x600")

        self.history = []
        self.current_index = -1
        self.all_paragraphs = []
        self.current_sequential_index = -1

        # Set a beautiful font
        custom_font = font.Font(family="Georgia", size=14)

        self.text_widget = tk.Text(root, wrap=tk.WORD, padx=10, pady=10, font=custom_font)
        self.text_widget.pack(expand=1, fill=tk.BOTH)

        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.show_button = tk.Button(button_frame, text="Show", command=self.show_paragraph)
        self.show_button.pack(side=tk.LEFT, fill=tk.X, expand=1)
        
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.prev_paragraph)
        self.prev_button.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_paragraph)
        self.next_button.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_history)
        self.clear_button.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.root.bind("<Right>", lambda event: self.next_paragraph())
        self.root.bind("<Left>", lambda event: self.prev_paragraph())
        self.root.bind("<Up>", lambda event: self.show_paragraph())
        self.root.bind("<Down>", lambda event: self.clear_history())
        self.root.bind("<Prior>", lambda event: self.prev_sequential_paragraph())  # PageUp
        self.root.bind("<Next>", lambda event: self.next_sequential_paragraph())  # PageDown
        
        self.load_all_paragraphs()
        self.load_random_paragraph()

    def load_all_paragraphs(self):
        folder = 'book'
        if not os.path.isdir(folder):
            messagebox.showerror("Error", f"Folder '{folder}' does not exist.")
            return

        pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
        if not pdf_files:
            messagebox.showerror("Error", "No PDF files found in the 'book' folder.")
            return

        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder, pdf_file)
            document = fitz.open(pdf_path)
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                text = page.get_text("text")
                sentences = text.split('. ')
                for i in range(0, len(sentences), 5):
                    paragraph = '. '.join(sentences[i:i+5])
                    if not paragraph.endswith('.'):
                        paragraph += '.'
                    self.all_paragraphs.append((pdf_path, page_num, paragraph))

    def load_random_paragraph(self):
        if not self.all_paragraphs:
            messagebox.showerror("Error", "No paragraphs found in the PDF files.")
            return

        pdf_path, page_num, paragraph = random.choice(self.all_paragraphs)
        self.history.append((pdf_path, page_num, paragraph))
        self.current_index += 1
        self.current_sequential_index = self.all_paragraphs.index((pdf_path, page_num, paragraph))
        self.display_paragraph(paragraph)

    def display_paragraph(self, paragraph):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, paragraph)

    def show_paragraph(self):
        if self.current_index < 0 or self.current_index >= len(self.history):
            return

        pdf_path, page_num, _ = self.history[self.current_index]
        os.system(f'start "" "C:\\Program Files (x86)\\Foxit Software\\Foxit PDF Reader\\FoxitPDFReader.exe" /A page={page_num + 1} "{pdf_path}"')

    def next_paragraph(self):
        if self.current_index + 1 < len(self.history):
            self.current_index += 1
            _, _, paragraph = self.history[self.current_index]
            self.display_paragraph(paragraph)
        else:
            self.load_random_paragraph()

    def prev_paragraph(self):
        if self.current_index > 0:
            self.current_index -= 1
            _, _, paragraph = self.history[self.current_index]
            self.display_paragraph(paragraph)

    def clear_history(self):
        if self.current_index < 0 or self.current_index >= len(self.history):
            return

        del self.history[self.current_index]
        if self.current_index >= len(self.history):
            self.current_index = len(self.history) - 1

        if self.history:
            _, _, paragraph = self.history[self.current_index]
            self.display_paragraph(paragraph)
        else:
            self.text_widget.delete(1.0, tk.END)
            self.current_index = -1

    def next_sequential_paragraph(self):
        if self.current_sequential_index < len(self.all_paragraphs) - 1:
            self.current_sequential_index += 1
            pdf_path, page_num, paragraph = self.all_paragraphs[self.current_sequential_index]
            self.history.append((pdf_path, page_num, paragraph))
            self.current_index = len(self.history) - 1
            self.display_paragraph(paragraph)

    def prev_sequential_paragraph(self):
        if self.current_sequential_index > 0:
            self.current_sequential_index -= 1
            pdf_path, page_num, paragraph = self.all_paragraphs[self.current_sequential_index]
            self.history.append((pdf_path, page_num, paragraph))
            self.current_index = len(self.history) - 1
            self.display_paragraph(paragraph)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()