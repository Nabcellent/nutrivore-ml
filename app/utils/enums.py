import enum


class PredictionType(enum.Enum):
    Diet = 'diet'
    Custom = 'custom'


class GenderEnum(enum.Enum):
    M = 'male'
    F = 'female'


class ExerciseEnum(enum.Enum):
    LittleNoExercise = 'no exercise'
    LittleExercise = 'light exercise'
    ModerateExercise = 'moderate exercise (3-5 days/wk)'
    VeryActive = 'very active (6-7 days/wk)'
    ExtraActive = 'extra active (very active & physical job)'


class WeightLossPlanEnum(enum.Enum):
    Maintain = 'maintain weight'
    MildLoss = 'mild weight loss'
    Loss = 'weight loss'
    ExtremeLoss = 'extreme weight loss'
