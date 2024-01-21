import unittest
import json
from pathlib import Path

from main import (
    PictureFromJson,
)


class TestCreateImage(unittest.TestCase):
    def _init_config_and_run(self, data_root_folder, output_folder, output_filename):
        with open('config.json', 'r', encoding='utf-8') as config_r:
            config_json = json.loads(config_r.read())

        config_json.update(data_root_folder=data_root_folder, output_folder=output_folder)

        with open('config.json', 'w', encoding='utf-8') as config_w:
            config_w.write(json.dumps(config_json))

        PictureFromJson.run('config.json')

        self.assertEqual((Path(output_folder) / output_filename).exists(), True)

    def test_exists_image_task1(
            self, data_root_folder='task1/DATA', output_folder='task1/Images', output_filename='task1.svg'
    ):
        self._init_config_and_run(data_root_folder, output_folder, output_filename)

    def test_exists_image_task2(
            self, data_root_folder='task2/DATA', output_folder='task2/Images', output_filename='task2.svg'
    ):
        self._init_config_and_run(data_root_folder, output_folder, output_filename)

    def test_exists_image_task3(
            self, data_root_folder='task3/DATA', output_folder='task3/Images', output_filename='task3.svg'
    ):
        self._init_config_and_run(data_root_folder, output_folder, output_filename)

    def test_exists_image_task4(
            self, data_root_folder='task4/DATA', output_folder='task4/Images', output_filename='task4.svg'
    ):
        self._init_config_and_run(data_root_folder, output_folder, output_filename)

    def test_exists_image_task5(
            self, data_root_folder='task5/DATA', output_folder='task5/Images', output_filename='task5.svg'
    ):
        self._init_config_and_run(data_root_folder, output_folder, output_filename)

    def test_exists_image_task6(
            self, data_root_folder='task6/DATA', output_folder='task6/Images', output_filename='task6.svg'
    ):
        self._init_config_and_run(data_root_folder, output_folder, output_filename)


if __name__ == '__main__':
    # coverage run -m unittest
    unittest.main()
