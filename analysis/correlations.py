import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
# INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
INKSCAPE_PATH = "inkscape"

def analyze_correlations(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'parameter_1': 'Parameter_1',
        'parameter_2': 'Parameter_2'
    })

    if chart_type == 'scatter_reg':
        base_name = 'correlation'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(12, 8))

        scatter_color = colors.get('scatter', 'b') if colors else 'b'
        line_color = colors.get('line', 'r') if colors else 'r'

        sns.regplot(
            data=df,
            x='Parameter_1',
            y='Parameter_2',
            scatter_kws={'color': scatter_color},
            line_kws={'color': line_color}
        )

        plt.title(custom_title.strip() if custom_title else "Correlation Between Parameters")
        plt.xlabel(x_label.strip() if x_label else "Parameter 1")
        plt.ylabel(y_label.strip() if y_label else "Parameter 2")
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
            "tytul": custom_title.strip() if custom_title else "Correlation Between Parameters",
            "img_svg": f"/output/{os.path.basename(svg_path)}",
            "img_emf": f"/output/{os.path.basename(emf_path)}"
        }

    else:
        raise ValueError("Unsupported chart_type for Correlations")
