#!/usr/bin/env python3
"""
Color Analysis Tool for HeartLine Logo Images
Analyzes the dominant colors in HrF-nbg.png and HeartLine-nbg.png
"""

import os
from PIL import Image
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def rgb_to_hex(rgb):
    """Convert RGB values to hex color code"""
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def analyze_image_colors(image_path, n_colors=10):
    """
    Analyze the dominant colors in an image
    
    Args:
        image_path (str): Path to the image file
        n_colors (int): Number of dominant colors to extract
    
    Returns:
        dict: Analysis results including dominant colors, percentages, and hex codes
    """
    try:
        # Open and convert image to RGB
        img = Image.open(image_path).convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Get image dimensions
        height, width, channels = img_array.shape
        total_pixels = height * width
        
        # Reshape for clustering
        pixels = img_array.reshape(-1, 3)
        
        # Remove transparent/white background pixels (if any)
        # Filter out very light colors (likely background)
        non_white_pixels = pixels[np.sum(pixels, axis=1) < 750]  # Adjust threshold as needed
        
        if len(non_white_pixels) == 0:
            non_white_pixels = pixels  # Use all pixels if no filtering needed
        
        # Use KMeans to find dominant colors
        kmeans = KMeans(n_clusters=min(n_colors, len(non_white_pixels)), random_state=42, n_init=10)
        kmeans.fit(non_white_pixels)
        
        # Get the colors and their frequencies
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        # Count frequency of each cluster
        color_counts = Counter(labels)
        
        # Calculate percentages
        total_analyzed_pixels = len(non_white_pixels)
        
        results = []
        for i, color in enumerate(colors):
            count = color_counts[i]
            percentage = (count / total_analyzed_pixels) * 100
            hex_color = rgb_to_hex(color)
            
            results.append({
                'rgb': tuple(color.astype(int)),
                'hex': hex_color,
                'percentage': percentage,
                'pixel_count': count
            })
        
        # Sort by percentage (most dominant first)
        results.sort(key=lambda x: x['percentage'], reverse=True)
        
        return {
            'image_path': image_path,
            'image_size': (width, height),
            'total_pixels': total_pixels,
            'analyzed_pixels': total_analyzed_pixels,
            'colors': results
        }
        
    except Exception as e:
        return {'error': f"Error analyzing {image_path}: {str(e)}"}

def create_color_palette_visualization(analysis_results, output_path=None):
    """Create a visual representation of the color palette"""
    if 'error' in analysis_results:
        print(f"Cannot create visualization: {analysis_results['error']}")
        return
    
    colors = analysis_results['colors'][:8]  # Top 8 colors
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Color swatches
    color_swatches = []
    color_labels = []
    percentages = []
    
    for color_data in colors:
        rgb_normalized = [c/255.0 for c in color_data['rgb']]
        color_swatches.append(rgb_normalized)
        color_labels.append(color_data['hex'])
        percentages.append(color_data['percentage'])
    
    # Create color bar
    ax1.imshow([color_swatches], aspect='auto')
    ax1.set_xlim(-0.5, len(color_swatches) - 0.5)
    ax1.set_ylim(-0.5, 0.5)
    ax1.set_xticks(range(len(color_swatches)))
    ax1.set_xticklabels([f"{hex_code}\n{perc:.1f}%" for hex_code, perc in zip(color_labels, percentages)])
    ax1.set_yticks([])
    ax1.set_title(f"Dominant Colors - {os.path.basename(analysis_results['image_path'])}", fontsize=14, fontweight='bold')
    
    # Percentage bar chart
    bars = ax2.bar(range(len(colors)), percentages, color=color_swatches)
    ax2.set_xlabel('Color Index')
    ax2.set_ylabel('Percentage (%)')
    ax2.set_title('Color Distribution')
    ax2.set_xticks(range(len(colors)))
    ax2.set_xticklabels([f"{i+1}" for i in range(len(colors))])
    
    # Add percentage labels on bars
    for bar, percentage in zip(bars, percentages):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{percentage:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Color palette saved to: {output_path}")
    
    plt.show()

def print_color_analysis(analysis_results):
    """Print detailed color analysis results"""
    if 'error' in analysis_results:
        print(f"Error: {analysis_results['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"COLOR ANALYSIS: {os.path.basename(analysis_results['image_path'])}")
    print(f"{'='*60}")
    print(f"Image Size: {analysis_results['image_size'][0]} x {analysis_results['image_size'][1]} pixels")
    print(f"Total Pixels: {analysis_results['total_pixels']:,}")
    print(f"Analyzed Pixels: {analysis_results['analyzed_pixels']:,}")
    print(f"\nDOMINANT COLORS:")
    print(f"{'Rank':<4} {'Hex Code':<8} {'RGB Values':<15} {'Percentage':<12} {'CSS/Design Use'}")
    print(f"{'-'*70}")
    
    css_suggestions = [
        "Primary Brand Color",
        "Secondary Color", 
        "Accent Color",
        "Background Color",
        "Text Color",
        "Border Color",
        "Hover State",
        "Gradient Color"
    ]
    
    for i, color_data in enumerate(analysis_results['colors'][:8]):
        rgb_str = f"({color_data['rgb'][0]}, {color_data['rgb'][1]}, {color_data['rgb'][2]})"
        suggestion = css_suggestions[i] if i < len(css_suggestions) else "Additional Color"
        
        print(f"{i+1:<4} {color_data['hex']:<8} {rgb_str:<15} {color_data['percentage']:<11.1f}% {suggestion}")

def main():
    """Main function to analyze both logo images"""
    # Image paths
    base_path = r"d:\projects\Hearline Webapp\static\img"
    images = [
        os.path.join(base_path, "HrF-nbg.png"),
        os.path.join(base_path, "HeartLine-nbg.png")
    ]
    
    all_results = []
    
    print("HeartLine Logo Color Analysis")
    print("="*50)
    
    for img_path in images:
        if os.path.exists(img_path):
            print(f"\nAnalyzing: {os.path.basename(img_path)}")
            results = analyze_image_colors(img_path, n_colors=8)
            all_results.append(results)
            print_color_analysis(results)
            
            # Create visualization
            output_viz = img_path.replace('.png', '_color_palette.png')
            create_color_palette_visualization(results, output_viz)
            
        else:
            print(f"Image not found: {img_path}")
    
    # Generate CSS color variables
    print(f"\n{'='*60}")
    print("SUGGESTED CSS COLOR VARIABLES")
    print(f"{'='*60}")
    
    for i, results in enumerate(all_results):
        if 'error' not in results:
            img_name = os.path.basename(results['image_path']).replace('-nbg.png', '').replace('.png', '')
            print(f"\n/* Colors from {img_name} */")
            
            for j, color_data in enumerate(results['colors'][:5]):  # Top 5 colors
                var_name = f"--{img_name.lower()}-color-{j+1}"
                print(f"{var_name}: {color_data['hex']};  /* RGB{color_data['rgb']} - {color_data['percentage']:.1f}% */")

if __name__ == "__main__":
    main()
