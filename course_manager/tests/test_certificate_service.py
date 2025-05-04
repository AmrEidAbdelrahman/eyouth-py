import pytest
import os
from unittest.mock import patch, MagicMock
from PIL import Image, ImageDraw
from django.conf import settings
from datetime import datetime
from course_manager.services.certificate_services import CertificateSeriveces
from course_manager.models import Certificate


@pytest.mark.django_db
class TestCertificateService:
    
    @patch('course_manager.services.certificate_services.Image')
    @patch('course_manager.services.certificate_services.ImageDraw')
    @patch('course_manager.services.certificate_services.ImageFont')
    def test_generate_certificate(self, mock_font, mock_draw, mock_image, certificate):
        """Test that a certificate can be generated successfully"""
        # Setup mocks
        mock_image_instance = MagicMock()
        mock_image.new.return_value = mock_image_instance
        
        mock_draw_instance = MagicMock()
        mock_draw.Draw.return_value = mock_draw_instance
        mock_draw_instance.textbbox.return_value = (0, 0, 100, 50)
        mock_draw_instance.multiline_textbbox.return_value = (0, 0, 100, 50)
        
        # Mock font loading
        mock_font.truetype.return_value = MagicMock()
        
        # Set a fixed completed_at date for the enrollment
        certificate.enrollment.completed_at = datetime(2023, 5, 15)
        certificate.enrollment.save()
        
        # Apply certificate generation
        with patch('os.makedirs') as mock_makedirs, patch('builtins.open', MagicMock()):
            CertificateSeriveces.generate_certificate(certificate)
            
            # Verify directories were created
            mock_makedirs.assert_called_once()
            
            # Verify the image was saved
            mock_image_instance.save.assert_called_once()
            
            # Verify certificate path was updated
            assert certificate.certificate_file.name is not None
            assert f'certificates/{certificate.enrollment.student.id}_{certificate.enrollment.course.id}_certificate.pdf' in certificate.certificate_file.name
    
    @patch('course_manager.services.certificate_services.ImageFont')
    def test_font_fallback(self, mock_font, certificate):
        """Test that the service falls back to default font if custom fonts aren't available"""
        # Setup font exception
        mock_font.truetype.side_effect = OSError("Font not found")
        mock_font.load_default.return_value = MagicMock()
        
        # Create mocks for the rest of the required components
        with patch('course_manager.services.certificate_services.Image') as mock_image, \
             patch('course_manager.services.certificate_services.ImageDraw') as mock_draw, \
             patch('os.makedirs'), \
             patch('builtins.open', MagicMock()):
            
            # Setup image and draw mocks
            mock_image_instance = MagicMock()
            mock_image.new.return_value = mock_image_instance
            
            mock_draw_instance = MagicMock()
            mock_draw.Draw.return_value = mock_draw_instance
            mock_draw_instance.textbbox.return_value = (0, 0, 100, 50)
            mock_draw_instance.multiline_textbbox.return_value = (0, 0, 100, 50)
            
            # Set a completed_at date
            certificate.enrollment.completed_at = datetime(2023, 5, 15)
            certificate.enrollment.save()
            
            # Apply certificate generation
            CertificateSeriveces.generate_certificate(certificate)
            
            # Verify fallback fonts were used
            mock_font.load_default.assert_called()
            
    def test_certificate_file_naming(self, certificate):
        """Test that certificate file is named according to the expected format"""
        # Create mock image
        mock_image = MagicMock()
        
        # Set up patching for PIL.Image
        with patch('course_manager.services.certificate_services.Image') as mock_image_class, \
             patch('course_manager.services.certificate_services.ImageDraw'), \
             patch('course_manager.services.certificate_services.ImageFont'), \
             patch('os.makedirs'):
            
            # Setup image mock
            mock_image_instance = MagicMock()
            mock_image_class.new.return_value = mock_image_instance
            
            # Set a completed_at date
            certificate.enrollment.completed_at = datetime(2023, 5, 15)
            certificate.enrollment.save()
            
            # Apply certificate generation
            CertificateSeriveces.generate_certificate(certificate)
            
            # Check file naming convention
            expected_filename = f'certificates/{certificate.enrollment.student.id}_{certificate.enrollment.course.id}_certificate.pdf'
            assert certificate.certificate_file.name == expected_filename 
