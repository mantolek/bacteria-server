import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # dopasuj do środowiska

def analyze_lsms(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns=lambda x: x.strip())

    if 'compound' in df.columns:
        df = df.set_index('compound')

    df = df.select_dtypes(include='number')

    if df.empty:
        raise ValueError("No numeric data to plot.")

    if chart_type == 'bar':
        base_name = 'lsms_bar'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))

        color_list = [colors.get(compound, None) for compound in df.index] if colors else None
        df.T.plot(kind='bar', stacked=True, ax=plt.gca(), color=color_list)

        plt.title(custom_title.strip() if custom_title else "LS/MS – Signal Intensity")
        plt.xlabel(x_label.strip() if x_label else "Sample")
        plt.ylabel(y_label.strip() if y_label else "Signal Intensity")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'pca':
        base_name = 'lsms_pca'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        pca = PCA(n_components=2)
        components = pca.fit_transform(df.T)

        plt.figure(figsize=(12, 8))

        if colors:
            color_list = [colors.get(sample, '#000000') for sample in df.columns]
        else:
            color_list = None

        plt.scatter(components[:, 0], components[:, 1], c=color_list)

        plt.title(custom_title.strip() if custom_title else "LS/MS – PCA")
        plt.xlabel(x_label.strip() if x_label else "Principal Component 1")
        plt.ylabel(y_label.strip() if y_label else "Principal Component 2")
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for LSMS")

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
