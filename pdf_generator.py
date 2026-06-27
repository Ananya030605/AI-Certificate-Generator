import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

def get_font(size, bold=False):
    font_names = ["arialbd.ttf", "Arial-Bold.ttf", "Helvetica-Bold"] if bold else ["arial.ttf", "Arial.ttf", "Helvetica"]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except IOError:
            continue
    return ImageFont.load_default()

def fit_font(draw, text, max_width, size, bold=False):
    while size > 1:
        font = get_font(size, bold)
        box = draw.textbbox((0, 0), text, font=font)
        text_width = box[2] - box[0]
        if text_width <= max_width:
            return font
        size -= 1
    return get_font(15, bold)

def create_certificate(name, course, cert_type, organization, date, message):
    os.makedirs("output", exist_ok=True)
    
    template_path = "templates/certificate.png"
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Missing template background! Please place your image file at: '{template_path}'")
        
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # --- 1. FONTS SETUP ---
    type_font = fit_font(draw, cert_type, width * 0.7, 38, bold=True)
    name_font = fit_font(draw, name, width * 0.65, 70, bold=True)
    course_font = fit_font(draw, course, width * 0.65, 42, bold=True)
    
    sub_font = get_font(22, bold=False)       
    info_font = get_font(20, bold=True)       

    # --- 2. CLEAN UP THE AI MESSAGE ---
    # If the AI message contains multiple lines (duplicating the layout), 
    # we only take the actual custom sentence at the end.
    clean_message = ""
    if message:
        lines = [line.strip() for line in message.split('\n') if line.strip()]
        # Filter out lines that duplicate our main headers
        filtered_lines = [
            l for l in lines if not any(
                keyword in l.lower() for keyword in 
                [name.lower(), course.lower(), organization.lower(), "presented to", "completing", "organized by", "achievement"]
            )
        ]
        # Use the last remaining clean sentence
        if filtered_lines:
            clean_message = filtered_lines[-1]
        else:
            clean_message = "This certificate is awarded for outstanding performance and successful completion."

    # --- 3. DRAW EXPLICIT LAYOUT FIELDS (NO MORE OVERLAPS) ---

    # Header type (e.g., Certificate of Achievement)
    draw.text((width // 2, height * 0.26), cert_type, font=type_font, anchor="mm", fill="#b8860b")

    # Presentation Line
    draw.text((width // 2, height * 0.34), "This certificate is proudly presented to", font=sub_font, anchor="mm", fill="#333333")

    # Participant Name
    draw.text((width // 2, height * 0.43), name, font=name_font, anchor="mm", fill="black")

    # Connector Line
    draw.text((width // 2, height * 0.51), "for successfully completing", font=sub_font, anchor="mm", fill="#333333")

    # Course / Achievement Name
    draw.text((width // 2, height * 0.58), course, font=course_font, anchor="mm", fill="black")

    # Center Organization Title
    draw.text((width // 2, height * 0.65), "Organized by:", font=get_font(18, bold=False), anchor="mm", fill="#555555")
    draw.text((width // 2, height * 0.69), organization, font=get_font(22, bold=True), anchor="mm", fill="black")

    # Left Alignment Line: Date Field
    draw.text((width * 0.18, height * 0.79), date, font=info_font, anchor="mm", fill="black")

    # Right Alignment Line: Organiser Field
    draw.text((width * 0.82, height * 0.79), organization, font=info_font, anchor="mm", fill="black")

    # 4. Clean Additional Message (Sits safely at the very bottom below everything)
    if clean_message:
        msg_font = fit_font(draw, clean_message, width * 0.8, 18, bold=False)
        draw.text((width // 2, height * 0.88), clean_message, font=msg_font, anchor="mm", fill="#444444")

    # --- 4. EXPORT MANAGEMENT ---
    output_png = "output/certificate.png"
    if os.path.exists(output_png):
        os.remove(output_png)
    img.save(output_png)
    
    return width, height

def convert_pdf(img_width, img_height):
    pdf = canvas.Canvas("output/certificate.pdf", pagesize=(img_width, img_height))
    pdf.drawImage("output/certificate.png", 0, 0, width=img_width, height=img_height)
    pdf.save()