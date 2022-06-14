import pandas as pd
import os
import datapane as dp

# Variables
# input_csv_path = '~/Downloads/log_nadia.csv'
# input_images_prefix_path = '/data/Image'
#
# user_name = input_csv_path.split('_')[-1].split('.')[0]
#
# # Load csv
# data = pd.read_csv('~/Downloads/log_nadia.csv')


def generate_report(filename):
    data = pd.read_csv(filename)
    user_name = filename.split('_')[-1].split('.')[0]
    report_elements = list()

    for row in data.iterrows():
        input_images_path = row[1]['Path']
        report_elements.append(dp.Table(pd.DataFrame(row[1])))
        list_dir = os.listdir(input_images_path)
        if len(list_dir) % 2 == 0:
            columns = 2
        else:
            columns = 3
        list_images = list()
        for image_dir in list_dir:
            list_images.append(dp.Media(file=os.path.join(input_images_path, image_dir)))
        report_elements.append(dp.Group(*list_images, columns=columns))

    dp.Report(
        dp.Group(
            dp.Text("# Report de {}".format(user_name)),
            dp.Media(file='data/Fondo/fondo_blanco.jpg'),
            dp.Media(file='data/Image/uah.jpg'),
            dp.Media(file='data/Image/logo_air4dp.png'),
            columns=4
        ),
        *[element for element in report_elements],
    ).save(path="Hello_world.html")
