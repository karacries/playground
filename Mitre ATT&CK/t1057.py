'''
Process Discovery T1057
Cross-Platform script to find a list of processes & scan the output for applications
educational purposes only; not perfect code
'''
import subprocess # run external commands
import sys # check the OS
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

def find_target_processes(target_list):
    # runs a system command to get all running processes and checks if any processes from the list are found

    run_command = [] # will eventually run the command

    # check the OS to pick the command
    if sys.platform == 'win32':
        run_command = ["tasklist"] # windows command for powershell, according to mitre
    elif sys.platform == 'darwin' or sys.platform == 'linux': # unix-based systems; linx & macos
        run_command = ["ps", "-ef"] # unix-based system command for terminal
    else:
        print(f"What is {sys.platform}?")
        return
    print(f"{sys.platform} detected! I'll try to run {' '.join(run_command)}!")
    print("------------------------------------")

    # now execute the command and see what it outputs
    try:
        result = subprocess.run(run_command, capture_output=True, text=True, check=True) # (run the command, store the output as stdout, decode the output as text, show an error if the command doesn't work)

        process_output = result.stdout # get the text from the command

        output = []

        # now we look at the output line by line
        for target in target_list:
            if target.lower() in process_output.lower(): # .lower() to make the search case-insensitive
                print(f"PROCESS FOUND: {target}")
                output.append(target)

        if len(output) > 0: # run the AI explanation!
            print("\nGemini 2.0 Explanation:")
            details_string = ", ".join(output)
            explanation = ai_explanation(finding_type="Publically Visible Processes (T1057)",
            details=f"the attacker found these applications running: {details_string}")
            print(explanation)

    except subprocess.CalledProcessError as e:
        print(f"Error with command: {e}")
        print(f"STDERR: {e.stderr}")
    except Exception as e:
        print(f"Something happened here... {e}")

def targets():
    targets_to_find = [ # find them (hopefully)
        "chrome.exe", # google chrome; windows
        "firefox", # firefox
        "chrome", # chrome
        "safari", # safari
        "powershell.exe", # powershell
        "sshd", # secure shell server
        "notepad.exe", # notepad
        "textedit",
        "terminal",
        "pycharm", # im using this right now!
        "spotify", # also using this rn
        "obsidian", # my notetaking app
        "discord", # chatting
        "steam", # video game
        "zoom", # zoom
        "anki" # anki flashcards

    ]
    return targets_to_find # send it back

def output_target():
    targets_process = targets()
    print("------------------------------------")
    print("Process Discovery T1057 - I can see your processes!")
    find_target_processes(targets_process)

    print("------------------------------------")

def main(): # main function
    output_target()

if __name__ == "__main__": # let's run it!
    main()
