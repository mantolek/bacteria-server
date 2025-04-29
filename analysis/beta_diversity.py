import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def analyze_beta_diversity(df, chart_type, colors=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'axis1': 'Axis1',
        'axis2': 'Axis2',
        'group': 'Group'
    })

    df['Group'] = df['Group'].astype(str)

    if chart_type == 'scatter':
        image_path = os.path.join(OUTPUT_FOLDER, 'beta_scatter.svg')
        plt.figure(figsize=(14, 8))

        palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

        sns.scatterplot(
            data=df,
            x='Axis1',
            y='Axis2',
            hue='Group',
            palette=palette
        )

        plt.title("β-diversity (PCoA)")
        plt.xlabel("Axis1")
        plt.ylabel("Axis2")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Beta Diversity – Scatter Plot", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for BetaDiversity")
