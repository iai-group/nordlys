"""
plot_diff
---------

Plots a series of scores which represent differences.

@author: Shuo Zhang
@author: Krisztian Balog
"""
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pylab as plt
from nordlys.core.utils.file_utils import FileUtils


class QueryDiff(object):
    SCORES = [25, 20, 10, 5, 0, -1, -5, -10]

    def __init__(self):
        self.width = 1 / 1
        self.color = "blue"

    def make_plot(self):
        """Make a bar plot using SCORES"""
        N = len(self.SCORES)
        x = range(N)
        plt.bar(x, self.SCORES, self.width, color=self.color)
        plt.show()

    def create_pdf(self, diff_file, pdf_file, title="", xlabel="", ylabel="", aspect_ratio="equal", separator="\t"):
        """Create bar plot for differences in pdf.
        
        This function is used to load difference .csv file, 
        create bar plot and store as a pfd file.

        :pdf: created and saved pdf file       
        """
        data = FileUtils.read_file_as_list(diff_file)

        scores = []
        for item in data:
            if "diff" in item:  # ignore the first line(title)
                continue
            scores.append(float(item.split(separator)[3]))

        scores = sorted(scores, reverse=True)

        with PdfPages(pdf_file) as pdf:
            n = len(scores)
            x = range(n)
            plt.figure(figsize=(4, 4))
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.bar(x, scores, self.width, color=self.color)
            plt.tight_layout()  # warning,still working
            pdf.savefig()
            plt.close()
