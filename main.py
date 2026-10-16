import math
class Category:
    def __init__(self, name):
       self.name = name
       self.ledger = []

    def deposit(self, amount, description=''):
       self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
       if self.check_funds(amount):
          self.ledger.append({'amount': -amount, 'description': description})
          return True
       else:
          return False

    def get_balance(self):
       get_balance = 0
       for item in self.ledger:
          get_balance += item['amount']
       return get_balance

    def check_funds(self, amount):
       if amount > self.get_balance():
          return False
       else:
          return True

    def transfer(self, amount, category):
       if self.withdraw(amount, f'Transfer to {category.name}'):
          category.deposit(amount, f'Transfer from {self.name}')
          return True
       else:
          return False

    def __str__(self):
       title = self.name.center(30, '*')
       item_list = []
       for item in self.ledger:
          item_list.append(item['description'][:23].ljust(23) + f"{item['amount']:.2f}".rjust(7))
       ledger_lines = '\n'.join(item_list)
       total_line = f'Total: {self.get_balance()}'
       return title + f'\n{ledger_lines}' + f'\n{total_line}'

def get_withdrawn_percentage(category, total_withdrawn):
    category_total = 0
    for item in category.ledger:
       if item['amount'] < 0:
          category_total += abs(item['amount'])

    percentage = category_total / total_withdrawn * 100
    first = percentage / 10
    second = math.floor(first)
    third = second * 10
    return third

def create_spend_chart(categories):
    total_withdrawn = 0
    for category in categories:
       for item in category.ledger:
          if item['amount'] < 0:
             total_withdrawn += abs(item['amount'])
    percentages = [get_withdrawn_percentage(category, total_withdrawn) for category in categories]

    title = 'Percentage spent by category\n'

    rows = []
    for height in range(100, -1, -10):
       row = f'{height}'.rjust(3) + '| '
       for percentage in percentages:
          if percentage >= height:
             row += 'o  '
          else:
             row += '   '
       rows.append(row)
    chart = '\n'.join(rows)
    horizontal_line = "    " + ("-" * (3 * len(categories) + 1))

    length_of_names = [len(cat_names.name) for cat_names in categories]
    max_length_of_names = max(length_of_names)

    label_rows = []
    for position in range(max_length_of_names):
        row = '     '
        for category in categories:
            if position < len(category.name):
                row += category.name[position] + '  '
            else:
                row += ' ' + '  '
        label_rows.append(row)
    labels = '\n'.join(label_rows)

    return title + chart + '\n' + horizontal_line + '\n' + labels

food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)

categories = [food, clothing]
print(create_spend_chart(categories))
