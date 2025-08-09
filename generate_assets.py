#!/usr/bin/env python3
"""
Generate visual assets for CTL project
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Ensure assets directory exists
os.makedirs("assets/images", exist_ok=True)

def create_symbol_1_data_flow():
    """Create Symbol 1: Data Flow Network Symbol"""
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    
    # Central hub (CTL)
    center = Circle((5, 5), 1.5, facecolor='#2E86AB', edgecolor='#1B5E7E', linewidth=3, alpha=0.9)
    ax.add_patch(center)
    ax.text(5, 5, 'CTL', ha='center', va='center', fontsize=16, fontweight='bold', color='white')
    
    # Data sources (connectors)
    sources = [
        (2, 8, 'SQL', '#F24236'),
        (8, 8, 'CSV', '#F6AE2D'),
        (2, 2, 'API', '#2F9599'),
        (8, 2, 'DB', '#F26419')
    ]
    
    for x, y, label, color in sources:
        source = Circle((x, y), 0.8, facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(source)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Draw arrows to center
        ax.annotate('', xy=(5, 5), xytext=(x, y),
                   arrowprops=dict(arrowstyle='->', lw=2, color='#555555', alpha=0.7))
    
    # Output transformations
    outputs = [
        (5, 8.5, 'Transform', '#A663CC'),
        (1.5, 5, 'Analyze', '#4ECDC4'),
        (8.5, 5, 'Export', '#FFE66D'),
        (5, 1.5, 'Visualize', '#FF6B6B')
    ]
    
    for x, y, label, color in outputs:
        output = Rectangle((x-0.7, y-0.4), 1.4, 0.8, facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(output)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        
        # Draw arrows from center
        ax.annotate('', xy=(x, y), xytext=(5, 5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='#555555', alpha=0.7))
    
    ax.set_title('CTL Data Flow Network', fontsize=18, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('assets/images/symbol_1_data_flow.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated Symbol 1: Data Flow Network")


def create_symbol_2_transformation_pipeline():
    """Create Symbol 2: Transformation Pipeline Symbol"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    
    # Pipeline stages
    stages = [
        (1, 2, 'Input\nData', '#3498db'),
        (3, 2, 'Clean &\nNormalize', '#e74c3c'),
        (5, 2, 'Transform\n& Analyze', '#f39c12'),
        (7, 2, 'Aggregate\n& Calculate', '#27ae60'),
        (9, 2, 'Output\nResults', '#9b59b6')
    ]
    
    for i, (x, y, label, color) in enumerate(stages):
        # Create rounded rectangle
        box = FancyBboxPatch((x-0.6, y-0.6), 1.2, 1.2, 
                            boxstyle="round,pad=0.1", 
                            facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Add arrows between stages
        if i < len(stages) - 1:
            ax.annotate('', xy=(stages[i+1][0]-0.6, stages[i+1][1]), 
                       xytext=(x+0.6, y),
                       arrowprops=dict(arrowstyle='->', lw=3, color='#2c3e50', alpha=0.8))
    
    # Add CTL branding
    ax.text(5, 3.5, 'CTL Transformation Pipeline', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#2c3e50')
    
    # Add MCP integration indicator
    mcp_box = Rectangle((8.5, 0.2), 1, 0.6, facecolor='#8e44ad', edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(mcp_box)
    ax.text(9, 0.5, 'MCP', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('assets/images/symbol_2_pipeline.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated Symbol 2: Transformation Pipeline")


def create_symbol_3_data_ecosystem():
    """Create Symbol 3: Data Ecosystem Symbol"""
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    
    # Create layered ecosystem
    # Outer ring - Applications
    apps = [
        (5, 9, 'Excel'),
        (8.5, 7, 'Python'),
        (8.5, 3, 'R/Stata'),
        (5, 1, 'MATLAB'),
        (1.5, 3, 'Web Apps'),
        (1.5, 7, 'Jupyter')
    ]
    
    # Draw outer ecosystem ring
    outer_circle = Circle((5, 5), 4, fill=False, edgecolor='#34495e', linewidth=2, linestyle='--', alpha=0.6)
    ax.add_patch(outer_circle)
    
    for x, y, label in apps:
        app_circle = Circle((x, y), 0.7, facecolor='#3498db', edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(app_circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        
        # Draw connection lines to center
        ax.plot([x, 5], [y, 5], 'k--', alpha=0.3, linewidth=1)
    
    # Middle ring - APIs
    api_circle = Circle((5, 5), 2.5, fill=False, edgecolor='#e74c3c', linewidth=3, alpha=0.7)
    ax.add_patch(api_circle)
    ax.text(5, 7.3, 'REST API', ha='center', va='center', fontsize=11, fontweight='bold', color='#e74c3c')
    ax.text(5, 2.7, 'MCP Server', ha='center', va='center', fontsize=11, fontweight='bold', color='#e74c3c')
    
    # Core - CTL
    core = Circle((5, 5), 1.3, facecolor='#2E86AB', edgecolor='white', linewidth=3, alpha=0.9)
    ax.add_patch(core)
    ax.text(5, 5.3, 'CTL', ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    ax.text(5, 4.7, 'CORE', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    ax.set_title('CTL Data Ecosystem', fontsize=18, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('assets/images/symbol_3_ecosystem.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated Symbol 3: Data Ecosystem")


def create_architecture_diagram():
    """Create comprehensive architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    
    # Title
    ax.text(6, 7.5, 'CTL Architecture: REST API + MCP Integration', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Client Applications Layer (Top)
    clients = [
        (1.5, 6.5, 'Excel\nClients', '#3498db'),
        (3.5, 6.5, 'Python\nScripts', '#e74c3c'),
        (5.5, 6.5, 'R/Stata\nApps', '#f39c12'),
        (7.5, 6.5, 'Web\nApps', '#27ae60'),
        (9.5, 6.5, 'AI\nAssistants', '#9b59b6')
    ]
    
    for x, y, label, color in clients:
        box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8, 
                            boxstyle="round,pad=0.05", 
                            facecolor=color, edgecolor='white', linewidth=1, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # API Layer
    # REST API
    rest_api = Rectangle((1, 5), 6, 0.8, facecolor='#e74c3c', edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(rest_api)
    ax.text(4, 5.4, 'FastAPI REST Server', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    # MCP Server
    mcp_server = Rectangle((8, 5), 3, 0.8, facecolor='#9b59b6', edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(mcp_server)
    ax.text(9.5, 5.4, 'MCP Server', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    # CTL Core Library
    core_lib = Rectangle((2, 3.5), 8, 0.8, facecolor='#2E86AB', edgecolor='white', linewidth=2, alpha=0.9)
    ax.add_patch(core_lib)
    ax.text(6, 3.9, 'CTL Core Library (Connectors + Transformations)', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # Data Connectors
    connectors = [
        (1.5, 2.5, 'Local\nFiles', '#34495e'),
        (3.5, 2.5, 'Azure\nSQL', '#3498db'),
        (5.5, 2.5, 'MySQL', '#e67e22'),
        (7.5, 2.5, 'Databricks', '#e74c3c'),
        (9.5, 2.5, 'Future\nConnectors', '#95a5a6')
    ]
    
    for x, y, label, color in connectors:
        box = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6, 
                            boxstyle="round,pad=0.05", 
                            facecolor=color, edgecolor='white', linewidth=1, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Transformations
    transforms = [
        (2.5, 1.5, 'Normalize', '#27ae60'),
        (4.5, 1.5, 'Moving\nAverage', '#f39c12'),
        (6.5, 1.5, 'Seasonal\nAdjustment', '#8e44ad'),
        (8.5, 1.5, 'Custom\nTransforms', '#16a085')
    ]
    
    for x, y, label, color in transforms:
        box = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6, 
                            boxstyle="round,pad=0.05", 
                            facecolor=color, edgecolor='white', linewidth=1, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Data Sources (Bottom)
    ax.text(6, 0.5, 'Data Sources: CSV, Parquet, Databases, APIs', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#2c3e50')
    
    # Draw arrows
    # From clients to APIs
    for x, _, _, _ in clients[:4]:  # REST API clients
        ax.annotate('', xy=(x, 5.8), xytext=(x, 6.1),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#34495e', alpha=0.7))
    
    # From AI Assistant to MCP
    ax.annotate('', xy=(9.5, 5.8), xytext=(9.5, 6.1),
               arrowprops=dict(arrowstyle='->', lw=1.5, color='#34495e', alpha=0.7))
    
    # From APIs to Core
    ax.annotate('', xy=(4, 4.3), xytext=(4, 5),
               arrowprops=dict(arrowstyle='->', lw=2, color='#34495e'))
    ax.annotate('', xy=(9.5, 4.3), xytext=(9.5, 5),
               arrowprops=dict(arrowstyle='->', lw=2, color='#34495e'))
    
    # From Core to Connectors/Transforms
    for x, _, _, _ in connectors:
        ax.annotate('', xy=(x, 2.8), xytext=(x, 3.5),
                   arrowprops=dict(arrowstyle='->', lw=1, color='#34495e', alpha=0.5))
    
    for x, _, _, _ in transforms:
        ax.annotate('', xy=(x, 1.8), xytext=(x, 3.5),
                   arrowprops=dict(arrowstyle='->', lw=1, color='#34495e', alpha=0.5))
    
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('assets/images/architecture_diagram.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Generated Architecture Diagram")


def main():
    """Generate all visual assets"""
    print("🎨 Generating CTL visual assets...")
    
    # Set matplotlib style
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    
    # Generate symbols
    create_symbol_1_data_flow()
    create_symbol_2_transformation_pipeline()
    create_symbol_3_data_ecosystem()
    
    # Generate architecture diagram
    create_architecture_diagram()
    
    print("\n🎉 All visual assets generated successfully!")
    print("📁 Assets saved in: assets/images/")
    print("   - symbol_1_data_flow.png")
    print("   - symbol_2_pipeline.png") 
    print("   - symbol_3_ecosystem.png")
    print("   - architecture_diagram.png")


if __name__ == "__main__":
    main()