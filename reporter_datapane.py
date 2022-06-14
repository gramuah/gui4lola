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
        input_image_path = row[1]['Path']
        report_elements.append(dp.Table(pd.DataFrame(row[1]).drop(index=['Path'], axis=0)))
        report_elements.append(dp.Media(file=input_image_path))

    dp.Report(
        dp.Group(
            dp.Text("# Report de {}".format(user_name)),
            dp.Media(file='~/gui4lola/data/Fondo/fondo_blanco.jpg'),
            dp.Media(file='~/gui4lola/data/Image/uah.jpg'),
            dp.Media(file='~/gui4lola/data/Image/logo_air4dp.png'),
            columns=4
        ),
        *[element for element in report_elements],
    ).save(path="Informe-{}.html".format(user_name))
