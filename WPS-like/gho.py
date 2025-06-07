import subprocess

def compress_pdf_with_ghostscript(input_path, output_path, quality=80):
    """
    Compresses a PDF file using Ghostscript.
    
    :param input_path: Path to the input PDF file.
    :param output_path: Path to save the compressed PDF file.
    :param quality: Compression quality (1-100).
    """
    ghostscript_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",  # /screen, /ebook, /prepress, /printer
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    subprocess.run(ghostscript_command)

# Example usage
input_pdf = "./output_combined.pdf"
output_pdf = "compressed_example.pdf"
compress_pdf_with_ghostscript(input_pdf, output_pdf)
