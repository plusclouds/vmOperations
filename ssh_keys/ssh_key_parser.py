def ssh_key_input(type: str, public_key: str, email: str):
    file_object = open('.ssh/authorized_keys', 'a')
    file_object.write(type + " " + public_key + " " + email)
    file_object.write('\n')
    file_object.close()
