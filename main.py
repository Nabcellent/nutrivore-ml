from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.recommend.custom import RecommendCustom
from app.recommend.diet import RecommendDiet
from app.utils.enums import WeightLossPlanEnum
from app.utils.helpers import convert_keys_to_snake_case
from app.utils.models import FoodPredictionResponse, DietPredictionRequest, CustomPredictionRequest

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://nutrivore-web-dkuvi4xfka-uc.a.run.app",
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
