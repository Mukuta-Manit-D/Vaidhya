from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
import joblib
import smtplib
import pandas as pd
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from docx import Document
from datetime import datetime, timedelta, timezone
import os
import random

config = ConfigParser()
config.read("config.ini")

app = Flask(__name__)

app.secret_key = config["SECRETS"]["APP_SECRET_KEY"]

translate_api_url = config["URL"]["TRANSLATE_URL"]
chatbot_api_url = config["URL"]["CHATBOT_URL"]
feel_api_url = config["URL"]["FEEL_URL"]

model = joblib.load("static/models/disease_prediction_model.joblib")
le_results = joblib.load("static/models/label_encoder_results.joblib")

client = MongoClient(config["DATABASE"]["STRING"])
db = client[config["DATABASE"]["DATABASE_NAME"]]
collection_pl = db[config["DATABASE"]["COLLECTION_PATIENT_LOGIN"]]
collection_dl = db[config["DATABASE"]["COLLECTION_DOCTOR_LOGIN"]]
collection_data = db[config["DATABASE"]["COLLECTION_DATA"]]
collection_as = db[config["DATABASE"]["COLLECTION_APPOINTMENT_STATUS"]]
collection_a = db[config["DATABASE"]["COLLECTION_APPOINTMENT"]]
collection_pi = db[config["DATABASE"]["COLLECTION_PATIENT_INFORMATION"]]
collection_di = db[config["DATABASE"]["COLLECTION_DOCTOR_INFORMATION"]]
collection_c = db[config["DATABASE"]["COLLECTION_CONSULTATION"]]
collection_o = db[config["DATABASE"]["OTP"]]
collection_n = db[config["DATABASE"]["NUMBERS"]]

main_patientusername = ""
main_doctorusername = ""
main_doctorname = ""
temp_username = ""
gemail = ""
new_username = ""
new_email = ""
docnew_username = ""
docnew_email = ""
temp_email = ""

ALLOWED_ROUTES = ["/index"]

def allowed_route(route):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if route in ALLOWED_ROUTES:
                return func(*args, **kwargs)
            else:
                return redirect(url_for("error_404"))
        wrapper._name_ = func._name_
        return wrapper
    return decorator

@app.route("/error")
def error_404():
    return render_template("error.html"), 404

@app.route("/errorfetch")
def error_500():
    return render_template("errorfetch.html"), 500

@app.route("/")
def login():
    try:
        return render_template("index.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/index")
def index():
    try:
        return render_template("index.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/dashboard")
def dashboard():
    error = "DASH1"
    try:
        # Ensure the patient is logged in
        if not main_patientusername:
            return redirect(url_for("login"))

        # Fetch all appointments for the patient
        patient_appointments = collection_a.find({"patient_username": main_patientusername})
        appointments = []
        for appointment in patient_appointments:
            doctor_info = collection_di.find_one({"_id": appointment.get("doctor_id")})
            appointments.append({
                "date": appointment["date"],
                "time_slot": appointment["time_slot"],
                "mode": appointment["mode"],
                "doctor_name": doctor_info["doctor_name"] if doctor_info else "Unknown",
                "location": doctor_info["location"] if doctor_info else "Unknown",
            })

        return render_template("dashboard.html", appointments=appointments)
    except Exception as e:
        return render_template("errorfetch.html", message=f"{error}: {str(e)}"), 500
    
@app.route("/about")
def about():
    try:
        return render_template("about.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/diseasePrediction")
def diseasePrediction():
    try:
        return render_template("2options.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/prediction1")
def prediction1():
    try:
        return render_template("prediction.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/mcq")
def mcq():
    try:
        return render_template("mcq.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/chatbot")
def chatbot():
    try:
        return render_template("chatbot.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/predic")
def predic():
    try:
        return render_template("predic.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/predict2")
def predict2():
    try:
        return render_template("prediction.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/doctorLogin")
def doctorLogin():
    try:
        return render_template("doctorLogin.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/doctordashboard")
def doctordashboard():
    try:
        return render_template("doctordashboard.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/appointments")
def appointments():
    try:
        return render_template("appointment.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/patientReport")
def patientReport():
    try:
        return render_template("patientReport.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/docappointment")
def docappointment():
    try:
        return render_template("docappointment.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/forgotpassword")
def forgotpassword():
    try:
        return render_template("forgotpassword.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/otp")
def otp():
    try:
        return render_template("otp.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/createpassword")
def createpassword():
    try:
        return render_template("createpassword.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/docforgotpassword")
def docforgotpassword():
    try:
        return render_template("docforgotpassword.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/docotp")
def docotp():
    try:
        return render_template("docotp.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/doccreatepassword")
def doccreatepassword():
    try:
        return render_template("createpassword.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/newusername")
def newusername():
    try:
        return render_template("newusername.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/newotp")
def newotp():
    try:
        return render_template("newotp.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/newemail")
def newemail():
    try:
        return render_template("newemail.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/createnewpassword")
def createnewpassword():
    try:
        return render_template("createnewpassword.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/docnewusername")
