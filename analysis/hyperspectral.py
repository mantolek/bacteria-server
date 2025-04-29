import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt

OUTPUT_FOLDER = 'output'

def analyze_hyperspectral(df, chart_type, colors=None):
    if chart_type == 'lines':
        image_path = os.path.join(OUTPUT_FOLDER, 'hyperspectral_lines.svg')
        plt.figure(figsize=(12, 8))

        df['Group'] = df['Group'].astype(str).str.strip()
        groups = df['Group'].unique()

        for group in groups:
            print(f'Plotting group: {group}, using color: {colors.get(group)}')
            subset = df[df['Group'] == group]
            plt.plot(
                subset['Wavelength'],
                subset['Intensity'],
                label=group,
                color=colors.get(group, None),
            )

        plt.title("Hyperspectral – Spectral Lines")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        plt.legend()
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Hyperspectral – Lines", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for Hyperspectral")
