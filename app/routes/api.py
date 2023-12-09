from fastapi import APIRouter

from app.controllers.recommendation_controller import RecommendationController
from app.recommend.custom import RecommendCustom
from app.recommend.diet import RecommendDiet
from app.utils.enums import WeightLossPlanEnum
from app.utils.helpers import convert_keys_to_snake_case
from app.utils.models import FoodPredictionResponse, DietPredictionRequest, CustomPredictionRequest, \
    CustomPredictionKERequest

router = APIRouter()


@router.post("/predict/ke/custom", response_model=FoodPredictionResponse)
def predict_custom_ke(req: CustomPredictionKERequest):
    values = [req.energy, req.fat, req.carbohydrate, req.protein, req.fibre, req.vitamin_a, req.iron, req.zinc]

    recommender = RecommendationController(req.ingredients, req.no_of_recommendations)

    recommendations = recommender.recommend_custom(values)

    return {"data": recommendations}


@router.post("/predict/ke/diet", response_model=FoodPredictionResponse)
def predict_diet_ke(req: DietPredictionRequest):
    recommender = RecommendationController(req.ingredients, req.no_of_recommendations)

    recommendations = recommender.recommend_diet(
        req.age,
        req.height,
        req.weight,
        req.gender.value,
        req.activity.value,
        req.weight_loss_plan.value,
        req.meals_per_day
    )

    return {"data": recommendations}


@router.post("/predict-diet", response_model=FoodPredictionResponse)
def predict_diet(req: DietPredictionRequest):
    if req.meals_per_day == 3:
        meals_calories_percent = {'breakfast': 0.35, 'lunch': 0.40, 'dinner': 0.25}
    elif req.meals_per_day == 4:
        meals_calories_percent = {'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'dinner': 0.25}
    else:
        meals_calories_percent = {'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'afternoon snack': 0.05,
                                  'dinner': 0.20}

    weights = [1, 0.9, 0.8, 0.6]
    plans = [el.value for el in WeightLossPlanEnum]
    weight_loss_plan = weights[plans.index(req.weight_loss_plan.value)]

    diet = RecommendDiet(
        req.age,
        req.height,
        req.weight,
        req.gender.value,
        req.activity.value,
        meals_calories_percent,
        weight_loss_plan
    )

    recommendations = diet.generate_recommendations(req.ingredients, req.no_of_recommendations)

    return {"data": convert_keys_to_snake_case(recommendations)}


@router.post("/predict-custom", response_model=FoodPredictionResponse)
def predict_custom(req: CustomPredictionRequest):
    nutrition_values_list = [req.calories, req.fat, req.saturated_fat, req.cholesterol, req.sodium,
                             req.carbohydrate, req.fibre, req.sugar, req.protein]

    custom = RecommendCustom(nutrition_values_list)
    recommendations = custom.generate_recommendations(req.ingredients, req.no_of_recommendations)

    return {"data": convert_keys_to_snake_case(recommendations)}
