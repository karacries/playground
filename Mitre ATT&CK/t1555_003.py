'''
Credentials from Web Browsers T1555.003
Cross-Platform script to view usernames and passwords saved by browsers (just looking for if it's there here)
educational purposes only; not perfect code
'''
import os # for user info
import sys # OS
from pathlib import Path # file paths
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

def browser_credentials():
    # check for chrome/firefox credentials

    # what os is the user on?
    home_dir = Path.home()

    # now, we will check the default paths for chrome/firefox; unsure how we can se
    check_paths = {
        "Google Chrome (Windows)": home_dir / "AppData/Local/Google/Chrome/User Data/Default/Login Data",
        "Google Chrome (macOS)": home_dir / "Library/Application Support/Google/Chrome/Default/Login Data",
        "Google Chrome (Linux)": home_dir / ".config/google-chrome/Default/Login Data",
        "Firefox (Windows)": home_dir / "AppData/Roaming/Mozilla/Firefox/Profiles/",
        "Firefox (macOS)": home_dir / "Library/Application Support/Firefox/Profiles/",
        "Firefox (Linux)": home_dir / ".mozilla/firefox/",
        "Zen (Windows)": home_dir / "AppData/Roaming/Mozilla/Zen/Profiles/",
        "Zen (macOS)": home_dir / "Library/Application Support/zen/Profiles/",
        "Zen (Linux)": home_dir / ".mozilla/zen/", # can zen even be on linux? i didn't do a search
        # i would also include brave, but i have uninstalled it so therefore idc
    }

    found_count = 0 # set a counter

    for browser, path in check_paths.items():

        # firefox has a randomly named profile folder according to google, but let's just see if it exists
        if "Firefox" or "Zen" in browser:
            if path.exists() and path.is_dir(): # if it exists!
                print(f"Your Firefox profile is located at {path}")
                found_count += 1 # increase counter
        else: # for chrome
            if path.exists() and path.is_file():
                print(f"Your Chrome profile is located at {path}")
                found_count += 1 # increase counter

    print("------------------------------------")
    if found_count > 0:
        print(f"I found {found_count} potential credential location(s)!")
        print("\nGemini 2.0 Explanation:")
        explanation = ai_explanation(finding_type="Credentials from Web Browsers (T1555.003)",
        details=f"the attacker found these credential files at: {path}")
        print(explanation)
    else:
        print(f"I couldn't find any credential files. Are the browsers installed in a different directory?")

def output():
    print("------------------------------------")
    print("Credentials from Web Browsers T1555.003 - I will find your credentials!")
    browser_credentials()

def main():
    output()

if __name__ == "__main__": # let's run it!
    main()
