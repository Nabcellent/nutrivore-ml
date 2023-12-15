from random import uniform as rnd

from app.image_finder.image_finder import get_images_links
from app.models.kenya import KenyaModel
from app.utils.enums import ActivityEnum, WeightLossPlanEnum


class RecommendationController:
    def __init__(self, ingredients, no_of_recommendations):
        self.ingredients = ingredients
        self.no_of_recommendations = no_of_recommendations

    def recommend_diet(self, age, height, weight, gender, activity, weight_loss_plan, meals_per_day):
        weights = [1.1, 1, 0.9, 0.8, 0.6]
        plans = [el.value for el in WeightLossPlanEnum]
        weight_loss = weights[plans.index(weight_loss_plan)]
        total_calories = weight_loss * self.calories_calculator(activity, gender, weight, height, age)
        meals = {'breakfast': 0.3, 'morning snack': 0.05, 'lunch': 0.4, 'afternoon snack': 0.05, 'dinner': 0.2}

        if meals_per_day == 2:
            meals = {'breakfast': 0.6, 'early dinner': 0.4}
        elif meals_per_day == 3:
            meals = {'breakfast': 0.35, 'lunch': 0.4, 'dinner': 0.25}
        elif meals_per_day == 4:
            meals = {'breakfast': 0.3, 'morning snack': 0.1, 'lunch': 0.4, 'dinner': 0.2}

        recommendations = []
        for meal in meals:
            calories = meals[meal] * total_calories

            if meal == 'breakfast':
                values = [calories, rnd(14, 21), rnd(30, 75), rnd(20, 100), rnd(4, 10),
                          rnd(100, 200), rnd(2.2, 3.3), rnd(1, 4)]
            elif meal == 'lunch':
                values = [calories, rnd(18, 25), rnd(30, 75), rnd(40, 175), rnd(4, 20),
                          rnd(100, 200), rnd(2.75, 3.85), rnd(1, 4)]
            elif meal == 'dinner':
                values = [calories, rnd(20, 40), rnd(30, 75), rnd(40, 175), rnd(4, 20),
                          rnd(100, 200), rnd(3.3, 4.4), rnd(1, 4)]
            else:
                values = [calories, rnd(10, 30), rnd(30, 75), rnd(20, 100), rnd(4, 10),
                          rnd(100, 200), rnd(2.2, 3.3), rnd(1, 4)]

            model = KenyaModel(values)

            recommendation_dataframe = model.recommend(self.ingredients, {
                'n_neighbors': self.no_of_recommendations,
                'return_distance': False
            })

            recommended_recipes = model.output_recommended_recipes(recommendation_dataframe)
            recommendations.append({"meal": meal, "recipes": recommended_recipes})

        for recommendation in recommendations:
            for recipe in recommendation['recipes']:
                recipe['image_link'] = get_images_links(recipe['name'])

        return recommendations

    def recommend_custom(self, nutritional_values):
        model = KenyaModel(nutritional_values)

        recommendation_dataframe = model.recommend(self.ingredients, {
            'n_neighbors': self.no_of_recommendations,
            'return_distance': False
        })

        recommendations = model.output_recommended_recipes(recommendation_dataframe)

        if recommendations:
            for recipe in recommendations:
                recipe['image_link'] = get_images_links(recipe['name'])

        return recommendations

    def calculate_bmr(self, gender: str, weight: int, height: int, age: int):
        if gender == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        else:
            return 10 * weight + 6.25 * height - 5 * age - 161

    def calories_calculator(self, activity: str, gender: str, user_weight: int, height: int, age: int):
        activities = [el.value for el in ActivityEnum]
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight = weights[activities.index(activity)]
        maintain_calories = self.calculate_bmr(gender, user_weight, height, age) * weight

        return maintain_calories
