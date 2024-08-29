import flet as ft
from pypdf import PdfReader, PdfWriter
import os, re

def split_pdf(input_pdf_path, output_dir):
    if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    reader = PdfReader(input_pdf_path)
    num_pages = len(reader.pages)

    for i in range(num_pages):
        sourcepage = reader.pages[i]
        sourcetext =  sourcepage.extract_text()

        output_pdf_file_name =  re.findall(r"チケット番号\s*(\d+)", sourcetext)[0]
        output_pdf_path = rf"{output_dir}/{output_pdf_file_name}.pdf"

        writer = PdfWriter() 

        writer.add_page(sourcepage)

        with open(output_pdf_path, "wb") as output_pdf_file:
            writer.write(output_pdf_file)

def main(page: ft.Page):
    def pick_file_result(e: ft.FilePickerResultEvent):
        selected_files.value = e.files[0].name if e.files else "Canceled"
        selected_files.update()

        pdf_file_path = e.files[0].path
        pdf_file_dir_path = os.path.dirname(pdf_file_path)
        output_dir_path = f"{pdf_file_dir_path}/slice"

        split_pdf(pdf_file_path, output_dir_path)
        page.open(dlg_modal)        
    
    def handle_close(e):
        page.close(dlg_modal)

    pick_files_dialog = ft.FilePicker(on_result=pick_file_result)
    selected_files = ft.Text()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("処理が完了しました．"),
        content=ft.Text("分割されたPDFファイルは元のPDFファイルがあったフォルダ内のsliceフォルダに保存されました．"),
        actions=[
            ft.TextButton("閉じる", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(pick_files_dialog)

    page.add(
         ft.Row([
            ft.Column([
                    ft.ElevatedButton(
                        "PDFを選択",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _ : pick_files_dialog.pick_files(
                            allowed_extensions=["pdf"],
                            allow_multiple=False,
                            dialog_title="PDFを選択"
                        ),
                    ),

                    selected_files
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(main)
