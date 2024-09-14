from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
import requests
import json
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

global_token = ""

class SignupScreen(Screen):
    
    def get_mobile_number(self):
        mobile_number = self.ids.mobile_number.text
        self.validate_mobile_number(mobile_number)

    def validate_mobile_number(self,mobile_number):
        if not (len(mobile_number) == 10 and mobile_number.isdigit()):
            self.ids.error_label.text = "Mobile number should be 10 digit number"
        else:
            print(mobile_number)
            self.send_otp_to_mobile_number(mobile_number)

    def send_otp_to_mobile_number(self,mobile_number):
        self.ids.get_otp.disabled = True
        self.ids.otp.disabled = False
        self.ids.submit.disabled = False
        self.send_otp_to_mobile_number_api(mobile_number)

    def send_otp_to_mobile_number_api(self,mobile_number):
        api_url = "http://localhost:8000/send-otp/"
        data = {"mobile_number":mobile_number}
        try:
            response = requests.post(api_url, json = data)
            get_data = json.loads(response.text)
            if response.status_code == 201 :
                self.ids.error_label.text = get_data['data']['message']
            else:
                self.ids.error_label.text = "Error in sending OTP"
        except Exception as e:
            print("Generated exception is:",str(e))
            self.ids.error_label.text = "Error in Sending OTP"

    def signup_process(self):
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        mobile_number = self.ids.mobile_number.text
        otp = self.ids.otp.text
        self.validate(first_name,last_name,mobile_number,otp)

    def validate(self,first_name,last_name,mobile_number,otp):
        if first_name is None:
            self.ids.error_label.text = "first_name should not be empty"
        if last_name is None:
            self.ids.error_label.text = "last_name should not be empty"
        if mobile_number is None:
            self.ids.error_label.text = "mobile_number should not be empty"
        if otp is None:
            self.ids.error_label.text = "OTP should not be empty"
        self.send_data_to_signup_api(first_name,last_name,mobile_number,otp)

    def send_data_to_signup_api(self,first_name,last_name,mobile_number,otp):
        api_url = "http://localhost:8000/signup/"
        data = {"first_name":first_name,
                "last_name":last_name,
                "mobile_number":mobile_number,
                "otp":otp}
        try:
            response = requests.post(api_url, json = data)
            get_data = json.loads(response.text)
            print(get_data)
            if response.status_code == 201 :
                home_screen = MyApp.get_running_app().root.get_screen("home")
                home_screen.ids.token_field.text = get_data["Access_Token"]
                print(f'token {get_data["Access_Token"]}')
                home_screen.ids.token_field.opacity = 0
                MyApp.get_running_app().root.current = "home"
               
        except Exception as e:
            print("Generated exception is:",str(e))
            self.ids.error_label.text = "Error in creating the user"


class LoginScreen(Screen):
    def get_mobile_number(self):
        mobile_number = self.ids.mobile_number.text
        self.validate_mobile_number(mobile_number)
    
    def validate_mobile_number(self,mobile_number):
        if not (len(mobile_number) == 10 and mobile_number.isdigit()):
            self.ids.error_label.text = "Mobile number should be 10 digit number"
        else:
            print(mobile_number)
            self.send_otp_to_mobile_number(mobile_number)

    def send_otp_to_mobile_number(self,mobile_number):
        self.ids.get_otp.disabled = True
        self.ids.otp.disabled = False
        self.ids.submit.disabled = False
        self.send_otp_to_mobile_number_api(mobile_number)


    def send_otp_to_mobile_number_api(self,mobile_number):
        api_url = "http://localhost:8000/send-otp/"
        data = {"mobile_number":mobile_number}
        try:
            response = requests.post(api_url, json = data)
            get_data = json.loads(response.text)
            if response.status_code == 201 :
                self.ids.error_label.text = get_data['data']['message']
            else:
                self.ids.error_label.text = "Error in sending OTP"
        except Exception as e:
            print("Generated exception is:",str(e))
            self.ids.error_label.text = "Error in Sending OTP"
    
    def signin_process(self):
        mobile_number = self.ids.mobile_number.text
        otp = self.ids.otp.text
        self.validate(mobile_number,otp)
    
    def validate(self,mobile_number,otp):
        if mobile_number is None:
            self.ids.error_label.text = "mobile_number should not be empty"
        if otp is None:
            self.ids.error_label.text = "OTP should not be empty"
        self.send_data_to_signin_api(mobile_number,otp)

    def send_data_to_signin_api(self,mobile_number,otp):
        api_url = "http://localhost:8000/signin/"
        data = {"mobile_number":mobile_number,"otp":otp}
        try:
            response = requests.post(api_url, json = data)
            get_data = json.loads(response.text)
            if response.status_code == 200 :
                home_screen = MyApp.get_running_app().root.get_screen("home")
                token = eval(get_data['data']['object']).get('Access_Token', None)
                home_screen.ids.token_field.text = token
                home_screen.ids.token_field.opacity = 0
                home_screen.ids.welcome_label.text = get_data['data']['message']
                MyApp.get_running_app().root.current = "home"
                
        except Exception as e:
            print("Generated exception is:",str(e))
            self.ids.error_label.text = "Error in Logging user"



class HomeScreen(Screen):
    def signout(self):
        token_value = self.ids.token_field.text
        print(token_value)
        api_url="http://localhost:8000/signout/"
        headers={'Authorization': f'JWT {token_value}',"Content-type":'application/json'}
        try:
            response = requests.post(api_url,headers=headers)
            print(response.status_code)
            if response.status_code == 204:
                self.manager.current = 'login'
        except Exception as e:
            print(f"generated Exception is {str(e)}")

class MyApp(MDApp):    
    def build(self):
        #Loading kivy files
        Builder.load_file('login.kv')
        Builder.load_file('home.kv')
        Builder.load_file('signup.kv')

        #creating a screens
        signup_screen = SignupScreen(name='signup')
        login_screen = LoginScreen(name='login')
        home_screen = HomeScreen(name='home')
        
        #Screen manager actions
        screen_manager = ScreenManager()
        screen_manager.add_widget(signup_screen)
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(home_screen)
        
        screen_manager.current = "signup"
        return screen_manager
    

if __name__ == "__main__":
    MyApp().run()