def docnewusername():
    try:
        return render_template("docnewusername.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/docnewemail")
def docnewemail():
    try:
        return render_template("docnewemail.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/docnewotp")
def docnewotp():
    try:
        return render_template("docnewotp.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/doccreatenewpassword")
def doccreatenewpassword():
    try:
        return render_template("doccreatenewpassword.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/admin")
def admin():
    try:
        return render_template("admin.html")
    except:
        return render_template("error.html"), 404
    
@app.route("/emailsent", methods=["POST"])
def emailsent():
    error = "ESEX1"
    try:
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            message = request.form["message"]
            sender_email = config["EMAIL"]["SENDER_EMAIL"]
            sender_password = config["EMAIL"]["SENDER_PASSWORD"]
            to_email = config["EMAIL"]["RECEIVER_EMAIL"]
            subject = "Response form Vaidhya"
            body = f"Sender Name: {name}\nSender Email: {email}\nMessage: {message}"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            return render_template("about.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/ask", methods=["POST"])
def ask():
    error = "CHTGC1"
    try:
        questions = request.get_json().get("question")
        response = requests.post(
            f"{chatbot_api_url}/input_bot", json={"questions": questions}
        )
        if response.status_code == 200:
            answers = response.json().get("answer")
            print(answers)
            return jsonify({"answers": answers})
        else:
            return jsonify({"error": "Failed to get answers"})
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/mcqfun1", methods=["GET", "POST"])
def mcqfun1():
    error = "MCQXE1"
    try:
        q1 = request.form["q1"]
        q2 = request.form["q2"]
        q3 = request.form["q3"]
        q4 = request.form["q4"]
        q5 = request.form["q5"]
        q6 = request.form["q6"]
        q7 = request.form["q7"]
        q8 = request.form["q8"]
        q9 = request.form["q9"]
        q10 = request.form["q10"]
        input_data = {
            "age": 22,
            "Your friend has invited you to a party. Consider how you might respond in the given scenario. Choose the option that best reflects your feelings and tendencies": q1,
            "You have an upcoming deadline at work. How do you typically handle this": q2,
            "You receive unexpected praise for your achievements. How do you react?": q3,
            "You witness a car accident on the street. How does it affect you?": q4,
            "You are preparing for a social event with friends. How do you approach it?": q5,
            "You find yourself in a crowded and noisy environment. How do you react?": q6,
            "You encounter a trigger related to a past traumatic event. How do you cope?": q7,
            "You are faced with a decision that requires careful consideration. How do you approach it?": q8,
            "You are experiencing a period of heightened creativity and productivity. How does it impact you?": q9,
            "You are in a situation where you feel judged by others. How do you react?": q10,
        }
        answer_mapping = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7}
        for mcq, answer in input_data.items():
            if mcq != "age":
                input_data[mcq] = answer_mapping.get(answer, 0)
        input_df = pd.DataFrame([input_data])
        predictions = model.predict(input_df.iloc[:, 1:])
        predictions_decoded = le_results.inverse_transform(predictions)
        symptom = predictions_decoded[0]
        existing_student = collection_data.find_one({"_id": main_patientusername})
        if existing_student:
            collection_data.update_one(
                {"_id": main_patientusername}, {"$set": {"symptom-test": symptom}}
            )
        return render_template("predic.html", symp=symptom)
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/translate", methods=["POST"])
def translate():
    error = "TRANGC2"
    try:
        data = request.get_json()
        texts = data.get("texts", [])
        target_lang = data.get("target_lang", "en")
        response = requests.post(
            f"{translate_api_url}/translate",
            json={"texts": texts, "target_lang": target_lang},
        )
        if response.status_code == 200:
            translated_texts = response.json().get("translated_texts", [])
            return jsonify({"translated_texts": translated_texts})
        else:
            return jsonify({"error": "Failed to get translation"})
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/loginsuccessfull", methods=["GET", "POST"])
def validate_login():
    error = "LOGUS1"
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            print(username, password)
            required_one = {"_id": username, "password": password}
            data = collection_pl.find_one(required_one)
            if data:
                global main_patientusername, main_doctorname, main_doctorusername
                main_patientusername = username
                try:
                    patient_info = collection_pi.find_one(
                        {"patient_username": username}
                    )
                    patient_id = patient_info["_id"]
                    consultation = collection_c.find_one({"_id": patient_id})
                    doctor_id = consultation["doctor_id"]
                    doctor_info = collection_di.find_one({"_id": doctor_id})
                    main_doctorname = doctor_info["doctor_name"]
                    main_doctorusername = doctor_info["doctor_username"]
                except:
                    pass
                if not collection_pi.find_one(
                    {"patient_username": main_patientusername}
                ):
                    return render_template("patientinfo.html")
                return render_template("dashboard.html")
            else:
                return render_template(
                    "index.html", message="Invalid username and password!"
                )
        return render_template("index.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/userfeeling", methods=["GET", "POST"])
