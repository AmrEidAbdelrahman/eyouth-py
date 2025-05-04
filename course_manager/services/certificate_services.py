
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os



class CertificateSeriveces:
    
    @staticmethod
    def generate_certificate(certificate):
        # Create a new image with a white background
        width = 3500  
        height = 2400
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)

        # Load fonts (you'll need to provide these font files in your project)
        try:
            title_font = ImageFont.truetype('DejaVuSerif-Bold.ttf', 120)
            main_font = ImageFont.truetype('DejaVuSerif.ttf', 80)
            subtitle_font = ImageFont.truetype('DejaVuSerif-Italic.ttf', 60)
        except OSError:
            # Fallback to default font if custom fonts are not available
            title_font = ImageFont.load_default(120)
            main_font = ImageFont.load_default(80)
            subtitle_font = ImageFont.load_default(60)

        # Add decorative border
        border_width = 20
        draw.rectangle(
            [(border_width, border_width), (width - border_width, height - border_width)],
            outline='#1f4068',
            width=border_width
        )

        # Add certificate title
        title = "Certificate of Completion"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(
            ((width - title_width) / 2, 300),
            title,
            font=title_font,
            fill='#1f4068'
        )

        # Add student name
        student_name = certificate.enrollment.student.get_full_name()
        if not student_name:
            student_name = certificate.enrollment.student.email
        student_text = f"This is to certify that\n{student_name}"
        text_bbox = draw.multiline_textbbox((0, 0), student_text, font=main_font, align='center', stroke_width=10)
        text_width = (text_bbox[2] - text_bbox[0])
        draw.multiline_text(
            ((width - text_width) / 2, 700),
            student_text,
            font=main_font,
            fill='#1b1b2f',
            align='center'
        )

        # Add course completion text
        course_name = certificate.enrollment.course.title
        completion_text = f"has successfully completed the course\n{course_name}"
        completion_bbox = draw.multiline_textbbox((0, 0), completion_text, font=main_font, align='center', spacing=5)
        completion_width = completion_bbox[2] - completion_bbox[0]
        draw.multiline_text(
            ((width - completion_width) / 2, 1000),
            completion_text,
            font=main_font,
            fill='#1b1b2f',
            align='center'
        )

        # Add completion date
        completion_date = certificate.enrollment.completed_at.strftime("%B %d, %Y")
        date_text = f"Completed on {completion_date}"
        date_bbox = draw.textbbox((0, 0), date_text, font=subtitle_font, stroke_width=5)
        date_width = (date_bbox[2] - date_bbox[0])
        draw.text(
            ((width - date_width) / 2, 1400),
            date_text,
            font=subtitle_font,
            fill='#1b1b2f'
        )

        # Save the certificate
        certificate_path = f'certificates/{certificate.enrollment.student.id}_{certificate.enrollment.course.id}_certificate.pdf'
        full_path = os.path.join(settings.MEDIA_ROOT, certificate_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        image.save(full_path, 'PDF', resolution=300.0)
        
        # Update certificate file field
        certificate.certificate_file.name = certificate_path
        certificate.save()
