from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "output" / "pdf"

BACKGROUND_PATH = IMAGE_DIR / "rld-review-sign-background-vintage.png"
LOGO_SOURCE_PATH = IMAGE_DIR / "Resort-main-logo.jpg"
LOGO_PATH = IMAGE_DIR / "rld-resort-logo-polangyuta.png"
QR_PATH = IMAGE_DIR / "rld-resort-google-review-qr.png"

FONT_DIR = Path("C:/Windows/Fonts")

TERRACOTTA = HexColor("#A84F2E")
TERRACOTTA_DARK = HexColor("#8F3F25")
CHARCOAL = HexColor("#3E3E3E")
PAPER = HexColor("#FBF6EC")
PANEL = HexColor("#FFF9F2")
CREAM_INK = (246, 214, 193, 255)
LOGO_BG = (164, 79, 48, 255)

A5_WIDTH, A5_HEIGHT = A5


def register_fonts():
    fonts = {
        "RLD-Sans": FONT_DIR / "arial.ttf",
        "RLD-Sans-Bold": FONT_DIR / "arialbd.ttf",
        "RLD-Garamond": FONT_DIR / "GARA.TTF",
        "RLD-Garamond-Bold": FONT_DIR / "GARABD.TTF",
        "RLD-Script": FONT_DIR / "segoesc.ttf",
    }
    for name, path in fonts.items():
        if not path.exists():
            raise FileNotFoundError(f"Required font not found: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))


def centered_pillow_text(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill, anchor="mm")


def centered_spaced_pillow_text(draw, center_x, y, text, font, fill, tracking):
    widths = [draw.textlength(character, font=font) for character in text]
    total_width = sum(widths) + tracking * max(0, len(text) - 1)
    cursor = center_x - total_width / 2
    for character, width in zip(text, widths):
        draw.text((cursor, y), character, font=font, fill=fill, anchor="lm")
        cursor += width + tracking


def create_corrected_logo():
    with Image.open(LOGO_SOURCE_PATH) as source:
        source = source.convert("RGB")
        # Keep only the resort-house illustration from the original raster logo.
        # The lettering and oval are rebuilt below so they stay clean at print size.
        artwork = source.crop((145, 132, 355, 304))

    artwork = artwork.resize((770, 630), Image.Resampling.LANCZOS)
    artwork_mask = artwork.convert("L").point(
        lambda value: max(0, min(255, (value - 108) * 4))
    )
    artwork_mask = artwork_mask.filter(ImageFilter.GaussianBlur(radius=0.45))
    artwork_layer = Image.new("RGBA", artwork.size, CREAM_INK)
    artwork_layer.putalpha(artwork_mask)

    logo = Image.new("RGBA", (1370, 1900), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    draw.rounded_rectangle(
        (45, 45, 1325, 1855),
        radius=620,
        fill=LOGO_BG,
        outline=CREAM_INK,
        width=11,
    )
    draw.rounded_rectangle(
        (95, 95, 1275, 1805),
        radius=570,
        outline=CREAM_INK,
        width=5,
    )

    rld_font = ImageFont.truetype(str(FONT_DIR / "arial.ttf"), 152)
    centered_spaced_pillow_text(draw, 685, 235, "RLD", rld_font, CREAM_INK, 34)
    logo.alpha_composite(artwork_layer, (300, 405))

    location_font = ImageFont.truetype(str(FONT_DIR / "arialbd.ttf"), 48)
    established_font = ImageFont.truetype(str(FONT_DIR / "arial.ttf"), 42)
    centered_pillow_text(draw, (685, 1125), "POLANGYUTA,", location_font, CREAM_INK)
    centered_pillow_text(draw, (685, 1220), "SIQUIJOR PH", location_font, CREAM_INK)
    centered_pillow_text(draw, (685, 1325), "EST. 2024", established_font, CREAM_INK)

    resort_font = ImageFont.truetype(str(FONT_DIR / "arial.ttf"), 112)
    centered_spaced_pillow_text(
        draw,
        685,
        1545,
        "RESORT",
        resort_font,
        CREAM_INK,
        34,
    )
    logo.save(LOGO_PATH, optimize=True)


def draw_wave(c, center_x, y, width, amplitude, color, line_width=1.0):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(line_width)
    path = c.beginPath()
    path.moveTo(center_x - width / 2, y)
    segment = width / 4
    path.curveTo(
        center_x - width / 2 + segment * 0.35,
        y + amplitude,
        center_x - width / 2 + segment * 0.65,
        y + amplitude,
        center_x - width / 2 + segment,
        y,
    )
    path.curveTo(
        center_x - width / 2 + segment * 1.35,
        y - amplitude,
        center_x - width / 2 + segment * 1.65,
        y - amplitude,
        center_x,
        y,
    )
    path.curveTo(
        center_x + segment * 0.35,
        y + amplitude,
        center_x + segment * 0.65,
        y + amplitude,
        center_x + segment,
        y,
    )
    path.curveTo(
        center_x + segment * 1.35,
        y - amplitude,
        center_x + segment * 1.65,
        y - amplitude,
        center_x + width / 2,
        y,
    )
    c.drawPath(path, stroke=1, fill=0)
    c.restoreState()


def draw_divider(c, y):
    c.saveState()
    c.setStrokeColor(TERRACOTTA)
    c.setLineWidth(0.85)
    c.line(A5_WIDTH / 2 - 57 * mm, y, A5_WIDTH / 2 - 24 * mm, y)
    c.line(A5_WIDTH / 2 + 24 * mm, y, A5_WIDTH / 2 + 57 * mm, y)
    for offset in (2.4 * mm, 0, -2.4 * mm):
        draw_wave(c, A5_WIDTH / 2, y + offset, 18 * mm, 1.35 * mm, TERRACOTTA, 0.85)
    c.restoreState()


def draw_star(c, center_x, center_y, radius):
    import math

    points = []
    for index in range(10):
        angle = math.radians(90 + index * 36)
        point_radius = radius if index % 2 == 0 else radius * 0.43
        points.append(
            (
                center_x + math.cos(angle) * point_radius,
                center_y + math.sin(angle) * point_radius,
            )
        )

    path = c.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    path.close()
    c.drawPath(path, stroke=1, fill=0)


def draw_review_icon(c, center_x, center_y):
    c.saveState()
    c.setFillColor(TERRACOTTA)
    c.circle(center_x, center_y, 5.2 * mm, stroke=0, fill=1)
    c.setStrokeColor(PAPER)
    c.setLineWidth(1.25)
    draw_star(c, center_x, center_y + 0.15 * mm, 2.85 * mm)
    c.restoreState()


def draw_palm_mark(c, center_x, y):
    c.saveState()
    c.setStrokeColor(TERRACOTTA)
    c.setLineWidth(1.0)
    crown_y = y + 7.6 * mm

    trunk = c.beginPath()
    trunk.moveTo(center_x - 0.35 * mm, y)
    trunk.curveTo(
        center_x - 0.1 * mm,
        y + 2.5 * mm,
        center_x + 0.65 * mm,
        y + 5.4 * mm,
        center_x,
        crown_y,
    )
    c.drawPath(trunk, stroke=1, fill=0)

    fronds = (
        (-5.0, 3.6, -2.3, 1.4),
        (-4.0, 6.1, -2.1, 2.4),
        (-1.8, 8.6, -0.8, 3.2),
        (2.0, 8.7, 0.9, 3.2),
        (4.2, 6.0, 2.2, 2.4),
        (5.2, 3.5, 2.5, 1.4),
    )
    for end_x, end_y, control_x, control_y in fronds:
        frond = c.beginPath()
        frond.moveTo(center_x, crown_y)
        frond.curveTo(
            center_x + control_x * mm,
            crown_y + control_y * mm,
            center_x + end_x * 0.8 * mm,
            y + end_y * mm,
            center_x + end_x * mm,
            y + end_y * mm,
        )
        c.drawPath(frond, stroke=1, fill=0)
    c.restoreState()


def draw_background(c):
    c.drawImage(
        str(BACKGROUND_PATH),
        0,
        0,
        width=A5_WIDTH,
        height=A5_HEIGHT,
        preserveAspectRatio=False,
        mask="auto",
    )
    c.saveState()
    c.setStrokeColor(TERRACOTTA_DARK)
    c.setLineWidth(0.75)
    inset_outer = 4.1 * mm
    inset_inner = 5.6 * mm
    c.rect(
        inset_outer,
        inset_outer,
        A5_WIDTH - 2 * inset_outer,
        A5_HEIGHT - 2 * inset_outer,
        stroke=1,
        fill=0,
    )
    c.setLineWidth(0.35)
    c.rect(
        inset_inner,
        inset_inner,
        A5_WIDTH - 2 * inset_inner,
        A5_HEIGHT - 2 * inset_inner,
        stroke=1,
        fill=0,
    )
    c.restoreState()


def draw_review_sign(c):
    draw_background(c)

    logo_height = 45 * mm
    logo_width = logo_height * (1370 / 1900)
    c.drawImage(
        str(LOGO_PATH),
        (A5_WIDTH - logo_width) / 2,
        A5_HEIGHT - 8.5 * mm - logo_height,
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
        mask="auto",
    )

    c.setFillColor(TERRACOTTA)
    c.setFont("RLD-Garamond", 47)
    c.drawCentredString(A5_WIDTH / 2, A5_HEIGHT - 69 * mm, "Enjoyed")
    c.setFont("RLD-Garamond", 52)
    c.drawCentredString(A5_WIDTH / 2, A5_HEIGHT - 86 * mm, "your stay?")

    divider_y = A5_HEIGHT - 97 * mm
    draw_divider(c, divider_y)

    c.setFillColor(CHARCOAL)
    c.setFont("RLD-Sans-Bold", 9.4)
    c.drawCentredString(
        A5_WIDTH / 2,
        A5_HEIGHT - 106.5 * mm,
        "We'd love to hear about your experience at RLD Resort.",
    )

    c.setFont("RLD-Sans-Bold", 10.0)
    call_to_action = "SCAN TO LEAVE US A GOOGLE REVIEW"
    text_width = pdfmetrics.stringWidth(call_to_action, "RLD-Sans-Bold", 10.0)
    icon_diameter = 10.4 * mm
    gap = 3.5 * mm
    group_width = icon_diameter + gap + text_width
    group_x = (A5_WIDTH - group_width) / 2
    cta_center_y = A5_HEIGHT - 113.5 * mm
    draw_review_icon(c, group_x + icon_diameter / 2, cta_center_y)
    c.drawString(
        group_x + icon_diameter + gap,
        cta_center_y - 1.8 * mm,
        call_to_action,
    )

    panel_size = 60 * mm
    panel_x = (A5_WIDTH - panel_size) / 2
    panel_y = 29 * mm
    c.saveState()
    c.setFillColor(PANEL)
    c.setStrokeColor(TERRACOTTA)
    c.setLineWidth(0.9)
    c.roundRect(
        panel_x,
        panel_y,
        panel_size,
        panel_size,
        4.2 * mm,
        stroke=1,
        fill=1,
    )
    c.restoreState()

    qr_inset = 4.8 * mm
    c.drawImage(
        str(QR_PATH),
        panel_x + qr_inset,
        panel_y + qr_inset,
        width=panel_size - 2 * qr_inset,
        height=panel_size - 2 * qr_inset,
        preserveAspectRatio=True,
        mask="auto",
    )

    ornament_y = 23 * mm
    c.saveState()
    c.setStrokeColor(TERRACOTTA)
    c.setLineWidth(0.65)
    c.line(A5_WIDTH / 2 - 31 * mm, ornament_y, A5_WIDTH / 2 - 9 * mm, ornament_y)
    c.line(A5_WIDTH / 2 + 9 * mm, ornament_y, A5_WIDTH / 2 + 31 * mm, ornament_y)
    c.restoreState()
    draw_palm_mark(c, A5_WIDTH / 2, 18 * mm)

    c.setFillColor(CHARCOAL)
    c.setFont("RLD-Script", 14.2)
    c.drawCentredString(A5_WIDTH / 2, 12.8 * mm, "Thank you for staying with us.")
    draw_wave(c, A5_WIDTH / 2, 7.4 * mm, 27 * mm, 1.5 * mm, TERRACOTTA, 1.15)


def create_pdf(path, page_size):
    page_width, _ = page_size
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
    create_corrected_logo()
    create_pdf(OUTPUT_DIR / "rld-resort-google-review-sign-a5.pdf", A5)
    create_pdf(OUTPUT_DIR / "rld-resort-google-review-sign-a4.pdf", A4)
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()