def userfeeling():
    error = "USFGC3"
    try:
        if request.method == "POST":
            userfeeling = request.form["feeling"]
            try:
                response = requests.post(
                    f"{feel_api_url}/feel_bot", json={"question": userfeeling}
                )
                if response.status_code == 200:
                    answer = response.json().get("answer")
                symptom = answer
                existing_student = collection_data.find_one(
                    {"_id": main_patientusername}
                )
                if existing_student:
                    collection_data.update_one(
                        {"_id": main_patientusername},
                        {"$set": {"symptom-feel": symptom}},
                    )
            except:
                return render_template("prediction.html", symptom="Error 429!")
            return render_template("prediction.html", symptom=symptom)
        else:
            return render_template("prediction.html", symptom=None)
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/doctorloginsuccessfull", methods=["GET", "POST"])
def validate_doctor_login():
    error = "LOGUS2"
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            print(username, password)
            required_one = {"_id": username, "password": password}
            data = collection_dl.find_one(required_one)
            if data:
                global main_doctorusername
                main_doctorusername = username
                if not collection_di.find_one({"doctor_username": main_doctorusername}):
                    return render_template("doctorinfo.html")
                return render_template("doctordashboard.html")
            else:
                return render_template(
                    "doctorLogin.html", message="Invalid username and password!"
                )
        return render_template("doctorLogin.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/fetchpatientdetails", methods=["GET", "POST"])
def fetchpatientdetails():
    error = "FPDEX1"
    patientid = " "
    patientname = " "
    patientage = " "
    sfeel = " "
    stest = " "
    message = "Data Not Available"
    doc_name = " "
    doc_id = " "
    try:
        if request.method == "POST":
            patientid = request.form["patientid"]
            key = request.form["key"]
            required_one = {"patientid": patientid, "key": key}
            data = collection_data.find_one(required_one)
            if data:
                message = "Data Found!"
                patientid = data["patientid"]
                patientname = data["patientname"]
                patientage = data["age"]
                sfeel = data["symptom-feel"]
                stest = data["symptom-test"]
                doc_name = data["doctor_name"]
                doc_id = data["doctor_id"]
                return render_template(
                    "patientReport.html",
                    message=message,
                    name=patientname,
                    pid=patientid,
                    age=patientage,
                    sfeel=sfeel,
                    stest=stest,
                    doc_name=doc_name,
                    doc_id=doc_id,
                )
            else:
                return render_template(
                    "patientReport.html",
                    message=message,
                    name=patientname,
                    pid=patientid,
                    age=patientage,
                    sfeel=sfeel,
                    stest=stest,
                    doc_name=doc_name,
                    doc_id=doc_id,
                )
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/generatereport", methods=["GET"])
def generatereport():
    error = "GENRP1"
    try:
        name = request.args.get("name")
        pid = request.args.get("pid")
        age = request.args.get("age")
        sfeel = request.args.get("sfeel")
        stest = request.args.get("stest")
        docid = request.args.get("docid")
        docname = request.args.get("docname")
        data = {
            "name": name,
            "pid": pid,
            "age": age,
            "sfeel": sfeel,
            "stest": stest,
            "doctor_id": docid,
            "doctor_name": docname,
        }
        now = datetime.now()
        current_month = str(now.month)
        current_date = str(now.day)
        current_year = str(now.year)
        data["DD"] = current_date
        data["MM"] = current_month
        data["YYYY"] = current_year
        try:
            doc = Document("static/documents/patient_report.docx")
        except:
            errorone = "DOC404"
            return render_template("errorfetch.html", message=errorone), 500
        for paragraph in doc.paragraphs:
            for key, value in data.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(
                        "{{" + key + "}}", str(value)
                    )
        documentsgen_dir = os.path.join(app.root_path, "static", "documentsgen")
        os.makedirs(documentsgen_dir, exist_ok=True)
        fname = data["pid"]
        temp_docx_path = os.path.join(documentsgen_dir, f"{fname}.docx")
        doc.save(temp_docx_path)
        return send_file(temp_docx_path, as_attachment=True)
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/appointment")
def appointment():
    error = "GAP1AP"
    try:
        # Ensure the doctor is logged in
        if not main_doctorusername:
            return redirect(url_for("doctorLogin"))

        # Fetch the doctor's details
        doc = collection_di.find_one({"doctor_username": main_doctorusername})
        if not doc:
            return render_template("errorfetch.html", message="Doctor not found"), 404

        doc_id = doc["_id"]

        # Fetch all time slots for the doctor
        time_slots = collection_as.find({"_id": {"$regex": f"^{doc_id}-"}})
        dates_with_availability = []
        for slot in time_slots:
            date = slot["_id"].split("-")[-1]
            slots_availability = {
                key: value for key, value in slot.items() if key != "_id"
            }
            dates_with_availability.append((date, slots_availability))

        # Debug: Log the available dates and slots
        print("Available dates and slots:", dates_with_availability)

        # Pass the data to the template
        return render_template(
            "appointment.html",
            dates_with_availability=dates_with_availability,
            doctor_name=main_doctorname,
        )
    except Exception as e:
        print(f"Error in appointment route: {e}")
        return render_template("errorfetch.html", message=f"{error}: {str(e)}"), 500

