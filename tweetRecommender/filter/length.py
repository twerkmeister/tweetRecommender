def filter():
    return {'$where': 'this.terms.length > 3'}