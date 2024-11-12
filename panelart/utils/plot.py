import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore


def plot_results(plot_df, title, figsize=(10, 6)):
    plt.figure(figsize=figsize)

    sns.barplot(plot_df, x='party', y='count', hue='output')

    plt.legend()
    plt.title(title)
    plt.tight_layout()
    plt.show()
