__author__ = 'Chayne'


def generateCurrencyDenominationsString(currencyMessage):
    if currencyMessage[0] != '$':
        return "Currency must begin with a dollar sign"

    currency = currencyMessage[1:]
    currencySplit = currency.split('.')

    if (len(currencySplit) > 2):
        return "Invalid number of decimals"

    try:
        dollars = int(currencySplit[0])
        cents = int(currencySplit[1])
    except:
        return "Invalid character detected."

    print(dollars)
    print(cents)

    num_of_hundreds = dollars//100
    dollars -= num_of_hundreds*100
    num_of_twenties = dollars//20
    dollars -= num_of_twenties*20
    num_of_tens = dollars//10
    dollars -= num_of_tens*10
    num_of_fives = dollars//5
    num_of_ones = dollars - num_of_fives*5

    num_of_quarters = cents//25
    cents -= num_of_quarters*25
    num_of_dimes = cents//10
    cents -= num_of_dimes*10
    num_of_nickels = cents//5
    num_of_pennies = cents - num_of_nickels*5

    formatted_output = "100's: " + str(num_of_hundreds) + ", 20's: " + str(num_of_twenties) + ", 10's: " + str(num_of_tens) + ", 5's: " + str(num_of_fives) + ", 1's: " + str(num_of_ones)
    formatted_output += ", Q: " + str(num_of_quarters) + ", D: " + str(num_of_dimes) + ", N: " + str(num_of_nickels) + ", P: " + str(num_of_pennies)

    return formatted_output
