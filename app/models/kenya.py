import numpy as np
import polars as pl
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler


class KenyaModel:
    dataset = pl.read_csv('data/ke-recipes.csv').fill_nan(None)

    def __init__(self, values):
        self._input = values

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

    def apply_pipeline(self, pipeline, _input, extracted_data):
        _input = np.array(_input).reshape(1, -1)

        return extracted_data[pipeline.transform(_input)[0]]

    def recommend(self, _input, ingredients, params):
        data = self.dataset

        if len(ingredients) > 0:
            data = data.filter([pl.col('ingredients').str.contains(i) for i in ingredients])

        if data.shape[0] < params['n_neighbors']:
            return None

        prep_data, scaler = self.scaling(data)
        neigh = self.nn_predictor(prep_data)
        pipeline = self.build_pipeline(neigh, scaler, params)

        return self.apply_pipeline(pipeline, _input, data)

    def output_recommended_recipes(self, dataframe):
        if dataframe is not None:
            output = dataframe.clone()
            output = output.rows(named=True)

            for recipe in output:
                recipe['ingredients'] = recipe['ingredients'].split(';')
                recipe['instructions'] = recipe['instructions'].split(';')

            return output
        return None
