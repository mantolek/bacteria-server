import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

OUTPUT_FOLDER = 'output'

def analyze_fluorescence_over_time(df, chart_type, colors=None):
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    if 'Wavelength (nm)' not in df.columns:
        raise ValueError("Missing 'Wavelength (nm)' column in data.")

    df.set_index('Wavelength (nm)', inplace=True)

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
        image_path = os.path.join(OUTPUT_FOLDER, 'fluorescence_line.svg')
        plt.figure(figsize=(14, 8))

        color_list = list(colors.values()) if colors else None

        df.T.plot(color=color_list)

        plt.title("Fluorescence Change Over Time")
        plt.xlabel("Time")
        plt.ylabel("Intensity")
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Fluorescence Change Over Time", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'surface':
        from mpl_toolkits.mplot3d import Axes3D
        image_path = os.path.join(OUTPUT_FOLDER, 'fluorescence_surface.svg')

        X, Y = np.meshgrid(df.columns, df.index)
        Z = df.values

        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(X, Y, Z, cmap='viridis')

        ax.set_xlabel("Time (relative)")
        ax.set_ylabel("Wavelength (nm)")
        ax.set_zlabel("Intensity")
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Fluorescence Surface", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for FluorescenceOverTime")
