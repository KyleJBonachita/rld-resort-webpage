from pathlib import Path

from PIL import Image, ImageEnhance
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "output" / "pdf"
TEMP_DIR = ROOT / "tmp" / "pdfs"

PHOTO_PATH = IMAGE_DIR / "Resort-main-night.jpg"
QR_PATH = IMAGE_DIR / "rld-resort-google-review-qr.png"
HEADER_PATH = TEMP_DIR / "rld-resort-review-sign-header.jpg"

FOREST = HexColor("#072D2B")
INK = HexColor("#16302D")
CORAL = HexColor("#E86F51")
SUN = HexColor("#E2AD4B")
WATER = HexColor("#1E7771")
PAPER = HexColor("#FFFDF8")
CREAM = HexColor("#F5EFE3")
WHITE = HexColor("#FFFFFF")

A5_WIDTH, A5_HEIGHT = A5


def register_fonts():
    font_dir = Path("C:/Windows/Fonts")
    fonts = {
        "RLD-Sans": font_dir / "arial.ttf",
        "RLD-Sans-Bold": font_dir / "arialbd.ttf",
        "RLD-Serif": font_dir / "georgia.ttf",
        "RLD-Serif-Bold": font_dir / "georgiab.ttf",
    }
    for name, path in fonts.items():
        if not path.exists():
            raise FileNotFoundError(f"Required font not found: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))


def draw_cover_image(c, image_path, x, y, width, height, focus_y=0.52):
    with Image.open(image_path) as image:
        image_width, image_height = image.size
    scale = max(width / image_width, height / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    draw_x = x + (width - draw_width) / 2
    overflow_y = draw_height - height
    draw_y = y - overflow_y * focus_y

    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(
        ImageReader(str(image_path)),
        draw_x,
        draw_y,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        mask="auto",
    )
    c.restoreState()


def prepare_header_image():
    target_width = 1800
    target_height = round(target_width * (52 / 148))
    target_ratio = target_width / target_height

    with Image.open(PHOTO_PATH) as source:
        source = source.convert("RGB")
        source_width, source_height = source.size
        crop_height = round(source_width / target_ratio)
        crop_top = round((source_height - crop_height) * 0.55)
        crop = source.crop((0, crop_top, source_width, crop_top + crop_height))
        crop = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
        crop = ImageEnhance.Contrast(crop).enhance(1.08)
        crop = ImageEnhance.Brightness(crop).enhance(0.84)
        tint = Image.new("RGB", crop.size, (7, 45, 43))
        finished = Image.blend(crop, tint, 0.34)
        finished.save(HEADER_PATH, quality=94, subsampling=0, optimize=True)


def draw_spaced_text(c, text, x, y, font_name, font_size, color, tracking, align="left"):
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    widths = [pdfmetrics.stringWidth(char, font_name, font_size) for char in text]
    total_width = sum(widths) + max(0, len(text) - 1) * tracking
    cursor = x
    if align == "center":
        cursor -= total_width / 2
    elif align == "right":
        cursor -= total_width

    for char, width in zip(text, widths):
        c.drawString(cursor, y, char)
        cursor += width + tracking


def draw_sun_mark(c, x, y, radius):
    c.saveState()
    c.setStrokeColor(SUN)
    c.setLineWidth(1.15)
    c.circle(x, y, radius * 0.42, stroke=1, fill=0)
    for angle in range(0, 360, 45):
        import math

        radians = math.radians(angle)
        x1 = x + math.cos(radians) * radius * 0.68
        y1 = y + math.sin(radians) * radius * 0.68
        x2 = x + math.cos(radians) * radius
        y2 = y + math.sin(radians) * radius
        c.line(x1, y1, x2, y2)
    c.restoreState()


def draw_review_sign(c):
    width, height = A5_WIDTH, A5_HEIGHT
    header_height = 52 * mm
    footer_height = 16 * mm

    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    header_y = height - header_height
    c.drawImage(
        str(HEADER_PATH),
        0,
        header_y,
        width=width,
        height=header_height,
        preserveAspectRatio=True,
        mask="auto",
    )

    c.setStrokeColor(Color(1, 1, 1, alpha=0.42))
    c.setLineWidth(0.65)
    c.line(12 * mm, height - 12 * mm, width - 12 * mm, height - 12 * mm)

    draw_spaced_text(
        c,
        "RLD",
        13 * mm,
        height - 27 * mm,
        "RLD-Sans-Bold",
        24,
        WHITE,
        2.6,
    )
    draw_spaced_text(
        c,
        "RESORT",
        13.3 * mm,
        height - 34 * mm,
        "RLD-Sans",
        8.5,
        WHITE,
        2.0,
    )
    draw_spaced_text(
        c,
        "POLANGYUTA, SIQUIJOR",
        width - 13 * mm,
        height - 31 * mm,
        "RLD-Sans-Bold",
        7.4,
        WHITE,
        0.7,
        align="right",
    )
    draw_spaced_text(
        c,
        "ISLA DEL FUEGO",
        width - 13 * mm,
        height - 36.5 * mm,
        "RLD-Sans",
        6.9,
        SUN,
        1.3,
        align="right",
    )
    draw_sun_mark(c, width - 18 * mm, height - 19.5 * mm, 4.5 * mm)

    c.setFillColor(CORAL)
    c.rect(0, header_y - 1.6 * mm, 44 * mm, 1.6 * mm, stroke=0, fill=1)
    c.setFillColor(SUN)
    c.rect(44 * mm, header_y - 1.6 * mm, width - 44 * mm, 1.6 * mm, stroke=0, fill=1)

    content_top = header_y - 11 * mm
    draw_spaced_text(
        c,
        "ONE QUICK ISLAND FAVOR",
        width / 2,
        content_top,
        "RLD-Sans-Bold",
        7.7,
        CORAL,
        1.25,
        align="center",
    )

    c.setFillColor(INK)
    c.setFont("RLD-Serif-Bold", 23)
    c.drawCentredString(width / 2, content_top - 11 * mm, "How was your stay?")

    c.setFillColor(WATER)
    c.setFont("RLD-Serif", 10.5)
    c.drawCentredString(
        width / 2,
        content_top - 19 * mm,
        "Tell Google while the island glow is still fresh.",
    )

    panel_size = 82 * mm
    panel_x = (width - panel_size) / 2
    panel_y = footer_height + 27 * mm

    c.saveState()
    c.setFillAlpha(0.10)
    c.setFillColor(FOREST)
    c.roundRect(
        panel_x + 1.2 * mm,
        panel_y - 1.6 * mm,
        panel_size,
        panel_size,
        3.6 * mm,
        stroke=0,
        fill=1,
    )
    c.restoreState()

    c.setFillColor(WHITE)
    c.setStrokeColor(HexColor("#DDE6E1"))
    c.setLineWidth(0.75)
    c.roundRect(panel_x, panel_y, panel_size, panel_size, 3.6 * mm, stroke=1, fill=1)

    qr_inset = 5.5 * mm
    c.drawImage(
        str(QR_PATH),
        panel_x + qr_inset,
        panel_y + qr_inset,
        width=panel_size - 2 * qr_inset,
        height=panel_size - 2 * qr_inset,
        preserveAspectRatio=True,
        mask="auto",
    )

    label_y = panel_y - 7 * mm
    draw_spaced_text(
        c,
        "SCAN TO SHARE YOUR EXPERIENCE",
        width / 2,
        label_y,
        "RLD-Sans-Bold",
        7.6,
        FOREST,
        0.82,
        align="center",
    )

    c.setFillColor(INK)
    c.setFont("RLD-Sans", 8.2)
    c.drawCentredString(
        width / 2,
        label_y - 6 * mm,
        "Your honest review helps future guests find their way to RLD Resort.",
    )

    c.setFillColor(FOREST)
    c.rect(0, 0, width, footer_height, stroke=0, fill=1)
    c.setFillColor(SUN)
    c.setFont("RLD-Serif", 10.5)
    c.drawCentredString(width / 2, 9.3 * mm, "Leave a little island glow behind.")
    draw_spaced_text(
        c,
        "THANK YOU FOR BEING PART OF OUR STORY",
        width / 2,
        4.3 * mm,
        "RLD-Sans-Bold",
        5.7,
        WHITE,
        0.75,
        align="center",
    )


def create_pdf(path, page_size):
    page_width, page_height = page_size
    scale = page_width / A5_WIDTH
    c = canvas.Canvas(str(path), pagesize=page_size, pageCompression=1)
    c.setTitle("RLD Resort Google Review Sign")
    c.setAuthor("RLD Resort")
    c.setSubject("Printable Google review QR sign")
    c.saveState()
    c.scale(scale, scale)
    draw_review_sign(c)
    c.restoreState()
    c.showPage()
    c.save()


def main():
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    prepare_header_image()
    create_pdf(OUTPUT_DIR / "rld-resort-google-review-sign-a5.pdf", A5)
    create_pdf(OUTPUT_DIR / "rld-resort-google-review-sign-a4.pdf", A4)
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
