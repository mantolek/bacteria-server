import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # dopasuj do środowiska

def analyze_hyperspectral(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    if chart_type == 'lines':
        base_name = 'hyperspectral_lines'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(12, 8))

        df['Group'] = df['Group'].astype(str).str.strip()
        groups = df['Group'].unique()

        for group in groups:
            subset = df[df['Group'] == group]
            plt.plot(
                subset['Wavelength'],
                subset['Intensity'],
                label=group,
                color=colors.get(group, None),
            )

        plt.title(custom_title.strip() if custom_title else "Hyperspectral – Spectral Lines")
        plt.xlabel(x_label.strip() if x_label else "Wavelength (nm)")
        plt.ylabel(y_label.strip() if y_label else "Intensity")
        plt.legend()
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
            "tytul": custom_title.strip() if custom_title else "Hyperspectral – Lines",
            "img_svg": f"/output/{os.path.basename(svg_path)}",
            "img_emf": f"/output/{os.path.basename(emf_path)}"
        }

    else:
        raise ValueError("Unsupported chart_type for Hyperspectral")
