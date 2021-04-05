def sonOfABitch(n): 
    isp=False
  
    if (n > 2):
        isp=True 
    if (n > 3):  
        isp=True


    if ((n % 12 == 1 or n % 12 == 5)): 
        isp= True
    if (n % 12 == 7): 
        isp= True
    if  ( n % 12 == 11): 
        isp= True

    return isp