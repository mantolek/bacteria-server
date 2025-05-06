import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # dopasuj do środowiska

def analyze_qlf(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    groups = df['Group'].unique().tolist()

    if chart_type == 'bar':
        base_name = 'qlf_bar'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(12, 6))

        palette = [colors[group] for group in groups] if colors else None

        ax = sns.barplot(
            data=df,
            x='Point',
            y='R/G Value (Mean)',
            hue='Group',
            ci=None,
            palette=palette
        )

        for idx, row in df.iterrows():
            ax.errorbar(
                x=idx,
                y=row['R/G Value (Mean)'],
                yerr=row['R/G Value (SD)'],
                fmt='none',
                c='black',
                capsize=5
            )

        plt.title(custom_title.strip() if custom_title else "QLF – RGB Bar Chart")
        plt.xlabel(x_label.strip() if x_label else "Point")
        plt.ylabel(y_label.strip() if y_label else "R/G Value (Mean)")
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'heatmap':
        base_name = 'qlf_heatmap'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        pivot = df.pivot(index='Point', columns='Group', values='R/G Value (Mean)')
        plt.figure(figsize=(12, 8))

        sns.heatmap(pivot, annot=True, cmap="coolwarm", cbar_kws={'label': 'R/G Value'})

        plt.title(custom_title.strip() if custom_title else "QLF – RGB Heatmap")
        if x_label: plt.xlabel(x_label.strip())
        if y_label: plt.ylabel(y_label.strip())

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for QLF")

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
