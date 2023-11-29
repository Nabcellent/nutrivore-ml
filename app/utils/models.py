from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.enums import GenderEnum, ExerciseEnum, WeightLossPlanEnum


class Recipe(BaseModel):
    name: str
    image_link: str
    cook_time: str | int
    prep_time: str | int
    total_time: str | int
    recipe_ingredient_parts: list[str]
    calories: float
    fat_content: float
    saturated_fat_content: float
    cholesterol_content: float
    sodium_content: float
    carbohydrate_content: float
    fiber_content: float
    sugar_content: float
    protein_content: float
    recipe_instructions: list[str]


class DietResponse(BaseModel):
    meal: str
    recipes: List[Recipe]


class FoodPredictionResponse(BaseModel):
    data: Optional[List[DietResponse | Recipe]] = None


class DietPredictionRequest(BaseModel):
    age: int = Field(ge=2, le=120)
    height: int = Field(ge=50, le=300)
    weight: int = Field(ge=10, le=300)
    gender: GenderEnum
    exercise: ExerciseEnum
    meals_per_day: int = Field(ge=3, le=5)
    weight_loss_plan: WeightLossPlanEnum
    ingredients: list[str] = []
    no_of_recommendations: int = Field(3, gt=0, le=10)


class CustomPredictionRequest(BaseModel):
    calories: int = Field(ge=0, le=2000)
    fat: int = Field(ge=0, le=100)
    saturated_fat: int = Field(ge=0, le=13)
    cholesterol: int = Field(ge=0, le=300)
    sodium: int = Field(ge=0, le=2300)
    carbohydrate: int = Field(ge=0, le=325)
    fibre: int = Field(ge=0, le=50)
    sugar: int = Field(ge=0, le=40)
    protein: int = Field(ge=0, le=40)
    ingredients: list[str] = []
    no_of_recommendations: int = Field(3, gt=0, le=10)
