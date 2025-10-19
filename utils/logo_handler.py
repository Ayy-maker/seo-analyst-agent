"""
Logo Handler - Add company logos to PDF reports
"""

from PIL import Image
import io
from pathlib import Path
from typing import Optional


class LogoHandler:
    """Handle logo loading, resizing, and placement"""
    
    @staticmethod
    def load_logo(logo_path: str, max_width: int = 200, max_height: int = 80) -> Optional[io.BytesIO]:
        """
        Load and resize logo for PDF
        
        Args:
            logo_path: Path to logo file (PNG, JPG, etc.)
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            
        Returns:
            BytesIO buffer with resized image, or None if file not found
        """
        logo_file = Path(logo_path)
        
        if not logo_file.exists():
            return None
        
        try:
            # Open image
            img = Image.open(logo_file)
            
            # Convert to RGBA if needed
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            
            # Calculate resize ratio
            width_ratio = max_width / img.width
            height_ratio = max_height / img.height
            ratio = min(width_ratio, height_ratio)
            
            # Resize if needed
            if ratio < 1:
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save to buffer
            buf = io.BytesIO()
            
            # Save as PNG with transparency
            if img.mode == 'RGBA':
                img.save(buf, format='PNG', optimize=True)
            else:
                img.save(buf, format='PNG', optimize=True)
            
            buf.seek(0)
            return buf
            
        except Exception as e:
            print(f"Warning: Could not load logo from {logo_path}: {e}")
            return None
    
    @staticmethod
    def create_placeholder_logo(width: int = 200, height: int = 80) -> io.BytesIO:
        """
        Create a simple placeholder logo
        
        Args:
            width: Width in pixels
            height: Height in pixels
            
        Returns:
            BytesIO buffer with placeholder image
        """
        # Create gradient placeholder
        img = Image.new('RGBA', (width, height), (102, 126, 234, 255))
        
        # Save to buffer
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return buf
