"""
"""
import pandas as pd
import seaborn as sns


class ExploratoryVisualization(object):

    def reshape_df_to_plot(self, groups):
        plotDF = pd.DataFrame()
        for name in groups:
            df = groups[name]
            df['group'] = name
            plotDF = pd.concat([plotDF, df])
        return plotDF

    def box_plot(self, groups):
        key = list(groups.keys())[0]
        cols = [str(col) for i, col in enumerate(groups[key].columns)]
        plotDF = self.reshape_df_to_plot(groups)

        sns.set_context(font_scale=0.6)
        sns.set(rc={'figure.figsize': (2*11.7, 2 * 8.27)})
        for col in cols:
            plot = sns.boxenplot(x=col, y="group", data=plotDF)
            plot.set_title(col)
            plot.get_figure().savefig('boxplot_' + col + '.jpg')

    def violin_plot(self, parameter_list):
        pass

    def scatter_matrix(self, parameter_list):
        pass

    def qq_plot(self, parameter_list):
        pass
