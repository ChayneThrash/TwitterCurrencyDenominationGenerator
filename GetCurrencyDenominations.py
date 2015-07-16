__author__ = 'Chayne'


# Generates the number of denominations in the value given. It also returns the value passed in after removing
# all of the denominations. ie: updated_val // denomination will be equal.
def generateDenominations(denomination, update_value):
    num_denominations = update_value // denomination
    update_value -= num_denominations * denomination
    return num_denominations, update_value

# Class responsible for formatting string specifically for currency denominations.
class OutputFormatter:
    def __init__(self):
        self.beginning_of_output = True
        self.formattedOutput = ''

    # This function adds the string and value to the output. Can be chained
    # so that multiple calls on separate lines are not necessary.
    def addToOutput(self, value_string, value):
        if value != 0:
            if not self.beginning_of_output:
                self.formattedOutput += ', '
            else:
                self.beginning_of_output = False
            self.formattedOutput += value_string + str(value)
        return self

    def getFormattedOutput(self):
        return self.formattedOutput


# Class responsible for generating currency denominations. Also contains a formatted string for representing the
# currency denominations.
class CurrencyDenominationGenerator:
    def __init__(self, dollars, cents):
        self.__generateDenominations(dollars, cents)
        self.__formatCurrencyDenominations()

    def __generateDenominations(self, dollars, cents):
        self.num_of_hundreds, updated_dollars = generateDenominations(100, dollars)
        self.num_of_twenties, updated_dollars = generateDenominations(20, updated_dollars)
        self.num_of_tens, updated_dollars = generateDenominations(10, updated_dollars)
        self.num_of_fives, updated_dollars = generateDenominations(5, updated_dollars)
        self.num_of_ones = updated_dollars

        self.num_of_quarters, updated_cents = generateDenominations(25, cents)
        self.num_of_dimes, updated_cents = generateDenominations(10, updated_cents)
        self.num_of_nickels, updated_cents = generateDenominations(5, updated_cents)
        self.num_of_pennies = updated_cents

    def __formatCurrencyDenominations(self):
        formatter = OutputFormatter()

        formatter.addToOutput("100's: ", self.num_of_hundreds).addToOutput("20's: ", self.num_of_twenties) \
            .addToOutput("10's: ", self.num_of_tens).addToOutput("5's: ", self.num_of_fives) \
            .addToOutput("1's: ", self.num_of_ones)

        formatter.addToOutput("Q's: ", self.num_of_quarters).addToOutput("D's: ", self.num_of_dimes) \
            .addToOutput("N's: ", self.num_of_nickels).addToOutput("P's: ", self.num_of_pennies)
        self.formatted_currency_denominations = formatter.getFormattedOutput()

    def __str__(self):
        return self.formatted_currency_denominations


def generateCurrencyDenominationsString(currency):
    if currency[0] != '$':
        return "Currency must begin with a dollar sign"

    currency = currency[1:]  # Strip off the dollar sign.
    currency = currency.split('.')

    if len(currency) > 2:
        return "Invalid number of decimals"

    try:
        dollars = int(currency[0])
        cents = int(currency[1])
    except:
        return "Invalid character detected."

    denominations = CurrencyDenominationGenerator(dollars, cents)

    return str(denominations)


if __name__ == '__main__':
    user_currency = raw_input('Enter a currency amount: ')
    print generateCurrencyDenominationsString(user_currency)
