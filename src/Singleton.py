""" Singleton

    We want most classes in this program to only have one instance, so we'll 
    force all of them to be singletons
"""

class Singleton(object):
    """ Singleton base
        
        We only want one of each object for the whole code, so we'll force it
        as a singleton
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance