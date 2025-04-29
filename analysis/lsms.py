import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

OUTPUT_FOLDER = 'output'

def analyze_lsms(df, chart_type, colors=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns=lambda x: x.strip())

    if 'compound' in df.columns:
        df = df.set_index('compound')

    df = df.select_dtypes(include='number')

    if df.empty:
        raise ValueError("No numeric data to plot.")

    if chart_type == 'bar':
        image_path = os.path.join(OUTPUT_FOLDER, 'lsms_bar.svg')
        plt.figure(figsize=(14, 8))

        color_list = [colors.get(compound, None) for compound in df.index] if colors else None

        df.T.plot(kind='bar', stacked=True, figsize=(14, 8), color=color_list)

        plt.title("LS/MS – Signal Intensity")
        plt.xlabel("Sample")
        plt.ylabel("Signal Intensity")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.tight_layout()
        plt.savefig(image_path, format='svg')
        plt.close()

        return {"tytul": "LS/MS – Signal Intensity", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'pca':
        image_path = os.path.join(OUTPUT_FOLDER, 'lsms_pca.svg')

        pca = PCA(n_components=2)
        components = pca.fit_transform(df.T)

        plt.figure(figsize=(12, 8))

        if colors:
            color_list = []
            for sample in df.columns:
                color_list.append(colors.get(sample, '#000000'))
        else:
            color_list = None

        plt.scatter(
            components[:, 0],
            components[:, 1],
            c=color_list
        )

        plt.title("LS/MS – PCA")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.tight_layout()
        plt.savefig(image_path, format='svg')
        plt.close()

        return {"tytul": "LS/MS – PCA", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for LSMS")
