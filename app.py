from flask import *
import joblib

app = Flask(__name__)

def sex(Sex):
    Sex_M = 0
    Sex_F = 0
    
    if Sex == 'M':
        Sex_M = 1
    elif Sex == 'F':
        Sex_F = 1
    
    return Sex_M, Sex_F

def chestpain(ChestPainType):
    ChestPainType_ATA = 0
    ChestPainType_NAP = 0
    ChestPainType_ASY = 0
    ChestPainType_TA  = 0

    if ChestPainType == 'ATA':
        ChestPainType_ATA = 1
    elif ChestPainType == 'NAP':
        ChestPainType_NAP = 1
    elif ChestPainType == 'ASY':
        ChestPainType_ASY = 1
    elif ChestPainType == 'TA':
        ChestPainType_TA = 1
        
    return ChestPainType_ATA, ChestPainType_NAP, ChestPainType_ASY, ChestPainType_TA

def restingecg(RestingECG):
    RestingECG_Normal = 0
    RestingECG_ST     = 0
    RestingECG_LVH    = 0

    if RestingECG == 'Normal':
        RestingECG_Normal = 1
    elif RestingECG == 'ST':
        RestingECG_ST = 1
    elif RestingECG == 'LVH':
        RestingECG_LVH = 1

    return RestingECG_Normal, RestingECG_ST, RestingECG_LVH

def angina(ExerciseAngina):
    ExerciseAngina_N = 0
    ExerciseAngina_Y = 0

    if ExerciseAngina == 'N':
        ExerciseAngina_N = 1
    elif ExerciseAngina == 'Y':
        ExerciseAngina_Y = 1

    return ExerciseAngina_N, ExerciseAngina_Y

def stslope(ST_Slope):
    ST_Slope_Up   = 0
    ST_Slope_Flat = 0
    ST_Slope_Down = 0

    if ST_Slope == 'Up':
        ST_Slope_Up = 1
    elif ST_Slope == 'Flat':
        ST_Slope_Flat = 1
    elif ST_Slope == 'Down':
        ST_Slope_Down = 1

    return ST_Slope_Up, ST_Slope_Flat, ST_Slope_Down

model = joblib.load('model_rf_after.pkl')

@app.route("/", methods=['GET', 'POST'])
def home():
    
    str_prediction = ''
    
    if request.method == 'POST':
        Age = int(request.form['Age'])
        RestingBP = int(request.form['RestingBP'])
        Cholesterol = int(request.form['Cholesterol'])
        FastingBS = int(request.form['FastingBS'])
        MaxHR = int(request.form['MaxHR'])
        Oldpeak = float(request.form['Oldpeak'])
        Sex_M, Sex_F = sex(str(request.form['Sex']))
        ChestPainType_ATA, ChestPainType_NAP, \
        ChestPainType_ASY, ChestPainType_TA = chestpain(str(request.form['ChestPainType']))
        RestingECG_Normal, RestingECG_ST, RestingECG_LVH = restingecg(str(request.form["RestingECG"]))
        ExerciseAngina_N, ExerciseAngina_Y = angina(str(request.form["ExerciseAngina"]))
        ST_Slope_Up, ST_Slope_Flat, ST_Slope_Down = stslope(str(request.form["ST_Slope"]))
        
        ls_data = [Age, RestingBP, Cholesterol, FastingBS, MaxHR, Oldpeak, \
                   Sex_F, Sex_M, \
                   ChestPainType_ASY, ChestPainType_ATA, ChestPainType_NAP, ChestPainType_TA, \
                   RestingECG_LVH, RestingECG_Normal, RestingECG_ST, \
                   ExerciseAngina_N, ExerciseAngina_Y, \
                   ST_Slope_Down, ST_Slope_Flat, ST_Slope_Up]
        
        prediction_results = model.predict([ls_data])
        prediction_results = prediction_results[0]
        
        if prediction_results == 1:
            str_prediction = 'You may have heart disease. Please check your condition to the doctor.'
        elif prediction_results == 0:
            str_prediction = 'Congratulations, You are in excellent condition! Keep your heart in good condition by embracing a healthy lifestyle.'

        
    return render_template("index.html", str_prediction=str_prediction)


