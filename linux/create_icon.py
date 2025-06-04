#!/usr/bin/env python3
"""
Create application icon for Linux desktop integration
"""
from PIL import Image, ImageDraw
import os

def create_linux_icon():
    """Create a professional icon for Linux applications."""
    # Create different sizes for different contexts
    sizes = [16, 22, 24, 32, 48, 64, 128, 256, 512]
    
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background circle with gradient effect
        margin = max(2, size // 16)
        circle_color = (41, 128, 185)  # Professional blue
        draw.ellipse([margin, margin, size-margin, size-margin], 
                   fill=circle_color, outline=(52, 152, 219), width=max(1, size//64))
        
        # Route path (simplified for smaller sizes)
        if size >= 24:
            path_margin = size // 4
            line_width = max(1, size // 32)
            
            # Main route line
            points = [
                (path_margin, size//2),
                (size//3, path_margin + size//6),
                (2*size//3, path_margin + size//6), 
                (size-path_margin, size//2),
                (2*size//3, size-path_margin - size//6),
                (size//3, size-path_margin - size//6),
                (path_margin, size//2)
            ]
            
            # Draw route path
            for i in range(len(points)-1):
                draw.line([points[i], points[i+1]], fill=(255, 255, 255), width=line_width*2)
        
        # Start and end points
        point_size = max(2, size//12)
        # Start point (red)
        draw.ellipse([margin*2, size//2-point_size//2, 
                    margin*2+point_size, size//2+point_size//2], 
                   fill=(231, 76, 60))
        # End point (green)  
        draw.ellipse([size-margin*2-point_size, size//2-point_size//2,
                    size-margin*2, size//2+point_size//2], 
                   fill=(46, 204, 113))
        
        # Save icon
        icon_dir = f"linux/icons/hicolor/{size}x{size}/apps"
        os.makedirs(icon_dir, exist_ok=True)
        img.save(f"{icon_dir}/route-planner.png", "PNG")
    
    print("✅ Linux icons created successfully!")

if __name__ == "__main__":
    create_linux_icon()
