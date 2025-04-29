import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def analyze_alpha_diversity(df, chart_type, colors=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'group': 'Group',
        'alphadiversity': 'AlphaDiversity'
    })

    df['Group'] = df['Group'].astype(str)

    if chart_type == 'boxplot':
        image_path = os.path.join(OUTPUT_FOLDER, 'alpha_diversity_boxplot.svg')
        plt.figure(figsize=(14, 8))

        palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

        sns.boxplot(
            data=df,
            x='Group',
            y='AlphaDiversity',
            palette=palette
        )

        plt.title("Alpha Diversity – Boxplot")
        plt.xlabel("Group")
        plt.ylabel("Alpha Diversity")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Alpha Diversity – Boxplot", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for AlphaDiversity")
