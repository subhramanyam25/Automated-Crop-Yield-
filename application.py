
from flask import Flask, render_template, request, send_file
import numpy as np
import pickle
import requests
from datetime import datetime, timedelta
import json

model_model=pickle.load(open('models/model.pkl',"rb"))

app = Flask(__name__)

def weather_predict(city_name):

    url = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"
    querystring = {"city":city_name}
    headers = {

    "X-RapidAPI-Key": "1fb5719ecdmshb66a8a9cd24a45fp18fa8ajsn362a94b99f50",
	"X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    x=response.json()
    # print(x)
    if x.get("error") is None:
        min_temp=x["min_temp"]
        max_temp=x["max_temp"]
        rainfall=x["cloud_pct"]
        return min_temp,max_temp,rainfall
    else:
        return 10,30,10

# def prediction(input_data):
#     url = "https://mho77qbnu8.execute-api.ap-south-1.amazonaws.com/stage_1/devp"

#     # payload = "215.82,24.9,35.0,7.7,278.7,30.5,357.0,1.43,15.33,1.63,19.33,29.09,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1.0"
#     my_string = ','.join(map(str, input_data[0]))
#     # print(my_string)
#     headers = {
#     'Content-Type': 'text/csv'
#     }

#     response = requests.request("POST", url, headers=headers, data=my_string)

#     #print(response.text)
#     res=response.json()
#     return res["Prediction"] 

@app.route("/")
def start_page():
    return render_template("index.html")





@app.route("/predict_yield", methods=["GET", "POST"])
def predict_page():


    if request.method == "POST":
        rainfall = float(request.form["rainfall"])
        min_temp = float(request.form["min_temp"])
        max_temp = float(request.form["max_temp"])
        ph = float(request.form["ph"])
        n = float(request.form["n"])
        p = float(request.form["p"])
        k = float(request.form["k"])
        zn = float(request.form["zn"])
        fe = float(request.form["fe"])
        cu = float(request.form["cu"])
        mn = float(request.form["mn"])
        irrigation = float(request.form["irrigation"])
        district_mapping = {
            "Adilabad": 0,
            "Bhadradri Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Jayashankar": 4,
            "Jogulamba": 5,
            "Kamareddy": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "Komaram bheem asifabad": 9,
            "Mahabubabad": 10,
            "Mahabubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Mulugu": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Rajanna": 22,
            "Rangareddy": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Wanaparthy": 28,
            "Warangal": 29,
            "Warangal Urban": 30,
            "Yadadri": 31,
        }

        district = request.form["district"]
        district_index = district_mapping[district]
        district_encoded = np.zeros(32)
        district_encoded[district_index] = 1


        season_mapping ={
            "Kharif":0,
            "rabi":1,
        }
        season = request.form["season"]
        season_index = season_mapping[season]
        season_encoded = np.zeros(2)
        season_encoded[season_index] = 1
        
        
        crop_mapping = {
            "Crop_Groundnut": 0,
            "Crop_Maize": 1,
            "Crop_Moong(Green Gram)": 2,
            "Crop_Rice": 3,
            "Crop_cotton(lint)": 4,
        }
        crop = request.form["crop"]
        crop_index = crop_mapping[crop]
        crop_encoded = np.zeros(5)
        crop_encoded[crop_index] = 1
          

        test_input = np.array(
            [
                [
                    rainfall,
                    min_temp,
                    max_temp,
                    ph,
                    n,
                    p,
                    k,
                    zn,
                    fe,
                    cu,
                    mn,
                    irrigation,
                    *district_encoded,
                    *season_encoded,
                    *crop_encoded,
                ]
            ]
        )
        #print(test_input)
        #result=prediction(test_input)
        result=model_model.predict(test_input)
        return render_template("yield.html",result=result[0])
    else:
        return render_template("yield.html")

@app.route('/another-page')
def another_page():
    return render_template('data.html')


@app.route('/another1-page')
def another1_page():
    return render_template('yieldnext.html')

    
district_mapping = {
            "Adilabad": 0,
            "Bhadradri Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Jayashankar": 4,
            "Jogulamba": 5,
            "Kamareddy": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "Komaram bheem asifabad": 9,
            "Mahabubabad": 10,
            "Mahabubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Mulugu": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Rajanna": 22,
            "Rangareddy": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Wanaparthy": 28,
            "Warangal": 29,
            "Warangal Urban": 30,
            "Yadadri": 31,

    # Add more district mappings here
}

season_mapping ={
    "Kharif": 0,
    "Rabi": 1,
    # Add more season mappings here
}

crop_mapping = {
    "Crop_Groundnut": 0,
    "Crop_Maize": 1,
    "Crop_Moong(Green Gram)": 2,
    "Crop_Rice": 3,
    "Crop_cotton(lint)": 4,
    # Add more crop mappings here
}




@app.route('/yield')
def yield_page():
    return render_template('indexyield.html')


@app.route('/another2-page')
def another2_page():
    return render_template('index.html')

@app.route('/download')
def download():
    # Path to the file you want to download
    file_path = 'dataset/FINAL-Dataset-csv.csv'

    # Send the file to the client for download
    return send_file(file_path, as_attachment=True)


@app.route("/default_yield", methods=["GET", "POST"])
def default_page():
    if request.method == "POST":
        

        
        district_mapping = {
            "Adilabad": 0,
            "Bhadradri Kothagudem": 1,
            "Jagtial": 2,
            "Jangaon": 3,
            "Jayashankar": 4,
            "Jogulamba": 5,
            "Kamareddy": 6,
            "Karimnagar": 7,
            "Khammam": 8,
            "Komaram bheem asifabad": 9,
            "Mahabubabad": 10,
            "Mahabubnagar": 11,
            "Mancherial": 12,
            "Medak": 13,
            "Medchal": 14,
            "Mulugu": 15,
            "Nagarkurnool": 16,
            "Nalgonda": 17,
            "Narayanpet": 18,
            "Nirmal": 19,
            "Nizamabad": 20,
            "Peddapalli": 21,
            "Rajanna": 22,
            "Rangareddy": 23,
            "Sangareddy": 24,
            "Siddipet": 25,
            "Suryapet": 26,
            "Vikarabad": 27,
            "Wanaparthy": 28,
            "Warangal": 29,
            "Warangal Urban": 30,
            "Yadadri": 31,
        }

        # Retrieve the index of the selected district
        district = request.form["district"]
        district_index = district_mapping[district]
        district_encoded = np.zeros(32)
        district_encoded[district_index] = 1


        season_mapping ={
            "Kharif":0,
            "rabi":1,
        }
        season = request.form["season"]
        season_index = season_mapping[season]
        season_encoded = np.zeros(2)
        season_encoded[season_index] = 1
        
        
        crop_mapping = {
            "Crop_Groundnut": 0,
            "Crop_Maize": 1,
            "Crop_Moong(Green Gram)": 2,
            "Crop_Rice": 3,
            "Crop_cotton(lint)": 4,
        }
        crop = request.form["crop"]
        crop_index = crop_mapping[crop]
        crop_encoded = np.zeros(5)
        crop_encoded[crop_index] = 1
        
        min_temp,max_temp ,cloud_pct= weather_predict(district)

        test_input = np.array(
            [
                [
                    cloud_pct,
                    min_temp,
                    max_temp,
                    7.257323944,
                    219.5738468,
                    34.36901408,
                    304.3738028,
                    1.370602817,
                    13.66366197,
                    1.883211268,
                    12.78577465,
                    11.35644869,
                    *district_encoded,
                    *season_encoded,
                    *crop_encoded,
                ]
            ]
        )
        #result=prediction(test_input)
        result=model_model.predict(test_input)
        return render_template("yield2.html", result=result[0])
    else:
        default_values = {
            "rainfall": 86.78491341,
            "min_temp": 24.08427214,
            "max_temp": 41.1943379,
            "ph": 7.257323944,
            "n": 219.5738468,
            "p": 34.36901408,
            "k": 304.3738028,
            "zn": 1.370602817,
            "fe": 13.66366197,
            "cu": 1.883211268,
            "mn": 12.78577465,
            "irrigation": 11.35644869,
        }
        
        return render_template("yield2.html", default_values=default_values)

if __name__ == "__main__":
    app.run(host="0.0.0.0")