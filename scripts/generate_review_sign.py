from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.lib.pagesizes import A4, A5
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "output" / "pdf"

SAMPLE_PATH = IMAGE_DIR / "1.png"
LOGO_SOURCE_PATH = IMAGE_DIR / "Resort-main-logo.jpg"
LOGO_PATH = IMAGE_DIR / "rld-resort-logo-transparent.png"
QR_PATH = IMAGE_DIR / "rld-resort-google-review-qr.png"
FONT_DIR = Path("C:/Windows/Fonts")

LOGO_TERRACOTTA = (166, 76, 44, 255)
LOGO_CREAM = (250, 222, 204, 255)

POSTERS = {
    "a5": ((1749, 2481), A5),
    "a4": ((2481, 3508), A4),
}


def draw_spaced_text(draw, center_x, y, text, font, fill, tracking):
    widths = [draw.textlength(character, font=font) for character in text]
    total_width = sum(widths) + tracking * (len(text) - 1)
    cursor = center_x - total_width / 2
    for character, width in zip(text, widths):
        draw.text((cursor, y), character, font=font, fill=fill)
        cursor += width + tracking


def create_transparent_logo():
    """Restore the supplied badge and correct only its location spelling."""
    with Image.open(LOGO_SOURCE_PATH) as source:
        source = source.convert("RGB")
        # The white oval spans x=97..402 and y=70..429 in the source.
        # Keep a uniform six-pixel terracotta margin outside that exact outline.
        original_badge = source.crop((91, 64, 408, 435))

    logo_width = 1500
    logo_size = (
        logo_width,
        round(logo_width * original_badge.height / original_badge.width),
    )
    original_badge = original_badge.resize(logo_size, Image.Resampling.LANCZOS)
    line_mask = original_badge.convert("L").point(
        lambda value: max(0, min(255, (value - 135) * 3))
    )
    line_mask = line_mask.filter(ImageFilter.GaussianBlur(radius=0.6))
    mask_draw = ImageDraw.Draw(line_mask)
    mask_draw.rectangle((460, 1100, 1040, 1405), fill=0)

    logo = Image.new("RGBA", logo_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    draw.ellipse(
        (0, 0, logo.width - 1, logo.height - 1),
        fill=LOGO_TERRACOTTA,
    )
    restored_lines = Image.new("RGBA", logo_size, LOGO_CREAM)
    restored_lines.putalpha(line_mask)
    logo.alpha_composite(restored_lines)

    location_font = ImageFont.truetype(str(FONT_DIR / "arial.ttf"), 68)
    established_font = ImageFont.truetype(str(FONT_DIR / "arial.ttf"), 56)
    draw_spaced_text(
        draw, 750, 1125, "POLANGYUTA,", location_font, LOGO_CREAM, 7
    )
    draw_spaced_text(
        draw, 750, 1225, "SIQUIJOR PH", location_font, LOGO_CREAM, 7
    )
    draw_spaced_text(
        draw, 750, 1327, "EST. 2024", established_font, LOGO_CREAM, 6
    )
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
