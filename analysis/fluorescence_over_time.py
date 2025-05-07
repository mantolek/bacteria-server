import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import subprocess

OUTPUT_FOLDER = 'output'
# INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
INKSCAPE_PATH = "inkscape"

def analyze_fluorescence_over_time(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    if 'Wavelength (nm)' not in df.columns:
        raise ValueError("Missing 'Wavelength (nm)' column in data.")

    df.set_index('Wavelength (nm)', inplace=True)

    # Przekształcenie kolumn czasowych
    new_columns = []
    for col in df.columns:
        if isinstance(col, str) and col.startswith('T'):
            try:
                new_columns.append(int(col[1:]))
            except ValueError:
                new_columns.append(col)
        else:
            new_columns.append(col)
    df.columns = new_columns

    df.index = pd.to_numeric(df.index, errors='coerce')
    df = df.dropna(axis=0, how='any')

    if chart_type == 'line':
        base_name = 'fluorescence_line'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))
        color_list = list(colors.values()) if colors else None
        df.T.plot(color=color_list, ax=plt.gca())

        plt.title(custom_title.strip() if custom_title else "Fluorescence Change Over Time")
        plt.xlabel(x_label.strip() if x_label else "Time")
        plt.ylabel(y_label.strip() if y_label else "Intensity")

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'surface':
        from mpl_toolkits.mplot3d import Axes3D
        base_name = 'fluorescence_surface'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        X, Y = np.meshgrid(df.columns, df.index)
        Z = df.values

        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(X, Y, Z, cmap='viridis')

        ax.set_title(custom_title.strip() if custom_title else "Fluorescence Surface")
        ax.set_xlabel(x_label.strip() if x_label else "Time (relative)")
        ax.set_ylabel(y_label.strip() if y_label else "Wavelength (nm)")
        ax.set_zlabel("Intensity")

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for FluorescenceOverTime")

    # EMF konwersja
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
        "tytul": custom_title.strip() if custom_title else base_name.replace("_", " ").title(),
        "img_svg": f"/output/{os.path.basename(svg_path)}",
        "img_emf": f"/output/{os.path.basename(emf_path)}"
    }
