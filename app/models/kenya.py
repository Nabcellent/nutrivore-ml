import numpy as np
import re
import polars as pl
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


class KenyaModel:
    def __init__(self, values):
        self._input = values
        self.dataset = pl.read_csv('data/ke-recipes.csv')
        self.dataset = self.dataset.fill_nan(None)

    def scaling(self, dataframe):
        scaler = StandardScaler()
        prep_data = scaler.fit_transform(dataframe[:, 8:16].to_numpy())

        return prep_data, scaler

    def nn_predictor(self, prep_data):
        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data)

        return neigh

    def build_pipeline(self, neigh, scaler, params):
        transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
        pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])

        return pipeline

    def extract_data(self, dataframe, ingredients):
        extracted_data = dataframe.clone()
        extracted_data = self.extract_ingredient_filtered_data(extracted_data, ingredients)

        return extracted_data

    def extract_ingredient_filtered_data(self, dataframe, ingredients):
        extracted_data = dataframe.clone()

        return extracted_data.filter([pl.col('ingredients').str.contains(i) for i in ingredients])

    def apply_pipeline(self, pipeline, _input, extracted_data):
        _input = np.array(_input).reshape(1, -1)

        return extracted_data[pipeline.transform(_input)[0]]

    def recommend(self, _input, ingredients, params):
        extracted_data = self.extract_data(self.dataset, ingredients)

        if extracted_data.shape[0] >= params['n_neighbors']:
            prep_data, scaler = self.scaling(extracted_data)
            neigh = self.nn_predictor(prep_data)
            pipeline = self.build_pipeline(neigh, scaler, params)

            return self.apply_pipeline(pipeline, _input, extracted_data)
        else:
            return None

    def extract_quoted_strings(self, s):
        # Find all the strings inside double quotes
        strings = re.findall(r'"([^"]*)"', s)
        # Join the strings with 'and'

        return strings

    def output_recommended_recipes(self, dataframe):
        if dataframe is not None:
            output = dataframe.clone()
            output = output.rows(named=True)

            for recipe in output:
                recipe['ingredients'] = recipe['ingredients'].split(';')
                recipe['instructions'] = recipe['instructions'].split(';')
        else:
            output = None

        return output
