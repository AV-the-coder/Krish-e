from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
import numpy as np
import pickle 

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secretkey"
db = SQLAlchemy(app)

#2021BCA017  @test1234

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#crop predict

crop_recommendation_model=pickle.load(open('./CropModel/trained_model.sav','rb'))

kees=list(range(0,22))
targets={0: 'apple',
 1: 'banana',
 2: 'blackgram',
 3: 'chickpea',
 4: 'coconut',
 5: 'coffee',
 6: 'cotton',
 7: 'grapes',
 8: 'jute',
 9: 'kidneybeans',
 10: 'lentil',
 11: 'maize',
 12: 'mango',
 13: 'mothbeans',
 14: 'mungbean',
 15: 'muskmelon',
 16: 'orange',
 17: 'papaya',
 18: 'pigeonpeas',
 19: 'pomegranate',
 20: 'rice',
 21: 'watermelon'}

def dataC(input_data):
    input_data_array=np.asarray(input_data) 
    reshape_array=input_data_array.reshape(1,-1)
    
    prediction=crop_recommendation_model.predict(reshape_array)
    

    if prediction[0] in kees:
        print("you should plant",targets.get(prediction[0]))
        return targets.get(prediction[0])
# crop complete


#fertilizer predict

fertname_dict={0: '10-26-26', 1: '14-35-14', 2: '17-17-17', 3: '20-20', 4: '28-28', 5: 'DAP', 6: 'Urea'}
cropType_dict={0: 'Barley', 1: 'Cotton', 2: 'Ground Nuts', 3: 'Maize', 4: 'Millets', 5: 'Oil seeds', 6: 'Paddy', 7: 'Pulses', 8: 'Sugarcane', 9: 'Tobacco', 10: 'Wheat'}
cropType_dict_key_list = list(cropType_dict.keys())
cropType_dict_val_list = list(cropType_dict.values())

soil_type_dict={0: 'Black', 1: 'Clayey', 2: 'Loamy', 3: 'Red', 4: 'Sandy'}
soilType_dict_key_list = list(soil_type_dict.keys())
soilType_dict_val_list = list(soil_type_dict.values())

fertilizer_recommendation_model=pickle.load(open('./FertilizerModel/trained_model_hj.sav','rb'))

def dataF(input_data):
    input_data_array=np.asarray(input_data)
    reshape_array=input_data_array.reshape(1,-1)
    
    prediction=fertilizer_recommendation_model.predict(reshape_array)
    

    if prediction[0] in [ i for i in range(7)] :
        print(fertname_dict.get(prediction[0])) 
        print(prediction)
        return (fertname_dict.get(prediction[0]))


#fertilizer complete

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False)
    fullname = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    mobileNumber = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(200), nullable = False)
    

    
    
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    fullname = StringField(validators=[
                        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Fullname"})
    
    email = StringField(validators=[
                           Email(), Length(min=8, max=20)], render_kw={"placeholder": "Email"})
    
    mobileNumber = StringField(validators=[
                           InputRequired(), Length(min=10, max=12)], render_kw={"placeholder": "Mobile Number"})


    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
            
            
    
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
    
    
class CropForm(FlaskForm):
    n = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Nitrogen Level"})

    p = StringField(validators=[
                             InputRequired()], render_kw={"placeholder": "Phosphorus Level"})
    
    k = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Potassium Level"})
    
    ph = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "PH Level"})
    
    rain = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Rainfall"})
    
    temp = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Temperature"})
    
    hum = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Humidity"})
    
    

    submit = SubmitField('Predict')
    
class FertilizerForm(FlaskForm):
    temp = StringField(validators=[
                           InputRequired()], render_kw={"placeholder": "Temperature"})

    hum = StringField(validators=[
                             InputRequired()], render_kw={"placeholder": "Humidity"})
    
    moist = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Moisture"})
    
    soil = SelectField(validators=[
                            InputRequired()], render_kw={"placeholder": "Soil Type"}, choices=[i for i in soil_type_dict.values()])
    
    crop = SelectField('Crop Type', choices=[i for i in cropType_dict.values()])
    
    n = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Nitrogen Level"})
    
    p = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Potassium Level"})
    
    k = StringField(validators=[
                            InputRequired()], render_kw={"placeholder": "Phosphorous Level"})
    
    # ph = StringField(validators=[
    #                         InputRequired()], render_kw={"placeholder": "PH Level"})
    
    # rain = StringField(validators=[
    #                         InputRequired()], render_kw={"placeholder": "Rainfall Level"})
    
    
    submit = SubmitField('Predict')
    
    

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/show")
def show():
    return render_template("show.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        if (form.email.data):
            new_user = User(username=form.username.data,fullname=form.fullname.data ,password=hashed_password, email = form.email.data, mobileNumber = form.mobileNumber.data)
        else:
            new_user = User(username=form.username.data,fullname=form.fullname.data ,password=hashed_password, email = "", mobileNumber = form.mobileNumber.data)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@ app.route('/cropPredict', methods=['POST', 'GET'])
@login_required
def crop_prediction():
    form = CropForm()
    title = 'Harvestify - Crop Recommendation'
    if form.validate_on_submit():
        N = float(form.n.data)
        P = float(form.p.data)
        K = float(form.k.data)
        ph = float(form.ph.data)
        rainfall = float(form.rain.data)
        temperature = float(form.temp.data)
        humidity = float(form.hum.data)
        pred=dataC([N,P,K,temperature,humidity, ph, rainfall])
        print(pred)
        return render_template('show.html', crop=pred)
    return render_template('crop.html', form=form)

@ app.route('/fertilizerPredict', methods=['POST', 'GET'])
@login_required
def fert_recommend():
    form = FertilizerForm()
    title = 'Harvestify - Fertilizer Suggestion'
    if form.validate_on_submit():
        Temperature=float(form.temp.data)
        Humidity=float(form.hum.data)
        Moisture=float(form.moist.data)
        Soil=(form.soil.data)
        Crop=(form.crop.data)
        Nitrogen=float(form.n.data)
        Potassium=float(form.p.data)
        Phosphorous=float(form.k.data)
        # ph=float(form.ph.data)
        # rainfall = float(form.rain.data)
        positionCrop = cropType_dict_val_list.index(Crop)
        CropType=cropType_dict_key_list[positionCrop]
        
        positionSoil = soilType_dict_val_list.index(Soil)
        SoilType= soilType_dict_key_list[positionSoil]
        
        pred=dataF([Temperature,Humidity,Moisture,SoilType,CropType,Nitrogen,Potassium,Phosphorous])
        print(pred)
        return render_template('showF.html', fert=pred)
    return render_template('fertilizer.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=8000)