@app.route("/appointment/submitted", methods=["POST", "GET"])
def submit_appointment():
    error = "GAP1SP"
    try:
        # Ensure the doctor is logged in
        if not main_doctorusername:
            return jsonify({"message": "Doctor is not logged in. Please log in again."}), 400

        # Fetch the doctor's details
        doc = collection_di.find_one({"doctor_username": main_doctorusername})
        if not doc:
            return jsonify({"message": "Doctor details not found. Please log in again."}), 404

        doc_id = doc['_id']

        # Check if the request is JSON or form-encoded
        if request.is_json:
            appointment_data = request.get_json()
        else:
            appointment_data = request.form.to_dict()

        # Debug: Log the incoming request data
        print("Incoming appointment data:", appointment_data)

        # Validate the appointment data
        if not appointment_data:
            return jsonify({"message": "Request body is empty."}), 400

        # Extract appointment details
        name = appointment_data.get("name")
        pid = appointment_data.get("pid")
        time_slot = appointment_data.get("timeSlot")
        mode = appointment_data.get("mode")
        date = appointment_data.get("dates")

        # Debug: Log the extracted fields
        print(f"Extracted details - Name: {name}, PID: {pid}, Time Slot: {time_slot}, Mode: {mode}, Date: {date}")

        # Validate required fields
        missing_fields = [field for field in ["name", "pid", "timeSlot", "mode", "dates"] if not appointment_data.get(field)]
        if missing_fields:
            return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Update the time slot in the database
        query = {"_id": f"{doc_id}-{date}"}
        newquery = {"$set": {time_slot: 1}}
        update_result = collection_as.update_one(query, newquery)
        if update_result.matched_count == 0:
            return jsonify({"message": "Failed to update time slot. Please try again."}), 400

        # Insert the new appointment into the database
        new_appointment = {
            "id": f"{pid}{date}_{time_slot}",
            "name": name,
            "patient_username": pid,
            "time_slot": time_slot,
            "mode": mode,
            "date": date,
            "doctor_id": doc_id,
            "doctor_name": main_doctorname,
        }
        collection_a.insert_one(new_appointment)

        # Debug: Log the successful booking
        print("Appointment booked successfully:", new_appointment)

        # Return success response
        response_data = {"message": "Appointment submitted successfully!"}
        return jsonify(response_data)

    except Exception as e:
        # Log the exception for debugging
        print(f"Error in submit_appointment: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
       
@app.route("/docappointment/submitted", methods=["POST", "GET"])
def submit_docappointment():
    error = "GAP2DAP"
    try:
        # Ensure main_doctorusername is set
        if not main_doctorusername:
            return jsonify({"message": "Doctor username is missing. Please log in again."}), 400

        appointment_docdata = request.get_json()
        if appointment_docdata:
            if (
                not appointment_docdata.get("timeSlots")
                and not appointment_docdata.get("customTimeSlot")
            ):
                response_data = {"message": "Select Atleast One Time slot!"}
                return jsonify(response_data)

            datek = datetime.strptime(appointment_docdata["date"], "%Y-%m-%d")
            date = datek.strftime("%d-%m-%Y")
            time_slots = []
            doc = collection_di.find_one({"doctor_username": main_doctorusername})
            if not doc:
                return jsonify({"message": "Doctor details not found. Please log in again."}), 400

            doc_id = doc['_id']
            result = {"_id": doc_id + "-" + date}
            for time_slot in appointment_docdata.get("timeSlots", []):
                time_slots.append(time_slot)
            if appointment_docdata.get("customTimeSlot"):
                time = (
                    appointment_docdata["customTimeSlot"]["from"]
                    + " - "
                    + appointment_docdata["customTimeSlot"]["to"]
                    + " IST"
                )
                time_slots.append(time)

            def check_overlap(time1, time2):
                start1, end1 = map(
                    lambda x: int(x.split(":")[0]) * 60
                    + int(x.split(":")[1].split()[0]),
                    time1.split(" - "),
                )
                start2, end2 = map(
                    lambda x: int(x.split(":")[0]) * 60
                    + int(x.split(":")[1].split()[0]),
                    time2.split(" - "),
                )
                if start1 <= start2 <= end1 or start1 <= end2 <= end1:
                    return True
                if start2 <= start1 <= end2 or start2 <= end1 <= end2:
                    return True
                return False

            for i in range(len(time_slots)):
                for j in range(i + 1, len(time_slots)):
                    if check_overlap(time_slots[i], time_slots[j]):
                        response_data = {
                            "message": "Select the Time Slots Such that they don't overlap with each other"
                        }
                        return jsonify(response_data)

            for t_s in time_slots:
                result[t_s] = 1  # Set the value to 1 to indicate the time slot is chosen

            if collection_as.find_one({"_id": result["_id"]}):
                collection_as.delete_one({"_id": result["_id"]})
            collection_as.insert_one(result)

            response_data = {"message": "Appointments Offered Successfully!"}
            return jsonify(response_data)
        else:
            response_data = {"message": "Something Went Wrong!"}
            return jsonify(response_data)
    except Exception as e:
        return render_template("errorfetch.html", message=f"{error}: {str(e)}"), 500
    
import traceback

@app.route("/forgotpassword/datafound", methods=["POST", "GET"])
def forgotpassworddatafound():
    error = "FPPS1"
    try:
        username = request.form["login-username"]
        print(f"Received username: {username}")

        if collection_pl.find_one({"_id": username}) or collection_pl.find_one({"email": username}):
            pin = int("".join(random.choices("0123456789", k=6)))
            global temp_username

            if collection_pl.find_one({"_id": username}):
                temp_username = username
                data = collection_pl.find_one({"_id": username})
            else:
                temp_username = collection_pl.find_one({"email": username})["_id"]
                data = collection_pl.find_one({"email": username})

            email = data["email"]
            print(f"Found user: {temp_username}, Email: {email}")

            sender_email = config["EMAIL"]["SENDER_EMAIL"]
            sender_password = config["EMAIL"]["SENDER_PASSWORD"]

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "One Time Password"
            message.attach(MIMEText(f"Your OTP is {pin}. Valid for 10 minutes.", "plain"))

            # SMTP Connection
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, email, message.as_string())
                print("Email sent successfully")
            except Exception as smtp_error:
                print(f"SMTP Error: {smtp_error}")
                return render_template("errorfetch.html", message=f"Email error: {smtp_error}"), 500

            collection_o.create_index("createdAt", expireAfterSeconds=600)
            to_push = {"createdAt": datetime.now(timezone.utc), "_id": email, "otp": pin}

            if collection_o.find_one({"_id": email}):
                collection_o.update_one({"_id": email}, {"$set": {"otp": pin}})
            else:
                collection_o.insert_one(to_push)

            return render_template("otp.html")

        else:
            return render_template("forgotpassword.html", message="Invalid username or email")

    except Exception as e:
        print("Error:", traceback.format_exc())  # Print full error traceback
        return render_template("errorfetch.html", message=f"{error}: {str(e)}"), 500

    
