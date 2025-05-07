import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
# INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
INKSCAPE_PATH = "inkscape"

def analyze_beta_diversity(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'axis1': 'Axis1',
        'axis2': 'Axis2',
        'group': 'Group'
    })

    df['Group'] = df['Group'].astype(str)

    if chart_type == 'scatter':
        base_name = 'beta_scatter'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))

        palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

        sns.scatterplot(
            data=df,
            x='Axis1',
            y='Axis2',
            hue='Group',
            palette=palette
        )

        plt.title(custom_title.strip() if custom_title else "β-diversity (PCoA)")
        plt.xlabel(x_label.strip() if x_label else "Axis1")
        plt.ylabel(y_label.strip() if y_label else "Axis2")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
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
            "tytul": custom_title.strip() if custom_title else "Beta Diversity – Scatter Plot",
            "img_svg": f"/output/{os.path.basename(svg_path)}",
            "img_emf": f"/output/{os.path.basename(emf_path)}"
        }

    else:
        raise ValueError("Unsupported chart_type for BetaDiversity")
