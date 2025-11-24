#!/usr/bin/env python3
"""
Script to scan body parts directories and generate a manifest JSON file
This script scans ALL image files in each category folder without checking names.
Usage: python3 generate_parts_manifest.py
"""

import os
import json

# Base paths
BASE_PATH = "assets/image"
FILM_PATH = os.path.join(BASE_PATH, "parti_estratte_film")
AI_PATH = os.path.join(BASE_PATH, "parti_estratte_ai")

# Categories to scan
CATEGORIES = ["head", "eyes", "chest", "arms", "hand", "foot"]

# Supported image extensions
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')

def scan_directory(base_path, category):
    """Scan a category directory and return ALL image files"""
    category_path = os.path.join(base_path, category)
    
    if not os.path.exists(category_path):
        print(f"⚠️  Directory not found: {category_path}")
        return []
    
    images = []
    try:
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Check if it's an image file (by extension only)
            if filename.lower().endswith(IMAGE_EXTENSIONS):
                images.append(filename)
                
    except Exception as e:
        print(f"❌ Error scanning {category_path}: {e}")
        return []
    
    return sorted(images)

def generate_manifest():
    """Generate complete manifest of all body parts"""
    manifest = {
        "film": {},
        "ai": {}
    }
    
    print("\n" + "="*60)
    print("  SCANNING FILM PARTS")
    print("="*60)
    for category in CATEGORIES:
        images = scan_directory(FILM_PATH, category)
        manifest["film"][category] = images
        print(f"  ✓ {category:8s} → {len(images):3d} images")
    
    print("\n" + "="*60)
    print("  SCANNING AI PARTS")
    print("="*60)
    for category in CATEGORIES:
        images = scan_directory(AI_PATH, category)
        manifest["ai"][category] = images
        print(f"  ✓ {category:8s} → {len(images):3d} images")
    
    return manifest

def main():
    print("\n" + "="*60)
    print("  BODY PARTS MANIFEST GENERATOR")
    print("="*60)
    print("\n📁 Scanning directories for image files...")
    print("   (All image files will be included, regardless of name)")
    
    # Generate manifest
    manifest = generate_manifest()
    
    # Calculate totals
    total_film = sum(len(images) for images in manifest["film"].values())
    total_ai = sum(len(images) for images in manifest["ai"].values())
    
    print("\n" + "="*60)
    print(f"  📊 SUMMARY")
    print("="*60)
    print(f"  Film parts:  {total_film:4d}")
    print(f"  AI parts:    {total_ai:4d}")
    print(f"  Total:       {total_film + total_ai:4d}")
    print("="*60)
    
    # Save to JSON
    output_file = "assets/parts_manifest.json"
    
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Manifest saved to: {output_file}")
    print("\n💡 You can now use this file in your web application!")
    print("   Just make sure the HTML file can access it.\n")

if __name__ == "__main__":
    main()