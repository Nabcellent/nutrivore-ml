from re import sub
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.recommend.custom import RecommendCustom
from app.recommend.diet import RecommendDiet
from app.utils.enums import WeightLossPlanEnum
from app.utils.models import FoodPredictionResponse, DietPredictionRequest, CustomPredictionRequest, Recipe

dataset = pd.read_csv('data/dataset.csv', compression='gzip')
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    errors = []
    for error in exc.errors():
        detail = {
            "loc": list(error["loc"]),
            "msg": error["msg"],
        }
        errors.append(detail)

    return JSONResponse(
        status_code=422,
        content={"message": f'{errors[0]["loc"][1]}: {errors[0]["msg"]}', "errors": errors},
    )


@app.get("/")
def home():
    return {"health_check": "OK"}


# Define a function to convert a string to snake case
def snake_case(s):
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def convert_keys_to_snake_case(data):
    if isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    elif isinstance(data, dict):
        return {snake_case(key): convert_keys_to_snake_case(value) for key, value in data.items()}
    else:
        return data


@app.post("/api/predict-diet/", response_model=FoodPredictionResponse)
def predict_diet(req: DietPredictionRequest):
    if req.meals_per_day == 3:
        meals_calories_perc = {'breakfast': 0.35, 'lunch': 0.40, 'dinner': 0.25}
    elif req.meals_per_day == 4:
        meals_calories_perc = {'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'dinner': 0.25}
    else:
        meals_calories_perc = {'breakfast': 0.30, 'morning snack': 0.05, 'lunch': 0.40, 'afternoon snack': 0.05,
                               'dinner': 0.20}

    weights = [1, 0.9, 0.8, 0.6]
    plans = [el.value for el in WeightLossPlanEnum]
    weight_loss_plan = weights[plans.index(req.weight_loss_plan.value)]

    diet = RecommendDiet(
        req.age,
        req.height,
        req.weight,
        req.gender.value,
        req.exercise.value,
        meals_calories_perc,
        weight_loss_plan
    )

    recommendations = diet.generate_recommendations(req.ingredients, req.no_of_recommendations)

    return {"data": convert_keys_to_snake_case(recommendations)}


@app.post("/api/predict-custom/", response_model=FoodPredictionResponse)
def predict_custom(req: CustomPredictionRequest):
    nutrition_values_list = [req.calories, req.fat, req.saturated_fat, req.cholesterol, req.sodium,
                             req.carbohydrate, req.fibre, req.sugar, req.protein]

    custom = RecommendCustom(nutrition_values_list)
    recommendations = custom.generate_recommendations(req.ingredients, req.no_of_recommendations)

    return {"data": convert_keys_to_snake_case(recommendations)}