@app.route("/otpverified", methods=["POST", "GET"])
def otpverified():
    error = "OTPVF1"
    try:
        one = request.form["input1"]
        two = request.form["input2"]
        three = request.form["input3"]
        four = request.form["input4"]
        five = request.form["input5"]
        six = request.form["input6"]
        pin = int(one + two + three + four + five + six)
        make_data = collection_pl.find_one({"_id": temp_username})
        email = make_data["email"]
        make_datax = collection_o.find_one({"_id": email})
        otp_from_mongo = make_datax["otp"]
        if otp_from_mongo == pin:
            return render_template("createpassword.html")
        else:
            return render_template("otp.html", message="Invalid OTP")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/createpasswordsuccessfull", methods=["POST", "GET"])
def createpasswordsuccessfull():
    error = "CPPS1"
    try:
        appointment_data = request.get_json()
        password1 = appointment_data["password1"]
        password2 = appointment_data["password2"]
        print(password1, password2)
        if password1 != password2:
            print(password1, password2)
            return jsonify(message="Password did not match !")
        else:
            if collection_pl.find_one({"_id": temp_username}):
                query = {"_id": temp_username}
                new_query = {"$set": {"password": password1}}
                collection_pl.update_one(query, new_query)
                return jsonify(message="Password Changed Successfully !")
            return render_template("error.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docforgotpassword/docdatafound", methods=["POST", "GET"])
def docforgotpassworddatafound():
    error = "FPDC1"
    try:
        username = request.form["login-username"]
        if collection_dl.find_one({"_id": username}) or collection_dl.find_one(
            {"email": username}
        ):
            pin = int("".join(random.choices("0123456789", k=6)))
            global temp_doc_username
            if collection_dl.find_one({"_id": username}):
                temp_doc_username = username
                data = collection_dl.find_one({"_id": username})
                email = data["email"]
            else:
                global temp_email
                temp_email = username
                data = collection_dl.find_one({"email": username})
                email = data["email"]
                temp_doc_username = data["_id"]
            sender_email = config["EMAIL"]["SENDER_EMAIL"]
            sender_password = config["EMAIL"]["SENDER_PASSWORD"]
            to_email = email
            subject = "One Time Password"
            body = f"Your One Time Password is {pin}.\n\nThe OTP will be valid only for 10 minutes.\n\nRegards,\nVaidhya"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            collection_o.create_index("createdAt", expireAfterSeconds=600)
            to_push = {
                "createdAt": datetime.now(timezone.utc),
                "_id": email,
                "otp": pin,
            }
            if collection_o.find_one({"_id": email}):
                query = {"_id": email}
                newquery = {"$set": {"otp": pin}}
                collection_o.update_one(query, newquery)
            else:
                collection_o.insert_one(to_push)
            return render_template("docotp.html")
        else:
            return render_template(
                "docforgotpassword.html", message="Invalid Credentials"
            )
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docotpverified", methods=["POST", "GET"])
def docotpverified():
    error = "OTPVF2"
    try:
        one = request.form["input1"]
        two = request.form["input2"]
        three = request.form["input3"]
        four = request.form["input4"]
        five = request.form["input5"]
        six = request.form["input6"]
        pin = int(one + two + three + four + five + six)
        make_data = collection_dl.find_one({"_id": temp_doc_username})
        email = make_data["email"]
        make_datax = collection_o.find_one({"_id": email})
        otp_from_mongo = make_datax["otp"]
        if otp_from_mongo == pin:
            return render_template("doccreatepassword.html")
        else:
            return render_template("docotp.html", message="Invalid OTP")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/doccreatepasswordsuccessfull", methods=["POST", "GET"])
