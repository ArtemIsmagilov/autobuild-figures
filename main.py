import json
from pathlib import Path
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Figure(ABC):

    @abstractmethod
    def __init__(self, transparency=None, color=None, line_width=None, alpha=None, linestyle=None):
        self.fill = transparency
        self.color = color
        self.linewidth = line_width
        self.alpha = alpha
        self.linestyle = linestyle

    @abstractmethod
    def draw(self, ax):
        pass

    def say_name(self):
        return f'{self.__class__.__name__}(id={id(self)})'


class Circle(Figure):

    def __init__(self, x_center, y_center, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xy = x_center, y_center
        self.radius = radius

    def draw(self, ax):
        circle = plt.Circle(**self.__dict__, label=self.say_name())
        ax.add_patch(circle)


class Rectangle(Figure):

    def __init__(self, x_upper_left, y_upper_left, x_lower_right, y_lower_right, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.xy = x_upper_left, y_upper_left
        self.width = x_lower_right
        self.height = y_lower_right

    def draw(self, ax):
        rectangle = plt.Rectangle(**self.__dict__, label=self.say_name())
        ax.add_patch(rectangle)


class Triangle(Figure):

    def __init__(self, shape, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = list(map(lambda x: tuple(x['point'].values()), shape))

    def draw(self, ax):
        circle = plt.Polygon(self.points, label=self.say_name())
        ax.add_patch(circle)


class Square(Rectangle):

    def __init__(self, x_upper_left, y_upper_left, side_length, *args, **kwargs):
        super().__init__(x_upper_left, y_upper_left, side_length, side_length, *args, **kwargs)

    def draw(self, ax):
        super().draw(ax)


class FigureFactory:

    @classmethod
    def create_product(cls, creator_name, *args, **kwargs):
        return eval(f'{creator_name}(*args, **kwargs)')


class PictureFromJson:

    @classmethod
    def run(cls, path_config):

        with open(path_config, 'r', encoding='utf-8') as config_f:
            config_json = json.loads(config_f.read())

        data_root_folder, output_folder = config_json['data_root_folder'], config_json['output_folder']

        for from_path in Path(data_root_folder).glob('*.json'):

            with open(from_path, 'r', encoding='utf-8') as json_f:
                json_data = json.loads(json_f.read())

            w, h = json_data['image_size'].values()
            fig, ax = plt.subplots(figsize=(w / 100, h / 100), layout='constrained')

            ax.set_xlabel('width')
            ax.set_ylabel('height')
            ax.set_title(from_path.name)

            for data in json_data['figures']:
                figure_name, params = data.popitem()
                figure_obj = FigureFactory.create_product(figure_name, **params)
                figure_obj.draw(ax)

            fig.legend(loc='outside upper right')
            ax.autoscale()
            to_path = Path(output_folder) / from_path.with_suffix('.png').name
            plt.savefig(to_path, format='png')
            print('Saved figure to', to_path, 'from', from_path)


if __name__ == '__main__':
    PictureFromJson.run('config.json')
