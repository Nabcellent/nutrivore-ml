import numpy as np
import polars as pl
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from app.utils.enums import Meal


class KenyaModel:
    dataset = pl.read_csv('data/ke-recipes.csv').fill_nan(None)

    def __init__(self, values: list):
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

    def apply_pipeline(self, pipeline, extracted_data):
        _input = np.array(self._input).reshape(1, -1)

        return extracted_data[pipeline.transform(_input)[0]]

    def apply_filters(self, dataset, ingredients, meal):
        if len(ingredients) > 0:
            dataset = dataset.filter([pl.col('ingredients').str.contains(i) for i in ingredients])

        if meal and 'snack' in meal.value:
            dataset = dataset.filter([pl.col('category').str.contains('snack|desserts|porridges')])

        return dataset

    def recommend(self, ingredients, params, meal: Meal = None):
        data = self.apply_filters(self.dataset, ingredients, meal)

        if data.shape[0] < params['n_neighbors']:
            return None

        prep_data, scaler = self.scaling(data)
        neigh = self.nn_predictor(prep_data)
        pipeline = self.build_pipeline(neigh, scaler, params)

        return self.apply_pipeline(pipeline, data)

    def output_recommended_recipes(self, dataframe):
        if dataframe is not None:
            output = dataframe.clone()
            output = output.rows(named=True)

            for recipe in output:
                recipe['ingredients'] = recipe['ingredients'].split(';')
                recipe['instructions'] = recipe['instructions'].split(';')

            return output
        return []