def doccreatepasswordsuccessfull():
    error = "CPDC1"
    try:
        appointment_data = request.get_json()
        password1 = appointment_data["password1"]
        password2 = appointment_data["password2"]
        print(password1, password2)
        if password1 != password2:
            print(password1, password2)
            return jsonify(message="Password did not match !")
        else:
            if collection_dl.find_one({"_id": temp_doc_username}):
                query = {"_id": temp_doc_username}
                new_query = {"$set": {"password": password1}}
                collection_dl.update_one(query, new_query)
                return jsonify(message="Password Changed Successfully !")
            return render_template("error.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/chooseusername", methods=["POST", "GET"])
def chooseusername():
    error = "CHUSPS1"
    try:
        username = request.form["login-username"]
        if collection_pl.find_one({"_id": username}):
            return render_template("newusername.html", message="username alreay exist!")
        else:
            global new_username
            new_username = username
            return render_template("newemail.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
import traceback

@app.route("/chooseemail", methods=["POST", "GET"])
def chooseemail():
    error = "CHEMPS1"
    try:
        email = request.form["login-username"]
        if collection_pl.find_one({"email": email}):
            return render_template("newemail.html", message="email already registered!")
        else:
            global new_email
            new_email = email
            pin = int("".join(random.choices("0123456789", k=6)))
            sender_email = config["EMAIL"]["SENDER_EMAIL"]
            sender_password = config["EMAIL"]["SENDER_PASSWORD"]
            to_email = new_email
            subject = "One Time Password"
            body = f"Your One Time Password is {pin}.\n\nThe OTP will be valid only for 10 minutes.\n\nRegards,\nVaidhya"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            collection_o.create_index("createdAt", expireAfterSeconds=600)
            to_push = {
                "createdAt": datetime.now(timezone.utc),
                "_id": new_email,
                "otp": pin,
            }
            if collection_o.find_one({"_id": new_email}):
                query = {"_id": new_email}
                newquery = {"$set": {"otp": pin}}
                collection_o.update_one(query, newquery)
            else:
                collection_o.insert_one(to_push)
            return render_template("newotp.html")
    except Exception as e:
        print(f"CHEMPS1 Error: {str(e)}")
        print(traceback.format_exc())  # This will print the full error traceback
        return render_template("errorfetch.html", message=error), 500

    
@app.route("/newotpverified", methods=["POST", "GET"])
def newotpverified():
    error = "OTPNVF1"
    try:
        one = request.form["input1"]
        two = request.form["input2"]
        three = request.form["input3"]
        four = request.form["input4"]
        five = request.form["input5"]
        six = request.form["input6"]
        pin = int(one + two + three + four + five + six)
        print(new_email)
        make_datax = collection_o.find_one({"_id": new_email})
        otp_from_mongo = make_datax["otp"]
        if otp_from_mongo == pin:
            return render_template("createnewpassword.html")
        else:
            return render_template("newotp.html", message="Invalid OTP")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/createaccount", methods=["POST", "GET"])
def createacount():
    error = "CREAAC1"
    try:
        appointment_data = request.get_json()
        password1 = appointment_data["password1"]
        password2 = appointment_data["password2"]
        if password1 != password2:
            print(password1, password2)
            return jsonify(message="Password did not match !")
        else:
            account = {"_id": new_username, "email": new_email, "password": password1}
            collection_pl.insert_one(account)
            return jsonify(message="Account Created Successfully !")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/savedetails", methods=["POST", "GET"])
def savedetails():
    error = "SVDL1"
    try:
        appointment_data = request.get_json()
        if not collection_pi.find_one({"patient_username": main_patientusername}):
            date = appointment_data["DOB"]
            date_object = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_object.strftime("%d-%m-%Y")
            dob_date = datetime.strptime(formatted_date, "%d-%m-%Y")
            current_date = datetime.now()
            agek = (
                current_date.year
                - dob_date.year
                - (
                    (current_date.month, current_date.day)
                    < (dob_date.month, dob_date.day)
                )
            )
            mongo = collection_n.find_one({"_id": "patient-register-number"})
            mongox = collection_pl.find_one({"_id": main_patientusername})
            value = mongo["value"]
            query = {"_id": "patient-register-number"}
            newquery = {"$set": {"value": value + 1}}
            collection_n.update_one(query, newquery)
            p_id = "VP" + str(value + 1)
            patient_username = main_patientusername
            DOB = str(formatted_date)
            age = agek
            address = appointment_data["address"]
            blood_group = appointment_data["bloodgroup"]
            ph_number = appointment_data["contactnumber"]
            email = mongox["email"]
            patient_name = appointment_data["name"]
            data = {
                "_id": p_id,
                "patient_username": patient_username,
                "DOB": DOB,
                "age": age,
                "address": address,
                "blood_group": blood_group,
                "ph_number": ph_number,
                "email": email,
                "patient_name": patient_name,
            }
            print(data)
            data_health = {
                "_id":patient_username,
                "age":age,
                "symptom-feel": "",
                "symptom-test": "",
                "key": "",
                "patientid": p_id,
                "patientname": patient_name,
                "doctor_name": "",
                "doctor_id": ""
            }
            collection_pi.insert_one(data)
            collection_data.insert_one(data_health)
            return jsonify(message="Details Saved successfully!")
        else:
            date = appointment_data["DOB"]
            date_object = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_object.strftime("%d-%m-%Y")
            dob_date = datetime.strptime(formatted_date, "%d-%m-%Y")
            current_date = datetime.now()
            agek = (
                current_date.year
                - dob_date.year
                - (
                    (current_date.month, current_date.day)
                    < (dob_date.month, dob_date.day)
                )
            )
            DOB = str(formatted_date)
            age = agek
            address = appointment_data["address"]
            blood_group = appointment_data["bloodgroup"]
            ph_number = appointment_data["contactnumber"]
            patient_name = appointment_data["name"]
            query = {"patient_username": main_patientusername}
            query_n_d_h = {"_id": main_patientusername}
            newquery = {
                "$set": {
                    "DOB": DOB,
                    "age": age,
                    "address": address,
                    "blood_group": blood_group,
                    "ph_number": ph_number,
                    "patient_name": patient_name,
                }
            }
            new_data_health = {
                "$set": {
                    "age":age,
                    "patientname": patient_name,
                }
            }
            collection_pi.update_one(query, newquery)
            collection_data.update_one(query_n_d_h, new_data_health)
            return jsonify(message="Data Updated successfully!")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docchooseusername", methods=["POST", "GET"])
def docchooseusername():
    error = "CHUSDC1"
    try:
        username = request.form["login-username"]
        if collection_dl.find_one({"_id": username}):
            return render_template(
                "docnewusername.html", message="username alreay exist!"
            )
        else:
            global docnew_username
            docnew_username = username
            print(docnew_username)
            return render_template("docnewemail.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docchooseemail", methods=["POST", "GET"])
def docchooseemail():
    error = "CHMPDC1"
    try:
        email = request.form["login-username"]
        if collection_dl.find_one({"email": email}):
            return render_template(
                "docnewemail.html", message="email already registered!"
            )
        else:
            global docnew_email
            docnew_email = email
            pin = int("".join(random.choices("0123456789", k=6)))
            sender_email = config["EMAIL"]["SENDER_EMAIL"]
            sender_password = config["EMAIL"]["SENDER_PASSWORD"]
            to_email = email
            subject = "One Time Password"
            body = f"Your One Time Password is {pin}.\n\nThe OTP will be valid only for 10 minutes.\n\nRegards,\nVaidhya"
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            collection_o.create_index("createdAt", expireAfterSeconds=600)
            to_push = {
                "createdAt": datetime.now(timezone.utc),
                "_id": email,
                "otp": pin,
            }
            if collection_o.find_one({"_id": email}):
                query = {"_id": email}
                newquery = {"$set": {"otp": pin}}
                collection_o.update_one(query, newquery)
            else:
                collection_o.insert_one(to_push)
            return render_template("docnewotp.html")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docnewotpverified", methods=["POST", "GET"])
def docnewotpverified():
    error = "OTPVFDC1"
    try:
        one = request.form["input1"]
        two = request.form["input2"]
        three = request.form["input3"]
        four = request.form["input4"]
        five = request.form["input5"]
        six = request.form["input6"]
        pin = int(one + two + three + four + five + six)
        make_datax = collection_o.find_one({"_id": docnew_email})
        otp_from_mongo = make_datax["otp"]
        if otp_from_mongo == pin:
            print("Hello")
            return render_template("doccreatenewpassword.html")
        else:
            return render_template("docnewotp.html", message="Invalid OTP")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/doccreateaccount", methods=["POST", "GET"])
def doccreateacount():
    error = "CREAADC1"
    try:
        appointment_data = request.get_json()
        password1 = appointment_data["password1"]
        password2 = appointment_data["password2"]
        if password1 != password2:
            print(password1, password2)
            return jsonify(message="Password did not match !")
        else:
            account = {
                "_id": docnew_username,
                "email": docnew_email,
                "password": password1,
            }
            collection_dl.insert_one(account)
            return jsonify(message="Account Created Successfully !")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docsavedetails", methods=["POST", "GET"])
def docsavedetails():
    error = "SAVDDC1"
    try:
        appointment_data = request.get_json()
        if not collection_di.find_one({"doctor_username": main_doctorusername}):
            date = appointment_data["DOB"]
            date_object = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_object.strftime("%d-%m-%Y")
            dob_date = datetime.strptime(formatted_date, "%d-%m-%Y")
            current_date = datetime.now()
            agek = (
                current_date.year
                - dob_date.year
                - (
                    (current_date.month, current_date.day)
                    < (dob_date.month, dob_date.day)
                )
            )
            mongo = collection_n.find_one({"_id": "doctor-register-number"})
            mongox = collection_dl.find_one({"_id": main_doctorusername})
            value = mongo["value"]
            query = {"_id": "doctor-register-number"}
            newquery = {"$set": {"value": value + 1}}
            collection_n.update_one(query, newquery)
            d_id = "VD" + str(value + 1)
            doctor_username = main_doctorusername
            DOB = str(formatted_date)
            age = agek
            address = appointment_data["address"]
            blood_group = appointment_data["bloodgroup"]
            ph_number = appointment_data["contactnumber"]
            email = mongox["email"]
            doctor_name = appointment_data["name"]
            room = appointment_data["consultancyroomnumber"]
            location = appointment_data["consultancylocation"]
            consultation_address = appointment_data["consultancyaddress"]
            licence_number = appointment_data["licence"]
            aadhar = appointment_data["aadhar"]
            data = {
                "_id": d_id,
                "doctor_username": doctor_username,
                "DOB": DOB,
                "age": age,
                "address": address,
                "blood_group": blood_group,
                "ph_number": ph_number,
                "email": email,
                "doctor_name": doctor_name,
                "room": room,
                "location": location,
                "consultation_address": consultation_address,
                "licence_number": licence_number,
                "aadhar": aadhar,
            }
            collection_di.insert_one(data)
            return jsonify(message="Details Saved successfully!")
        else:
            date = appointment_data["DOB"]
            date_object = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_object.strftime("%d-%m-%Y")
            dob_date = datetime.strptime(formatted_date, "%d-%m-%Y")
            current_date = datetime.now()
            agek = (
                current_date.year
                - dob_date.year
                - (
                    (current_date.month, current_date.day)
                    < (dob_date.month, dob_date.day)
                )
            )
            DOB = str(formatted_date)
            age = agek
            address = appointment_data["address"]
            blood_group = appointment_data["bloodgroup"]
            ph_number = appointment_data["contactnumber"]
            doctor_name = appointment_data["name"]
            room = appointment_data["consultancyroomnumber"]
            location = appointment_data["consultancylocation"]
            consultation_address = appointment_data["consultancyaddress"]
            licence_number = appointment_data["licence"]
            aadhar = appointment_data["aadhar"]
            query = {"doctor_username": main_doctorusername}
            newquery = {
                "$set": {
                    "DOB": DOB,
                    "age": age,
                    "address": address,
                    "blood_group": blood_group,
                    "ph_number": ph_number,
                    "doctor_name": doctor_name,
                    "room": room,
                    "location": location,
                    "consultation_address": consultation_address,
                    "licence_number": licence_number,
                    "aadhar": aadhar,
                }
            }
            collection_di.update_one(query, newquery)
            return jsonify(message="Data Updated successfully!")
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/accountinfo", methods=["POST", "GET"])
def accountinfo():
    error = "ACCINFPS1"
    try:
        data = collection_pi.find_one({"patient_username": main_patientusername})
        if data:
            DOBK = data["DOB"]
            DOB = datetime.strptime(DOBK, "%d-%m-%Y").strftime("%Y-%m-%d")
            address = data["address"]
            blood_group = data["blood_group"]
            ph_number = data["ph_number"]
            patient_name = data["patient_name"]
        return render_template(
            "accountinfo.html",
            DOB=DOB,
            address=address,
            blood_group=blood_group,
            ph_number=ph_number,
            patient_name=patient_name,
        )
    except:
        return render_template("errorfetch.html", message=error), 500
    
@app.route("/docaccountinfo", methods=["POST", "GET"])
def docaccountinfo():
    error = "ACCINFDC2"
    try:
        data = collection_di.find_one({"doctor_username": main_doctorusername})
        if data:
            DOBK = data["DOB"]
            DOB = datetime.strptime(DOBK, "%d-%m-%Y").strftime("%Y-%m-%d")
            address = data["address"]
            blood_group = data["blood_group"]
            ph_number = data["ph_number"]
            doctor_name = data["doctor_name"]
            aadhar = data["aadhar"]
            licence_number = data["licence_number"]
            consultation_address = data["consultation_address"]
            location = data["location"]
            room = data["room"]
            print(DOB)
            print(doctor_name)
            print(aadhar)
        return render_template(
            "docaccountinfo.html",
            DOB=DOB,
            address=address,
            blood_group=blood_group,
            ph_number=ph_number,
            doctor_name=doctor_name,
            aadhar=aadhar,
            licence_number=licence_number,
            consultation_address=consultation_address,
            location=location,
            room=room,
        )
    except:
        return render_template("errorfetch.html", message=error), 500
    
if __name__ == "__main__":
    app.run(debug=True)