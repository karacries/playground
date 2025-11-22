'''
Password Guessing T1110.001
Cross-Platform script to brute force a password
educational purposes only; not perfect code
'''
import time # add a small delay
import tkinter as tk
from tkinter import messagebox
# generative AI
import google.generativeai as genai

def load_api_key():
    try:
        with open("GEMINI_API_KEY.txt", "r") as key:
            return key.read().strip()
    except FileNotFoundError:
        print("Gemini API key not found. Please create it and try again.")
        return None

# gemini API integration
api_key = load_api_key()

# Configure the client globally; all subsequent calls use this key by default.
if api_key:
    genai.configure(api_key=api_key)
    print("Gemini API key loaded.")
else:
    print("Error loading Gemini API key.")

# set the persona
sys_instruction = (
    ''' 
    You are an expert Cybersecurity Risk Analyst for a corporate IT department tasked with teaching a younger audience.
    Your job is to interpret these Mitre attack simulations for non-technical users.
    Be concise and explain in 2 sentences the results at a 10th grade reading level.
    '''
)

# Choose a model. 'gemini-2.0-flash' is fast and affordable; 'gemini-2.0-pro' is stronger.
model_name = "gemini-2.0-flash"  # change to 'gemini-2.0-pro' for higher quality

# Create a GenerativeModel instance for repeated calls.
if api_key:
    model = genai.GenerativeModel(model_name,generation_config={"temperature": 0.3,"top_p": 0.85, "top_k": 40,"max_output_tokens": 150})

def ai_explanation(finding_type, details): # configuring the model to ask the same thing each time
    if not api_key:
        print("Explanation unavailable. Gemini API key not found.")
        return None
    try:
        prompt = f'''
        The user ran a security tool and found: {finding_type}. The specific details are: {details}. Explain the risk.
        '''
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Something happened: {e}")

# let's create a "login"!
def totally_secure_login(username_attempt, password_attempt):
    # making a simple login system that's totally secure!
    actual_username = "admin"
    actual_password = "qwerty"

    if (username_attempt == actual_username and password_attempt == actual_password):
        return True # we're in
    else:
        return False # it's so over

def gui():
    # creating the simulated "login" box
    root = tk.Tk()
    root.title("Super Important and Secret Login Portal")
    root.geometry("600x400")

    # header
    tk.Label(root, text="Please enter your username and password.", font=("Arial", 14, "bold")).pack(pady=10)

    # username field
    tk.Label(root, text="Username:").pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    # password field
    tk.Label(root, text="Password:").pack()
    password_entry = (tk.Entry(root, show="*"))
    password_entry.pack(pady=5)

    # results
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack()

    def check_credentials():
        # .get() will collect the text that is inside of the input boxes
        user_text = username_entry.get()
        pass_text = password_entry.get()

        result = totally_secure_login(user_text,pass_text)  # give the entered details to the method that's storing the correct credentials

        if result:
            result_label.config(text="ACCESS GRANTED", fg="green")
            messagebox.showinfo("Success", "You have successfully logged in!")
        else:
            result_label.config(text="ACCESS DENIED", fg="red")

    # login button
    login = tk.Button(root, text="Login",
                          command=check_credentials)  # check_credentials will run that function when clicked
    login.pack(pady=20)

    # start the window
    root.mainloop()

# now we will attack this because we don't know the password
def attacker():
    target_username = "admin" # let's assume that we have access to the username!

    password_list = [ # im picking the top 10 names i see in a "10k-most-common.txt" passwords list as a sample
        "password",
        "123456",
        "12345678",
        "1234",
        "qwerty",
        "baseball",
        "football",
        "letmein",
        "monkey",
        "mustang"
    ]
    print(f"{target_username}'s password is sure to be something from {password_list}!")
    print("------------------------------------")

    start_time = time.time() # start the timer

    for password_guess in password_list: # targeting the user
        print(f"I'm attempting {password_guess}...")

        login_success = totally_secure_login(target_username, password_guess)

        if login_success: # if the password is guessed
            end_time = time.time() # end it
            total_time = end_time - start_time # find the total time elapsed


            print("------------------------------------")
            print(f"{target_username}'s password is: {password_guess}")
            print(f"I found it in {total_time:.2f} seconds.")

            print("\nGemini 2.0 Explanation:") # ai explanation
            explanation = ai_explanation(finding_type="Brute Force Password Attack (T1110.001)",
            details=f"the attacker guessed password '{password_guess}' for user '{target_username}' in just {total_time:.2f} seconds using a common wordlist.")
            print(explanation)
            return # end the attempt

        time.sleep(0.1) # allows us to read the output

    # if the loop finishes and the password wasn't correct:
    end_time = time.time() # end it
    total_time = end_time - start_time # find the total time elapsed

    print("------------------------------------")
    print(f"I couldn't guess the password!")
    print(f"You have a unique password!")
    print(f"I was looking for {total_time:.2f} seconds.")


def output():
    while True:
        print("------------------------------------")
        print("Password Guessing T1110.001 - I will find your password!")
        print("------------------------------------")
        print("1. Login page")
        print("2. Brute forcing tool")
        print("3. Exit")

        choice = input("Please make a selection: ")

        if choice == "1":
            gui()
        elif choice == "2":
            attacker()
        elif choice == "3":
            break
        else:
            print("Please make a valid selection.")



def main():
    output()

if __name__ == "__main__": # let's run it!
    main()
