import pandas as pd
from sklearn.preprocessing import LabelEncoder
from core.config import DATASET


class LabelDecoder():
    def __init__(self):
        df = pd.read_csv(DATASET)
        self.df = self._clean_dataframe(df)

        label_encoder = LabelEncoder()

        label_encoder.fit_transform(self.df['Точка отказа'])
        self.request_type_labels = label_encoder.classes_
        
        label_encoder.fit_transform(self.df['Тип оборудования'])
        self.hardware_type_labels = label_encoder.classes_


    def _clean_dataframe(self, df):
        df = df.drop(df[df['Точка отказа'] == 'Консультация'].index)
        df['Точка отказа'] = df['Точка отказа'].replace({'Диск ': 'Диск'})
        return df
