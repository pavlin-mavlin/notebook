from controllers.nodecontroller import NodeController

def make_password_placeholder(password):
    placeholder=""
    if password:
        for x in range(1, len(password)):
            placeholder=placeholder+"•"
            
    return placeholder
