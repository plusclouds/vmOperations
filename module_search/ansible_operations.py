import os



def execute_playbook_script(directory: str):
    print("executing Playbook in dir: ", directory)

    print(os.system("ansible-playbook "+directory))

    print("Execution complete!")



