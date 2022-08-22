"""
    useful functions
"""

def is_empty(data):
    # check if variable is empty
    if data == '' \
    or data == 'null' \
    or data == 'undefined' \
    or data == None:
        
        return True
    else:
        return False
    
def validate_phonenumber(number):
    # Shaping and validating phone number
    phonenumber = str(number)
    for i in range(0,3):
        if phonenumber.startswith("0"):
            phonenumber = phonenumber[1:]

        if phonenumber.startswith("+"):
            phonenumber = phonenumber[1:]

        if phonenumber.startswith("98"):
            phonenumber = phonenumber[2:]

    if len(phonenumber) != 10:
        return ('err')

    if not phonenumber.isdigit():
        return ('err')
    
    return int(phonenumber)