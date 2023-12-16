from random import uniform as rnd, randint

from app.image_finder.image_finder import get_images_links
from app.models.kenya import KenyaModel
from app.utils.enums import ActivityEnum, WeightLossPlanEnum, Meal


class RecommendationController:
    def __init__(self, ingredients, no_of_recommendations):
        self.ingredients = ingredients
        self.no_of_recommendations = no_of_recommendations

    def recommend_diet(self, age, height, weight, gender, activity, weight_loss_plan, meals_per_day):
        weights = [1.1, 1, 0.9, 0.8, 0.6]
        plans = [el.value for el in WeightLossPlanEnum]
        weight_loss = weights[plans.index(weight_loss_plan)]
        total_calories = weight_loss * self.calories_calculator(activity, gender, weight, height, age)
        meals = {
            Meal.Breakfast: 0.3,
            Meal.MorningSnack: 0.05,
            Meal.Lunch: 0.4,
            Meal.AfternoonSnack: 0.05,
            Meal.Dinner: 0.2
        }

        if meals_per_day == 2:
            meals = {Meal.Breakfast: 0.6, Meal.EarlyDinner: 0.4}
        elif meals_per_day == 3:
            meals = {Meal.Breakfast: 0.35, Meal.Lunch: 0.4, Meal.Dinner: 0.25}
        elif meals_per_day == 4:
            meals = {Meal.Breakfast: 0.3, Meal.MorningSnack: 0.1, Meal.Lunch: 0.4, Meal.Dinner: 0.2}

        recommendations = []
        for meal in meals:
            calories = meals[meal] * total_calories

            if meal == Meal.Breakfast:
                values = [calories, rnd(14, 35), rnd(10, 75), rnd(20, 50), rnd(2, 10),
                          rnd(30, 200), rnd(2.2, 20), rnd(1, 7)]
            elif meal == Meal.Lunch:
                values = [calories, rnd(18, 35), rnd(10, 75), rnd(40, 90), rnd(2, 20),
                          rnd(30, 200), rnd(2.75, 18), rnd(1, 7)]
            elif meal == Meal.Dinner:
                values = [calories, rnd(20, 40), rnd(10, 75), rnd(40, 90), rnd(2, 20),
                          rnd(30, 200), rnd(3.3, 16), rnd(1, 7)]
            else:
                values = [calories, rnd(10, 35), rnd(10, 75), rnd(20, 50), rnd(2, 10),
                          rnd(30, 200), rnd(2.2, 14), rnd(1, 7)]

            model = KenyaModel(meal, [v / randint(2, 4) for v in values])

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
