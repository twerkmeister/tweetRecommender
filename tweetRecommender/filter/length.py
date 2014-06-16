def filter(webpage):
    return {'$where': 'this.terms.length > 3'}
