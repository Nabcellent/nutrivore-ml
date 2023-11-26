from app.image_finder.image_finder import get_images_links
from model import recommend, output_recommended_recipes


class RecommendCustom:
    def __init__(self, nutritional_values):
        self.nutritional_values = nutritional_values

    def generate_recommendations(self, ingredients, no_of_recommendations):
        recommendation_dataframe = recommend(self.nutritional_values, ingredients, {
            'n_neighbors': no_of_recommendations,
            'return_distance': False
        })
        recommendations = output_recommended_recipes(recommendation_dataframe)

        if recommendations is not None:
            for recipe in recommendations:
                recipe['image_link'] = get_images_links(recipe['Name'])

        return recommendations
