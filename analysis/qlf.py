import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def analyze_qlf(df, chart_type, colors=None):
    groups = df['Group'].unique().tolist()

    if chart_type == 'bar':
        image_path = os.path.join(OUTPUT_FOLDER, 'qlf_bar.svg')
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

        plt.title("QLF – RGB Bar Chart")
        plt.tight_layout()
        plt.savefig(image_path, format='svg')
        plt.close()

        return {"tytul": "QLF – Bar", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'heatmap':
        image_path = os.path.join(OUTPUT_FOLDER, 'qlf_heatmap.svg')
        pivot = df.pivot(index='Point', columns='Group', values='R/G Value (Mean)')
        plt.figure(figsize=(12, 8))

        sns.heatmap(pivot, annot=True, cmap="coolwarm", cbar_kws={'label': 'R/G Value'})

        plt.title("QLF – RGB Heatmap")
        plt.tight_layout()
        plt.savefig(image_path, format='svg')
        plt.close()

        return {"tytul": "QLF – Heatmap", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for QLF")
