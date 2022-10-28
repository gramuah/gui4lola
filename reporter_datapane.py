import pandas as pd
import os
import datapane as dp


def clean_dataframe(data):
    dict_change = {"Pasar_la_fregona": "Pasar la fregona",
                   "PasarLafregona": "Pasar la fregona",
                   "Cepillarse_los_dientes": "Cepillarse los dientes",
                   "CepillarLosDientes": "Cepillar los dientes",
                   "Escribir_en_la_pizarra": "Escribir en la pizarra",
                   "EscribirEnLaPizarra": "Escribir en la pizarra",
                   "Secar_el_pelo": "Secar el pelo",
                   "SecarElPelo": "Secar el pelo"}
    # Cambiar nombre index
    data = data.replace(dict_change)

    dict_colum = {'Acción_Requerida': 'Acción Requerida',
                  'Acción_Detectada': 'Acción Detectada',
                  'Hora_Comienzo': 'Hora Comienzo',
                  'Hora_Finalización': 'Hora Finalización'}

    data = data.rename(columns=dict_colum)
    return data


def generate_report(filename):
    data = pd.read_csv(filename)
    data = clean_dataframe(data)
    user_name = filename.split('_')[-1].split('.')[0]
    report_elements = list()

    for row in data.iterrows():
        report_elements.append(dp.Table(pd.DataFrame(row[1]).drop(index=['Path'], axis=0)))

        input_image_path = row[1]['Path']
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
    ).save(path="Reports/Informe-{}.html".format(user_name))
