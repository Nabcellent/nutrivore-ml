from random import uniform as rnd

from app.image_finder.image_finder import get_images_links
from app.utils.enums import ActivityEnum
from app.models.general import recommend, output_recommended_recipes


class RecommendDiet:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss

    def calculate_bmi(self, ):
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)

        return bmi

    def display_result(self, ):
        bmi = self.calculate_bmi()
        bmi_string = f'{bmi} kg/m²'
        if bmi < 18.5:
            category = 'Underweight'
            color = 'Red'
        elif 18.5 <= bmi < 25:
            category = 'Normal'
            color = 'Green'
        elif 25 <= bmi < 30:
            category = 'Overweight'
            color = 'Yellow'
        else:
            category = 'Obesity'
            color = 'Red'
        return bmi_string, category, color

    def calculate_bmr(self):
        if self.gender == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        return bmr

    def calories_calculator(self):
        activities = [el.value for el in ActivityEnum]
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight = weights[activities.index(self.activity)]
        maintain_calories = self.calculate_bmr() * weight

        return maintain_calories

    def generate_recommendations(self, ingredients, no_of_recommendations):
        total_calories = self.weight_loss * self.calories_calculator()
        recommendations = []

        for meal in self.meals_calories_perc:
            meal_calories = self.meals_calories_perc[meal] * total_calories

            if meal == 'breakfast':
                recommended_nutrition = [meal_calories, rnd(10, 30), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75),
                                         rnd(4, 10), rnd(0, 10), rnd(30, 100)]
            elif meal == 'lunch':
                recommended_nutrition = [meal_calories, rnd(20, 40), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75),
                                         rnd(4, 20), rnd(0, 10), rnd(50, 175)]
            elif meal == 'dinner':
                recommended_nutrition = [meal_calories, rnd(20, 40), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75),
                                         rnd(4, 20), rnd(0, 10), rnd(50, 175)]
            else:
                recommended_nutrition = [meal_calories, rnd(10, 30), rnd(0, 4), rnd(0, 30), rnd(0, 400), rnd(40, 75),
                                         rnd(4, 10), rnd(0, 10), rnd(30, 100)]

            recommendation_dataframe = recommend(recommended_nutrition, ingredients, {
                'n_neighbors': no_of_recommendations,
                'return_distance': False
            })

            recommended_recipes = output_recommended_recipes(recommendation_dataframe)

            if recommended_recipes:
                recommendations.append({"meal": meal, "recipes": recommended_recipes})

        for recommendation in recommendations:
            for recipe in recommendation['recipes']:
                recipe['image_link'] = get_images_links(recipe['Name'])

        return recommendations
