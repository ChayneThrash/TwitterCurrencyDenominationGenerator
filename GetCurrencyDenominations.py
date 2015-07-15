__author__ = 'Chayne'


def generateDenominations(denomination, update_value):
    num_denominations = update_value // denomination
    update_value -= num_denominations * denomination
    return (num_denominations, update_value)


class OutputFormatter:
    def __init__(self):
        self.beginning_of_output = True

    def getFormattedOutput(self, value_string, value):
        formatted_output = ''
        if value != 0:
            if not self.beginning_of_output:
                formatted_output += ', '
            else:
                self.beginning_of_output = False
            return formatted_output + value_string + str(value)
        return ''


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

    num_of_hundreds, updated_dollars = generateDenominations(100, dollars)
    num_of_twenties, updated_dollars = generateDenominations(20, updated_dollars)
    num_of_tens, updated_dollars = generateDenominations(10, updated_dollars)
    num_of_fives, updated_dollars = generateDenominations(5, updated_dollars)
    num_of_ones = updated_dollars

    num_of_quarters, updated_cents = generateDenominations(25, cents)
    num_of_dimes, updated_cents = generateDenominations(10, updated_cents)
    num_of_nickels, updated_cents = generateDenominations(5, updated_cents)
    num_of_pennies = updated_cents

    formatter = OutputFormatter()

    formatted_output = formatter.getFormattedOutput("100's: ", num_of_hundreds)
    formatted_output += formatter.getFormattedOutput("20's: ", num_of_twenties)
    formatted_output += formatter.getFormattedOutput("10's: ", num_of_tens)
    formatted_output += formatter.getFormattedOutput("5's: ", num_of_fives)
    formatted_output += formatter.getFormattedOutput("1's: ", num_of_ones)

    formatted_output += formatter.getFormattedOutput("Q's: ", num_of_quarters)
    formatted_output += formatter.getFormattedOutput("D's: ", num_of_dimes)
    formatted_output += formatter.getFormattedOutput("N's: ", num_of_nickels)
    formatted_output += formatter.getFormattedOutput("P's: ", num_of_pennies)

    return formatted_output


if __name__ == '__main__':
    user_currency = raw_input('Enter a currency amount: ')
    print generateCurrencyDenominationsString(user_currency)
