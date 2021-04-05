def factors(number):
    """Returns the factors of number as a list"""
    fact=[]

    for i in range(1, number+1):

        if number%i==0:
            fact+=[i]
            
    return fact

def checkIfPrime(number):
    """Returns True if number is prime"""
    isPrime=False
    f=[]

    if number==1:
        isPrime=False

    else:

        for j in range(1,number+1):

            if number%j==0:
                f+=[j]

            if len(f)<=2:
                isPrime=True

            else:
                isPrime=False

    return isPrime

def primeNumbers(upperLimit, lowerLimit=1):
    """Returns the prime numbers betwerrn upperLimit and lowerLimit"""

    if lowerLimit==1:
        primeNums=[2]
        a=2
        prime=None

        for b in range(upperLimit-1):

            for c in primeNums:

                if a%c==0:
                    prime=False
                    break

                else:
                    prime=True

            if prime==True:
                primeNums+=[a]

            a+=1

    else:
        f=[]
        primeNums=[]

        for i in range(lowerLimit+1,upperLimit+1):	

            for j in range(1,i+1):

                if i%j==0:
                    f+=[j]

            if len(f)<=2:
                    primeNums+=[i]
                    
            f=[]

    return primeNums

def primeFactors(number):
    """Returns the prime factors of number as a list"""
    pf=[]
    pn=primeNumbers(number, 1)

    while number > 1:
       
        for b in pn:

            while number%b==0:
                pf.append(b)
                number=int(number/b)
            
        number-=1

    return pf

def lcm(numbers):
    """Returns the least common multiple of numbers. (Must be <class 'list'>)"""
    
    if str(type(numbers))=="<class 'list'>":
        numbers.sort()
        pn=primeNumbers(numbers[-1])
        all_pf=[]
        occur={}
        answer=1

        for e in pn:
            occur[e]=0

        for a in numbers:
            all_pf.append(primeFactors(a))
    

        for b in all_pf:

            for c in pn:
        
                if b.count(c)>occur[c]:
                    occur[c]=b.count(c)

        for d in occur:
            answer*=d**occur[d]

        return answer

    else:
        print("Error: function 'lcm' is not defined for",type(numbers))
