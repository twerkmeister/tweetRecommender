DISPLAY_NAME = "Tweet length"

def filter(webpage):
    return {'$where': 'this.terms.length > 3'}
