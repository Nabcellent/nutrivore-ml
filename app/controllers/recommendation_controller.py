from app.image_finder.image_finder import get_images_links
from app.models.kenya import KenyaModel


class RecommendationController:
    def __init__(self, nutritional_values):
        self.nutritional_values = nutritional_values
        self.model = KenyaModel(nutritional_values)

    def recommend(self, ingredients, no_of_recommendations):
        recommendation_dataframe = self.model.recommend(self.nutritional_values, ingredients, {
            'n_neighbors': no_of_recommendations,
            'return_distance': False
        })

        recommendations = self.model.output_recommended_recipes(recommendation_dataframe)

        if recommendations:
            for recipe in recommendations:
                recipe['image_link'] = get_images_links(recipe['name'])

        return recommendations
