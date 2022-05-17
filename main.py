import os
from socket import AddressFamily
from sqlite3 import adapt
import sys
import requests
import json

from flask import Flask, make_response, send_file, send_from_directory
from flask import render_template
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__, static_folder='files')


@app.route("/")
def hello(name=None):
    return render_template('base.html', name=name)

@app.route("/forecast/")
def forecast(name=None):
    LAUSANNE_LATITUDE = 46.52751093142267
    LAUSANNE_LONGITUDE = 6.626519003698495
    r_pollution = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid=c6bbb95008347076780b7ce4a89f2224').json()
    r_forecast = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid=c6bbb95008347076780b7ce4a89f2224').json()
    #print(r_forecast,sys.stderr)
    #createimg()
    #convertotimg()
    createhtmlforecast(r_forecast)
    return render_template('tempforecast.html', name=name, forecast = r_forecast)

def createhtmlforecast(data):
    weather = []
    temp = []
    pressure = []
    humidity = []
    for elem in data["list"]:
        if(elem["dt_txt"].split(" ")[1] == "12:00:00"):
            weather.append(elem["weather"][0]["main"])
            temp.append(elem["main"]["temp"])
            pressure.append(elem["main"]["pressure"])
            humidity.append(elem["main"]["humidity"])
    content = """
        <!DOCTYPE html>
        <html lang="en" class="h-100">

        <head>
            <meta charset="UTF-8">
            <title>Hello World App</title>

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        </head>

        <style>
            .grid-content {
        display: grid;
        grid-template-columns: repeat(5 , minmax(32px, 1fr));
        gap: 2px;
        place-content: center;
        }
        .grid-content div {
        padding: 10px;
        background: #ddd;
        text-align: center;
        }

        </style>

        <body>

            <div class="jumbotron d-flex align-items-center justify-content-center min-vh-100">
                <div class="container-fluid">

                    <div class="row">
                        <div class="col">
                            <div class="card bg-light mx-auto">
                                <div class="card-body">
                                      <h1 class="display-3" style="text-align: center;">Forcast Weather</h1>
                                      <div class="grid-content">
                                        """
    from datetime import datetime
    tabday = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for i in range(0,5):   
        content += "<div><h5>" + tabday[i+1+int(datetime.today().weekday()) % 7] + """</h5>
                    """
        if(weather[i] == "Clouds"):
            content += """<svg width = "50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-2.12393 0 0 2.13534 1576.02-955.55)" x1="393.83" y1="549.46" x2="395.79" y2="542.83"><stop stop-color="#c8e1e8"/><stop offset="1" stop-color="#fff"/></linearGradient><linearGradient id="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)" x1="393.83" y1="549.46" x2="390.45" y2="542.88"><stop stop-color="#c3e6ee"/><stop offset="1" stop-color="#fff"/></linearGradient><linearGradient id="2" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)" x1="396.64" y1="546.11" x2="394.41" y2="538.61"><stop stop-color="#b7d7e1"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><g transform="matrix(1.06658 0 0 1.06658-745.92-181.44)"><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#2)" transform="matrix(1.21605 0 0 1.21605 343.92-455.87)"/><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#1)" transform="matrix(.7693 0 0 .7693 472.24-205.63)"/><path d="m743.78 199.48c.894-.702 2.02-1.119 3.235-1.119 2.87 0 5.205 2.315 5.279 5.2 2.963 1.124 5.071 4.01 5.071 7.402 0 4-2.942 7.31-6.759 7.831v.072h-27.04v-.013c-3.77-.221-6.759-3.382-6.759-7.25 0-3.73 2.78-6.802 6.36-7.215-.015-.227-.023-.457-.023-.688 0-5.78 4.823-10.466 10.773-10.466 4.404 0 8.19 2.567 9.861 6.245" fill="url(#0)"/></g></svg>"""
        elif(weather[i] == "Clear"):
            content += """<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88" width="50px"><defs><style>.cls-1{fill:#fcdb33;}</style></defs><title>sun-color</title><path class="cls-1" d="M30,13.21A3.93,3.93,0,1,1,36.8,9.27L41.86,18A3.94,3.94,0,1,1,35.05,22L30,13.21Zm31.45,13A35.23,35.23,0,1,1,36.52,36.52,35.13,35.13,0,0,1,61.44,26.2ZM58.31,4A3.95,3.95,0,1,1,66.2,4V14.06a3.95,3.95,0,1,1-7.89,0V4ZM87.49,10.1A3.93,3.93,0,1,1,94.3,14l-5.06,8.76a3.93,3.93,0,1,1-6.81-3.92l5.06-8.75ZM109.67,30a3.93,3.93,0,1,1,3.94,6.81l-8.75,5.06a3.94,3.94,0,1,1-4-6.81L109.67,30Zm9.26,28.32a3.95,3.95,0,1,1,0,7.89H108.82a3.95,3.95,0,1,1,0-7.89Zm-6.15,29.18a3.93,3.93,0,1,1-3.91,6.81l-8.76-5.06A3.93,3.93,0,1,1,104,82.43l8.75,5.06ZM92.89,109.67a3.93,3.93,0,1,1-6.81,3.94L81,104.86a3.94,3.94,0,0,1,6.81-4l5.06,8.76Zm-28.32,9.26a3.95,3.95,0,1,1-7.89,0V108.82a3.95,3.95,0,1,1,7.89,0v10.11Zm-29.18-6.15a3.93,3.93,0,0,1-6.81-3.91l5.06-8.76A3.93,3.93,0,1,1,40.45,104l-5.06,8.75ZM13.21,92.89a3.93,3.93,0,1,1-3.94-6.81L18,81A3.94,3.94,0,1,1,22,87.83l-8.76,5.06ZM4,64.57a3.95,3.95,0,1,1,0-7.89H14.06a3.95,3.95,0,1,1,0,7.89ZM10.1,35.39A3.93,3.93,0,1,1,14,28.58l8.76,5.06a3.93,3.93,0,1,1-3.92,6.81L10.1,35.39Z"></path></svg>"""
        else:
            content += """<svg width = "50" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64"><defs><linearGradient id="8" x1="-512.48" y1="-311.78" x2="-507.41" y2="-333.01" gradientUnits="userSpaceOnUse"><stop stop-color="#ff9300"/><stop offset="1" stop-color="#ffd702"/></linearGradient><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="5" xlink:href="#1" gradientTransform="matrix(.24869.02086-.02071.25039-610.69-323.28)"/><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="7" xlink:href="#1" gradientTransform="matrix(.23788.07548-.07572.23956-547.43-348.62)"/><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="6" xlink:href="#1" gradientTransform="matrix(.24144.06317-.06332.24313-553.91-335.79)"/><linearGradient gradientUnits="userSpaceOnUse" y2="-191.25" x2="-532.77" y1="-184.53" x1="-534.56" id="4" xlink:href="#1"/><linearGradient gradientUnits="userSpaceOnUse" y2="-187.54" x2="-502.64" y1="-178.75" x1="-504.46" id="3" xlink:href="#1"/><linearGradient y2="538.79" x2="394.7" y1="549.38" x1="396.46" gradientUnits="userSpaceOnUse" id="0" xlink:href="#1" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)"/><linearGradient gradientUnits="userSpaceOnUse" y2="-186.59" x2="-543.45" y1="-177.19" x1="-546.18" id="2" xlink:href="#1"/><linearGradient id="1"><stop stop-color="#7a808a"/><stop offset="1" stop-color="#ced8e0"/></linearGradient></defs><g transform="matrix(.74519 0 0 .74519 412.53 289.83)"><g transform="matrix(1.29586 0 0 1.29586-1506.97-589.71)"><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#0)" transform="matrix(1.41137 0 0 1.41137 320.53-578.44)"/><g transform="matrix(.66147 0 0 .66147 1114.42 325.53)"><path d="m-542.64-188.14l-4.894 4.727c-1.03 1-1.525 2.509-1.161 4.01.547 2.25 2.815 3.63 5.064 3.083 2.25-.547 3.63-2.815 3.083-5.064l-1.608-6.612c-.053-.218-.323-.297-.485-.141" fill="url(#2)"/><path d="m-502-189.02l-4.143 4.675c-.872.989-1.217 2.405-.777 3.749.661 2.02 2.834 3.122 4.855 2.461 2.02-.661 3.122-2.834 2.461-4.855l-1.942-5.937c-.064-.196-.317-.249-.454-.094" fill="url(#3)"/><path d="m-532.22-192.36l-3.401 3.438c-.716.728-1.043 1.808-.761 2.865.425 1.59 2.058 2.534 3.648 2.109 1.59-.425 2.534-2.058 2.109-3.648l-1.249-4.672c-.041-.154-.234-.206-.347-.092" fill="url(#4)"/><path d="m-538.48-175.91l-1.902 2.776c-.4.587-.492 1.369-.17 2.06.483 1.04 1.712 1.488 2.744 1 1.033-.486 1.478-1.723.995-2.763l-1.419-3.055c-.047-.101-.185-.112-.248-.021" fill="url(#5)"/><path d="m-508.03-178.22l-2.349 2.409c-.495.51-.719 1.264-.521 2 .298 1.107 1.431 1.759 2.532 1.457 1.101-.302 1.752-1.444 1.454-2.551l-.875-3.253c-.029-.107-.163-.142-.24-.063" fill="url(#6)"/><path d="m-509.7-188.91l-2.47 2.286c-.52.484-.783 1.226-.623 1.971.24 1.121 1.339 1.831 2.454 1.585 1.115-.245 1.823-1.353 1.583-2.473l-.707-3.294c-.023-.109-.155-.151-.237-.075" fill="url(#7)"/></g></g><path d="m-507.92-334.43l-9.587 11.662 6.469 3.5-1.676 8.162 9.587-11.662-6.469-3.5z" fill="url(#8)"/></g></svg>"""
        content += """<p><b>Temperature : </b> """ + str(round(temp[i]-273.15)) +"""&#176;C</p>
                    <p><b>Humidity : </b>""" + str(humidity[i]) +"""%</p>
                    <p><b>Pressure : </b>""" + str(pressure[i]) +""" mbar</p> </div>"""
    content += """
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>


     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>



    </body>

    </html>
    """

    file = open(os.path.abspath(app.static_folder + "/forecast.html"),"w")
    file.write(content)
    file.close()
    convertotimg()

def convertotimg():
    instructions = {
    'parts': [
        {
        'html': 'document'
        }
    ],
    "output": {
    "type": "image",
    "format": "png",
    "width": 1024
    }
    }

    response = requests.request(
    'POST',
    'https://api.pspdfkit.com/build',
    headers = {
        'Authorization': 'Bearer pdf_live_n0ZvClBNXTcOEP6CqMI7rjDwurXhQyy3aMWUf9vEGS2'
    },
    files = {
        'document': open(os.path.abspath(app.static_folder + "/forecast.html"), 'rb')
    },
    data = {
        'instructions': json.dumps(instructions)
    },
    stream = True
    )

    if response.ok:
        with open(os.path.abspath(app.static_folder + '/forecast.png'), 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
    return 1

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))