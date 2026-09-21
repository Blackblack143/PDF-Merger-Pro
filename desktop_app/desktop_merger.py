
import customtkinter as ctk
from tkinter import filedialog, messagebox
import PyPDF2
import os

# Set UI appearance and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PDFMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Merger Pro")
        self.geometry("600x450")
        self.resizable(False, False)

        self.pdf_files = []

        # Title
        self.title_label = ctk.CTkLabel(self, text="Merge Multiple PDFs", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # Frame for Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # Select Files Button
        self.select_btn = ctk.CTkButton(self.button_frame, text="Select PDF Files", command=self.select_files)
        self.select_btn.grid(row=0, column=0, padx=10)

        # Clear List Button
        self.clear_btn = ctk.CTkButton(self.button_frame, text="Clear List", command=self.clear_files, 
                                       fg_color="#E74C3C", hover_color="#C0392B")
        self.clear_btn.grid(row=0, column=1, padx=10)

        # Textbox to display selected files
        self.textbox = ctk.CTkTextbox(self, width=500, height=200)
        self.textbox.pack(pady=10)
        self.textbox.insert("0.0", "No files selected...\n")
        self.textbox.configure(state="disabled")

        # Merge Button
        self.merge_btn = ctk.CTkButton(self, text="Merge & Save", command=self.merge_pdfs, 
                                       font=ctk.CTkFont(size=16, weight="bold"), height=40, 
                                       fg_color="#27AE60", hover_color="#2ECC71")
        self.merge_btn.pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if files:
            self.pdf_files.extend(files)
            self.update_textbox()

    def clear_files(self):
        self.pdf_files.clear()
        self.update_textbox()

    def update_textbox(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        if not self.pdf_files:
            self.textbox.insert("0.0", "No files selected...\n")
        else:
            for i, file in enumerate(self.pdf_files, 1):
                filename = os.path.basename(file)
                self.textbox.insert("end", f"{i}. {filename}\n")
        self.textbox.configure(state="disabled")

    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Warning", "Please select at least 2 PDF files to merge.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            title="Save Merged PDF As",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not save_path:
            return

        try:
            merger = PyPDF2.PdfMerger()
            for pdf in self.pdf_files:
                merger.append(pdf)

            merger.write(save_path)
            merger.close()

            messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved to: {save_path}")
            self.clear_files()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()