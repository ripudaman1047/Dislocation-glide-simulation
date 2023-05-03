
def get_int(mainprompt, errorprompt, Min=None, Max=None):
    """
    This functions takes a integer value within bounds of (Min, Max) exclusive
    
    Parameters
    ----------
    mainprompt : string for demanding an integer input from the user
    
    errorprompt : string for a invalid value input by the user 
                  i.e. when the value is out of range     
    Min : TYPE, int
        Minimum integer value or lower bound. The default is None.
    Max : TYPE, int
        Maximum integer value or upper bound. The default is None.

    Returns
    -------
    var : TYPE, int
        user input integer value within bounds.

    """
    while True:
        try:
            var = int(input(mainprompt))
            if Min!=None and Max!=None and var<Max and var>Min: 
                return var
            elif Min!=None and Max==None and var>Min:
                return var
            elif Min==None and Max!=None and var<Max:
                return var
            else:
                print(errorprompt)
        except ValueError:
            print(errorprompt)
            

def get_float(mainprompt, errorprompt, Min=None, Max=None):
    """
    This functions takes a float value within bounds of (Min, Max) exclusive
    
    Parameters
    ----------
    mainprompt : string for demanding an float input from the user
    
    errorprompt : string for a invalid value input by the user 
                  i.e. when the value is out of range     
    Min : TYPE, float or int
        Minimum value or lower bound. The default is None.
    Max : TYPE, float or int
        Maximum value or upper bound. The default is None.

    Returns
    -------
    var : TYPE, float
        user input float value within bounds.

    """
    while True:
        try:
            var = float(input(mainprompt))
            if Min!=None and Max!=None and var<Max and var>Min: 
                return var
            elif Min!=None and Max==None and var>Min:
                return var
            elif Min==None and Max!=None and var<Max:
                return var
            else:
                print(errorprompt)
        except ValueError:
            print(errorprompt)
 
