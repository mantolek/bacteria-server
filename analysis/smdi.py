import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # pełna ścieżka do Inkscape

def analyze_smdi(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'group': 'Group',
        'smdi_value': 'SMDI_Value'
    })
    df['Group'] = df['Group'].astype(str)

    palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None
    base_name = 'smdi_boxplot' if chart_type == 'boxplot' else 'smdi_bar'

    svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
    emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

    plt.figure(figsize=(14, 8))

    if chart_type == 'boxplot':
        sns.boxplot(data=df, x='Group', y='SMDI_Value', palette=palette)
    elif chart_type == 'bar':
        sns.barplot(data=df, x='Group', y='SMDI_Value', ci='sd', palette=palette)
    else:
        raise ValueError("Unsupported chart_type for SMDI")

    title = custom_title.strip() if custom_title else ("SMDI – Boxplot" if chart_type == 'boxplot' else "SMDI – Bar Chart")
    plt.title(title)
    plt.xlabel(x_label.strip() if x_label else "Group")
    plt.ylabel(y_label.strip() if y_label else "SMDI_Value")

    plt.tight_layout()
    plt.savefig(svg_path, format='svg', bbox_inches='tight')
    plt.close()

    try:
        subprocess.run([
            INKSCAPE_PATH,
            svg_path,
            "--export-type=emf",
            "--export-filename", emf_path
        ], check=True)
    except Exception as e:
        return {"error": f"Failed to convert SVG to EMF: {str(e)}"}

    return {
        "tytul": title,
        "img_svg": f"/output/{os.path.basename(svg_path)}",
        "img_emf": f"/output/{os.path.basename(emf_path)}"
    }
