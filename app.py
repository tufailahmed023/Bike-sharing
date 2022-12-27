from flask import Flask,request,render_template
from flask_cors import cross_origin
from Project import utils
from Project.config import Year,Months,Weather,Weekday,boll_deci,Season,columns_after_transformation
from Project.predictor import ModelResolver
import numpy as np
import pandas as pd

model_resolver = ModelResolver()
model =  utils.load_object(model_resolver.latest_model_path())
transformer = utils.load_object(model_resolver.latest_transformer_path())


app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")
      
@app.route("/predict",methods = ['GET','POST'])
@cross_origin()
def predict():
    if request.method == 'POST':
        #loading all the data
        #year
        final_year = request.form['year']
        #holiday
        final_holiday = request.form['holiday']
        #workingday
        final_workingday = request.form['workingday']
        #temp
        final_temp = int(request.form['temp']) / 41
        #atemp
        final_atemp = int(request.form['atemp']) / 50
        #hum
        final_hum = int(request.form['hum']) / 100
        #windspeed
        final_windspeed = int(request.form['windspeed']) / 67
        #season
        final_season = request.form['season']
        #month
        final_month = request.form['months']
        #weekday
        final_weekday = request.form['weekday']
        #weather
        final_weather = request.form['weather']

        #transforming the data
        if final_year in Year:
            final_year = Year[final_year]
        else:
            Year[final_year] = len(Year)+1
            final_year = Year[final_year]
        
        final_holiday = boll_deci[final_holiday]
        final_workingday = boll_deci[final_workingday]

        final_season = Season[final_season]
        final_month = Months[final_month]
        final_weekday = Weekday[final_weekday]
        final_weather = Weather[final_weather]

        list_of_int = [final_year,final_holiday,final_workingday,final_temp,final_atemp,final_hum,final_windspeed]
        list_of_list = [final_season,final_month,final_weekday,final_weather]
        merge_list_of_list = sum(list_of_list,[])

        merge_two_list = [list_of_int,merge_list_of_list]

        final_list = sum(merge_two_list,[])

        final_list = np.array(final_list).reshape(1,-1)
        
        prediction_df = pd.DataFrame(final_list,columns=columns_after_transformation)
        input_featurs = transformer.feature_names_in_
        prediction_df[input_featurs] = transformer.transform(prediction_df[input_featurs])
        #making the prediction 
        predicted_value = round(model.predict(prediction_df)[0])

        return render_template("home.html",predicition_text = f"The prdicted count of bike sharing is : {predicted_value}")

if __name__ == "__main__":
    app.run(debug=True)