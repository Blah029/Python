def factors(number):
    """Return the factors of number as a list"""
    fact = []
    for i in range(1, number+1):
        if number % i == 0:
            fact += [i]
            
    return fact


def check_if_prime(number):
    """Return True if number is prime"""
    is_prime = False
    f = []
    if number == 1:
        is_prime = False
    else:
        for j in range(1,number+1):
            if number % j == 0:
                f += [j]
            if len(f) <= 2:
                is_prime = True
            else:
                is_prime = False

    return is_prime


def prime_numbers(limit_upper, limit_lower=1):
    """Return the prime numbers betwerrn limit_upper and limit_lower"""
    if limit_lower == 1:
        primenums = [2]
        a = 2
        prime = None
        for b in range(limit_upper-1):
            for c in primenums:
                if a % c == 0:
                    prime=False
                    break
                else:
                    prime=True
            if prime == True:
                primenums += [a]
            a+=1
    else:
        f =[]
        primenums = []
        for i in range(limit_lower+1,limit_upper+1):	
            for j in range(1,i+1):
                if i % j == 0:
                    f += [j]
            if len(f) <= 2:
                    primenums += [i]
            f=[]

    return primenums


def prime_factors(number):
    """Return the prime factors of number as a list"""
    pf=[]
    pn=prime_numbers(number, 1)
    while number > 1:
        for b in pn:
            while number % b == 0:
                pf.append(b)
                number = int(number/b)
        number -= 1

    return pf


def lcm(numbers):
    """Return the least common multiple of numbers. (Must be <class 'list'>)"""
    if str(type(numbers)) == "<class 'list'>":
        numbers.sort()
        pn = prime_numbers(numbers[-1])
        all_pf = []
        occur = {}
        answer = 1
        for e in pn:
            occur[e] = 0
        for a in numbers:
            all_pf.append(prime_factors(a))
        for b in all_pf:
            for c in pn:
                if b.count(c) > occur[c]:
                    occur[c] = b.count(c)
        for d in occur:
            answer = d**occur[d]

        return answer

    else:
        print("Error: function 'lcm' is not defined for",type(numbers))
