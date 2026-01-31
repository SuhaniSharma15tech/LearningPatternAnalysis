import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import pandas as pd

# Add the current directory to sys.path to resolve imports when running the file directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Robust import handling for both direct execution and module imports
try:
    from .analyze import get_complete_analysis
except (ImportError, ValueError):
    try:
        from analyze import get_complete_analysis
    except ImportError:
        # Fallback if running from the project root
        from utilities.analyze import get_complete_analysis

def generate_visuals(data, save_path="plots"):
    """
    Main function to generate matplotlib charts based on analysis results.
    'data' can be a single student dict or a batch DataFrame/CSV path.
    """
    # 1. Get the raw analysis results
    results = get_complete_analysis(data)
    
    # 2. Ensure save directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    if results.get("mode") == "single":
        _plot_single_student(results, save_path)
    else:
        _plot_batch_distribution(results, save_path)

def _plot_single_student(results, save_path):
    """Generates Radar and Positioning charts for one student."""
    
    # --- CHART 1: BEHAVIOURAL RADAR ---
    # We use themes if provided, otherwise we map the persona clusters
    themes = results.get('radar_data', {})
    
    # Fallback: if analyse.py doesn't return radar_data, we can't plot the radar
    if not themes:
        print("Note: Detailed radar data not found in results. Skipping Radar chart.")
    else:
        labels = list(themes.keys())
        values = [v * 100 for v in themes.values()]
        
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color='#6366f1', alpha=0.3)
        ax.plot(angles, values, color='#6366f1', linewidth=2)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([l.replace('_', '\n') for l in labels], size=9, fontweight='bold')
        ax.set_yticklabels([]) 
        
        plt.title(f"Student Persona: {results.get('persona_cluster', 'Unknown')}\nScore: {results.get('predicted_score', 0)}%", size=14, pad=20)
        plt.savefig(f"{save_path}/student_radar.png", bbox_inches='tight')
        plt.close()

    # --- CHART 2: ACADEMIC SCATTER ---
    plt.figure(figsize=(8, 6))
    centroids = {
        'Baseline': [0.498, 0.264], 
        'Growth': [0.833, 0.285],
        'Critical': [0.167, 0.248]
    }
    colors = {'Baseline': 'gold', 'Growth': 'forestgreen', 'Critical': 'crimson'}
    
    for name, pos in centroids.items():
        plt.scatter(pos[0]*100, pos[1]*100, c=colors[name], s=300, alpha=0.2, label=name)
    
    # Try to extract the score for plotting
    score = results.get('predicted_score', 0)
    # Note: For a proper scatter, we'd need 'Previous_Scores' from the record
    # This logic assumes the data is available in the results
    
    plt.xlabel("Previous Scores (%)")
    plt.ylabel("Exam Score (%)")
    plt.title("Academic Positioning Map")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(f"{save_path}/student_position.png", bbox_inches='tight')
    plt.close()
    
    print(f"Individual charts saved to {save_path}/")

def _plot_batch_distribution(results, save_path):
    """Generates Pie charts for class-wide data."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pie 1: Academic
    ac_map = results.get('academic_mapping', {})
    if ac_map:
        ac_labels = list(ac_map.keys())
        ac_counts = [len(v) for v in ac_map.values()]
        ax1.pie(ac_counts, labels=ac_labels, autopct='%1.1f%%', startangle=140, 
                colors=['#fbbf24', '#10b981', '#ef4444'], explode=[0.03]*len(ac_counts))
        ax1.set_title("Class Academic Distribution", fontweight='bold')

    # Pie 2: Persona
    pc_map = results.get('persona_mapping', {})
    if pc_map:
        pc_labels = list(pc_map.keys())
        pc_counts = [len(v) for v in pc_map.values()]
        ax2.pie(pc_counts, labels=pc_labels, autopct='%1.1f%%', startangle=140,
                colors=['#6366f1', '#ec4899', '#8b5cf6', '#06b6d4', '#94a3b8'])
        ax2.set_title("Class Persona Distribution", fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{save_path}/batch_distribution.png")
    plt.close()
    print(f"Batch distribution charts saved to {save_path}/")

if __name__ == "__main__":
    # Test with sample data
    test_student = {
        'Hours_Studied': 25, 'Attendance': 90, 'Parental_Involvement': 'High',
        'Access_to_Resources': 'High', 'Extracurricular_Activities': 'Yes',
        'Sleep_Hours': 8, 'Previous_Scores': 85, 'Motivation_Level': 'High',
        'Internet_Access': 'Yes', 'Tutoring_Sessions': 2, 'Family_Income': 'High',
        'Teacher_Quality': 'High', 'School_Type': 'Private', 'Peer_Influence': 'Positive',
        'Physical_Activity': 4, 'Learning_Disabilities': 'No',
        'Parental_Education_Level': 'Postgraduate', 'Distance_from_Home': 'Near', 'Gender': 'Female'
    }
    generate_visuals(test_student)