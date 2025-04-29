import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def analyze_correlations(df, chart_type, colors=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'parameter_1': 'Parameter_1',
        'parameter_2': 'Parameter_2'
    })

    if chart_type == 'scatter_reg':
        image_path = os.path.join(OUTPUT_FOLDER, 'correlation.svg')
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

        plt.title("Correlation Between Parameters")
        plt.xlabel("Parameter 1")
        plt.ylabel("Parameter 2")
        plt.tight_layout()
        plt.savefig(image_path, format='svg')
        plt.close()

        return {"tytul": "Correlation Between Parameters", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for Correlations")
