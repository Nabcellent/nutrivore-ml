import enum


class PredictionType(enum.Enum):
    Diet = 'diet'
    Custom = 'custom'


class GenderEnum(enum.Enum):
    M = 'Male'
    F = 'Female'


class ActivityEnum(enum.Enum):
    LittleNoExercise = 'Little/no exercise'
    LittleExercise = 'Light exercise'
    ModerateExercise = 'Moderate exercise (3-5 days/wk)'
    VeryActive = 'Very active (6-7 days/wk)'
    ExtraActive = 'Extra active (very active & physical job)'


class WeightLossPlanEnum(enum.Enum):
    Maintain = 'Maintain weight'
    MildLoss = 'Mild weight loss'
    Loss = 'Weight loss'
    ExtremeLoss = 'Extreme weight loss'
