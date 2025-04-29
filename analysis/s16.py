import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def analyze_16s(df, chart_type, colors=None):
    df = df.set_index('Taxon Name').astype(float)

    if chart_type == 'bar':
        image_path = os.path.join(OUTPUT_FOLDER, '16s_stacked_bar.svg')
        plt.figure(figsize=(14, 8))

        color_list = [colors.get(taxon, None) for taxon in df.index] if colors else None

        ax = df.T.plot(kind='bar', stacked=True, figsize=(14, 8), color=color_list)

        plt.title("16S rRNA – Stacked Bar Chart")
        plt.xlabel("Sample")
        plt.ylabel("Relative Abundance")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "16S – Stacked Bar", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'pie':
        image_path = os.path.join(OUTPUT_FOLDER, '16s_pie.svg')
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

        plt.title("16S rRNA – Top 10 Taxa (Pie Chart)")
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "16S – Pie", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'heatmap':
        image_path = os.path.join(OUTPUT_FOLDER, '16s_heatmap.svg')
        plt.figure(figsize=(14, 8))

        sns.heatmap(df, cmap="YlGnBu", annot=False)

        plt.title("16S rRNA – Heatmap")
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "16S – Heatmap", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for 16S")
