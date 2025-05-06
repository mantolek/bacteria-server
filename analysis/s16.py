import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # dopasuj do środowiska

def analyze_16s(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.set_index('Taxon Name').astype(float)

    if chart_type == 'bar':
        base_name = '16s_stacked_bar'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))
        color_list = [colors.get(taxon, None) for taxon in df.index] if colors else None

        ax = df.T.plot(kind='bar', stacked=True, figsize=(14, 8), color=color_list)

        plt.title(custom_title.strip() if custom_title else "16S rRNA – Stacked Bar Chart")
        plt.xlabel(x_label.strip() if x_label else "Sample")
        plt.ylabel(y_label.strip() if y_label else "Relative Abundance")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'pie':
        base_name = '16s_pie'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        summed = df.sum(axis=1)
        top = summed.nlargest(10)

        plt.figure(figsize=(10, 10))
        color_list = [colors.get(taxon, None) for taxon in top.index] if colors else None

        plt.pie(
            top,
            labels=top.index,
            autopct='%1.1f%%',
            colors=color_list,
            startangle=90
        )

        plt.title(custom_title.strip() if custom_title else "16S rRNA – Top 10 Taxa (Pie Chart)")
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'heatmap':
        base_name = '16s_heatmap'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))
        sns.heatmap(df, cmap="YlGnBu", annot=False)

        plt.title(custom_title.strip() if custom_title else "16S rRNA – Heatmap")
        if x_label: plt.xlabel(x_label.strip())
        if y_label: plt.ylabel(y_label.strip())

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for 16S")

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
