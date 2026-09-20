from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4, A5
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "output" / "pdf"

SAMPLE_PATH = IMAGE_DIR / "sample.png"
LOGO_SOURCE_PATH = IMAGE_DIR / "Resort-main-logo.jpg"
LOGO_PATH = IMAGE_DIR / "rld-resort-logo-transparent.png"
QR_PATH = IMAGE_DIR / "rld-resort-google-review-qr.png"

POSTERS = {
    "a5": ((1749, 2481), A5),
    "a4": ((2481, 3508), A4),
}


def create_transparent_logo():
    """Crop the supplied logo into a transparent oval without redrawing it."""
    with Image.open(LOGO_SOURCE_PATH) as source:
        source = source.convert("RGB")
        logo = source.crop((88, 29, 412, 444)).convert("RGBA")

    scale = 4
    logo = logo.resize(
        (logo.width * scale, logo.height * scale),
        Image.Resampling.LANCZOS,
    )

    mask = Image.new("L", logo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, logo.width - 1, logo.height - 1), fill=255)
    logo.putalpha(mask)
    logo.save(LOGO_PATH, optimize=True)


def create_poster(size):
    """Keep the approved sample intact and overlay only the logo and QR code."""
    width, height = size
    with Image.open(SAMPLE_PATH) as source:
        poster = source.convert("RGB").resize(size, Image.Resampling.LANCZOS)

    with Image.open(LOGO_PATH) as source:
        logo = source.convert("RGBA")
        logo_height = round(height * 0.226)
        logo_width = round(logo_height * logo.width / logo.height)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    logo_x = (width - logo_width) // 2
    logo_y = round(height * 0.026)
    poster.paste(logo, (logo_x, logo_y), logo)

    with Image.open(QR_PATH) as source:
        qr = source.convert("RGB")
        qr_size = round(width * 0.36)
        qr = qr.resize((qr_size, qr_size), Image.Resampling.NEAREST)

    qr_x = (width - qr_size) // 2
    qr_y = round(height * 0.592)
    poster.paste(qr, (qr_x, qr_y))
    return poster


def create_pdf(image_path, pdf_path, page_size):
    page_width, page_height = page_size
    pdf = canvas.Canvas(str(pdf_path), pagesize=page_size, pageCompression=1)
    pdf.setTitle("RLD Resort Google Review Sign")
    pdf.setAuthor("RLD Resort")
    pdf.setSubject("Printable Google review QR sign")
    pdf.drawImage(
        str(image_path),
        0,
        0,
        width=page_width,
        height=page_height,
        preserveAspectRatio=False,
    )
    pdf.showPage()
    pdf.save()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_transparent_logo()

    for label, (pixel_size, page_size) in POSTERS.items():
        png_path = OUTPUT_DIR / f"rld-resort-google-review-sign-{label}.png"
        pdf_path = OUTPUT_DIR / f"rld-resort-google-review-sign-{label}.pdf"
        poster = create_poster(pixel_size)
        poster.save(png_path, dpi=(300, 300), optimize=True)
        create_pdf(png_path, pdf_path, page_size)

    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
