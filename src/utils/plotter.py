import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

class Plotter:
    """A class that contains methods for plotting data in various formats.
    """
    def __init__(self, data_dict: dict, title: str, x_label: str, y_label: str, folder_path: str):
        """Initializes the Plotter class.

        Args:
            data_dict (dict): A dictionary containing the data to plot.
            title (str): The title of the plot.
            x_label (str): The label for the x-axis.
            y_label (str): The label for the y-axis.
            folder_path (str): The path to the folder where the plot png files will be saved.
        """
        self.data_dict = data_dict
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.folder_path = folder_path
        self.keys = list(self.data_dict.keys())
        self.values = list(self.data_dict.values())
        
    def line_graph(self) -> None:
        """Plots a line graph and saves it as a png file.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(self.keys, self.values, marker='o', linestyle='-', color='b')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(True)
        plt.savefig(f"{self.folder_path}/line_graph.png")
        plt.close()
    
    def bar_plot(self) -> None:
        """Plots a bar graph and saves it as a png file.
        """
        plt.figure(figsize=(10, 5))
        plt.bar(self.keys, self.values, color='skyblue')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.savefig(f"{self.folder_path}/bar_plot.png")
        plt.close()

    def pie_chart(self) -> None:
        """Plots a pie chart and saves it as a png file.
        """
        sizes = self.values
        labels = self.keys
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # ensure that pie is drawn as circle
        plt.title(self.title)
        plt.savefig(f"{self.folder_path}/pie_chart.png")
        plt.close()