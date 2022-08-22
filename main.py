import time
import textwrap
import configparser
import random
import sys

#https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
PURPLE = '\33[35m'
GREY = '\033[90m'
RED = '\33[31m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[36m'
BOLD = '\033[1m'
ITALICS = '\033[3m'
UNDERLINE = '\033[4m'
END = '\033[0m'
CHEATS = ['#health', '#inv', '#reset', '#money', '#back', '#to', '#give', '#list', '#cheats']

INVDICT = {'sword': ['A sharp weapon that will give you an edge in battle', 15], 
    'lantern': ['A helpful tool that can guide you in the dark', 25], 
    'rope': ["A mountain climber's best friend", 10],
    'backpack': ['Can hold all your stuff', 15],
    'bread': ['This food will keep you alive, all while being delicous', 5],
    'jacket': ['Like it or not, this is essential to surviving the mountain', 25],
    'compass': ['No matter where you are; a desert, and glacier, this tool will help you find your way', 10],
    'rope_of_clenching': ['A gift from the kind old man. this rope magically grabs targets you set', 0],
    'strange_egg': ["A very strange egg found in a mysteriously glowing tree. You've never seen anything like it", 0],
    'magic_die': ["It looks like a normal die, but on use, it tends to be abnormally lucky...", 45],
    'shawl': ["Not kingly wear, but better than nothing when scaling a mountain", 18],
    'snow_boots': ['Without these, your feet would quickly freeze off', 30],
    'extra_rations': ['Extra food to carry just in case you run out...', 10],
    'magic_herb': ['Bought from a shady woman hiding in some bushes, these herbs are supposedly magical', 10],
    'helpful_note': ['This note only says one thing on it: "Left is right!"'],
    'bow': ['A useful weapon, but not all that powerful.', 15],
    'arrow': ['Ammo for a bow.', 5],
    'prophecy': ['A hero with a magic rope, The one that will read this note, They are our only hope.', 20],
    'grapple': ['Useful when climbing, or grabbing.'],
    'parachute': ['Extremely useful in dire circumstances']}
    

class Player:

    default_inventory = {'backpack'}
    default_health = 10
    default_money = 40
    
    def __init__(self, inventory=None, health=None, money=None):
        self.inventory = inventory or self.default_inventory.copy()
        self.health = health or self.default_health
        self.money = money or self.default_money

    def hurt(self, amount):
        self.health -= amount
        print(f'{RED}You lost {amount} health!{END}')

    def heal(self, amount):
        self.health += amount
        if self.health < 10 or self.health > 10000:
            print(f'{GREEN}You gained {amount} health{END}')
        else:
            self.health = 10
            print(f'{GREEN}You are already at full health{END}')
            
    def pay(self, item):
        if item in INVDICT:
            amount = INVDICT[item][1]
        else:
            amount = int(item)
        if self.money - amount < 0: 
            print('You cannot pay for that!')
        elif item in self.inventory:
            print(f"you already have a(n) {item.replace('_', ' ')}")
        else:
            self.money -= amount
            if item in INVDICT:
                print(f"{GREEN}You payed for a(n) {item.replace('_', ' ')} and lost ${amount}!{END}")
                self.inventory.add(item)
            else:
                print(f'{GREEN}You payed ${item}{END}')

    def change_wallet(self, amount):
        amount = str(amount)
        if amount == 'all_money':
            print(f'{RED}You lost all your money{END}')
            self.money = 0
        elif amount.startswith('-%') or amount.startswith('%'):
            percentage = amount.split('%')[1]
            percentage = int((you.money / 100) * float(percentage))
            if amount.startswith('-'):
                you.change_wallet(f'-{percentage}')
            else:
                you.change_wallet(percentage)
        elif amount.isdigit() == True or str((int(amount) * -1)).isdigit() == True:
            amount = int(amount)
            self.money += amount
            if amount >= 0:
                print(f'{BLUE}You gained ${amount}{END}')
            else:
                print(f'{BLUE}you lost ${amount * -1}{END}')
            if self.money < 0:
                self.money = 0

    def gain_item(self, items):
        for item in items:
            if item in self.inventory:
                print(f"you already have a(n) {item.replace('_', ' ')}")
            elif item.isdigit() == True:
                you.change_wallet(item)
            else:
                print(f"{GREEN}You gained a(n) {item.replace('_', ' ')}!{END}")
                self.inventory.add(item)

    def remove_item(self, items):
        for item in items:
            print(f"{GREEN}You gained a(n) {item.replace('_', ' ')}!{END}")
            self.inventory.remove(item)
    

    def show_inventory(self):
        print(f'\nhealth: {self.health}'.center(8), 
              'INVENTORY'.center(44), 
              f'money: ${self.money}')
        maxlen = max([len(item) for item in self.inventory])
        colors = {BLUE, CYAN}
        color = BLUE
        for item in self.inventory:
            label = item.replace('_', ' ')
            description_lines = textwrap.fill(INVDICT[item][0], 70 - maxlen).splitlines()
            print(f"{label:>{maxlen}} | {color}{description_lines[0]}{END}")
            for line in description_lines[1:]:
                print(f"{' ':>{maxlen}} | {color}{line}{END}")
            color = (colors - set([color])).pop()
        print()

    def cheat(self, code):
        if code == '#health':
            you.health = sys.maxsize
        if code == '#inv':
            for item in INVDICT:
                you.gain_item([item])
        if code == '#reset':
            self.inventory = self.default_inventory.copy()
            self.health = self.default_health
            self.money = self.default_money
            return past_sections[0]
        if code == '#money':
            self.money = sys.maxsize
        if code.startswith('#give'):
            try:
                __, item = code.split()
            except ValueError:
                print(f'{RED}There is no such item{END}')
                return
            if item in INVDICT:
                you.gain_item([item])
            else:
                print(f'{RED}There is no such item{END}')
        if code == '#back':
            print()
            for (n, item) in enumerate(past_sections, 1):
                print(f'{n} {BLUE}{item}{END}')
            while True:
                choice = input(f'choose an option: {PURPLE}')
                while choice.isdigit() == True and int(choice) < len(past_sections) + 1 and int(choice) != 0:
                    print(END, end='')
                    return past_sections[int(choice) - 1]
        if code.startswith('#to'):
            try:
                __, section = code.split()
            except ValueError:
                print(f'{RED}There is no such section{END}')
                return
            if section in parser.sections():
                return section
            else:
                print(f'{RED}There is no such section{END}')
        you.show_inventory()
        if code == '#list':
            l = parser.sections()
            for (n, section) in enumerate(l):
                if n%2 == 0:
                    l[n] = f'{GREEN}{l[n]}{END}'
                else:
                    l[n] = f'{BLUE}{l[n]}{END}'
                print(l[n])
        if code == '#cheats':
            print('CHEATS'.center(60))
            print(f'{BLUE}#health{END} [Gives a large amount of health]')
            print(f'{BLUE}#inv{END} [Gives every inventory item]')
            print(f'{BLUE}#reset{END} [Resets your inventory and the game]')
            print(f'{BLUE}#money{END} [Gives a large amount of money]')
            print(f'{BLUE}#back{END} [Lists sections you have been in]')
            print(f'{BLUE}#to <section_name>{END} [Goes to specified section]')
            print(f'{BLUE}#give <item>{END} [Gives a specified item]')
            print(f'{BLUE}#list{END} [Lists all sections]')
            print('- - -'.center(60))


def ask(options, requirements, check_money, you):
    choices = {}
    labels = []
    for i, (option, label) in enumerate(options.values(), 1):
        choices[str(i)] = option
        if option in requirements:
            required = ' {}[{} {} required]{}'.format(
                PURPLE, ' and '.join(requirements[option]).replace('_', ' '), 
                'is' if len(requirements[option]) == 1 else 'are', END)       
        else:
            required = ''
        if option in check_money:
            afford = ' {}[${} is needed]{}'.format(PURPLE, check_money[option], END)
        else:
            afford = ''
        labels.append((str(i), f'{BLUE}{label}{END}{required}{afford}'))

    if len(choices) == 1:
        choices[''] = choices['1']
    
    for item, label in labels:
        print(item, label)

    t = 0
    while True:
        t += 1
        response = input(f'choose an option: {PURPLE}')
        print(END, end='')
        if response in choices:
            return choices[response]
        elif response != '' and response.split()[0] in CHEATS:
            s = you.cheat(response)
            if s is None:
                return section
            return s
        elif response in {'i', 'inv', 'inventory'}:
            you.show_inventory()
        if t == 10:
            return section

def format(text, format):
    return text.format(**globals())

def find(option):
    items = dict()
    for section in parser.sections():
        if parser.has_option(section, option) == True:
            items[section] = parser.get(section, option).split()
    return items

def perception(finds, blanks=3):
    if finds:
        return random.choice(list(finds) + [None] * (blanks * len(finds)))

def gamble(you, start=5, multiplier=3):
    start = int(start)
    multiplier = int(multiplier)
    print(f'You put ${start} in.')
    n = []
    c = []
    for i in range(multiplier):
        c.append(20)
        for a in range(multiplier - i + 3):
            c.append(6)
            for b in range(multiplier - a + 5):
                c.append(5)
                for d in range(multiplier - b + 8):
                    c.append(4)
                    for e in range(multiplier - d + 10):
                        c.append(2)
                        for f in range(multiplier - e):
                            c.append(0)
    for i in range(10):
        n.append(random.choice(c))
    earn = random.randint(1, multiplier) * random.choice(n) + random.choice([0, 0, 0, 1, 1, 1, start]) - start
    if earn <= 0:
        print("You didn't win any profit!")
        you.change_wallet((start * -1))
    else:
        you.change_wallet(earn)
    
#### GAME ####

parser = configparser.ConfigParser()
parser.read('text.ini')
you = Player()

#makes dicts of important modifiers
requirements = find('__required')
for key in requirements.keys():
    requirements[key] = set(requirements[key])
heal, hurt = find('__heal'), find('__hurt')
pay_dict = find('__pay')
change_wallet = find('__change_wallet')
perceptiondict = find('__perception')
for key in perceptiondict.keys():
    perceptiondict[key] = set(perceptiondict[key])
gain_item_dict = find('__gain_item')
death_message = find('__death')
check_money = find('__afford')
gamble_dict = find('__gamble')
remove_item_dict = find('__remove_item')
quit = find('__quit')
for key in check_money:
    check_money[key] = int(check_money[key][0])
starting_section = 'START'
section = starting_section
previous_section = section
past_sections = []

while True:
    options = {}
    option_section = []

    if section in requirements and not (you.inventory & requirements[section]):
        # you DO NOT have the requirement
        print(f'{RED}You do not have the requirements to choose this option\n{END}')
        section = previous_section

    if section in check_money and not (you.money >= check_money[section]):
        print(f'{RED}you do not have enough money to choose this option\n{END}')
        section = previous_section

    #printing
    string = parser.get(section, '__text').format(**globals())
    for line in ('  ' + string).splitlines():
        if line.startswith('"'):
            line = '  ' + line.strip()
        print(textwrap.fill(line, 60))
    previous_section = section
    
    #check for modifiers
    if section in heal:
        you.heal(int(heal[section][0]))
    if section in hurt:
        you.hurt(int(hurt[section][0]))
    if section in pay_dict:
        you.pay(pay_dict[section][0])
    if section in change_wallet:
        you.change_wallet(change_wallet[section][0])
    if section in remove_item_dict:
        you.remove_item(remove_item_dict[section])
    if section in perceptiondict:
        found = perception(perceptiondict[section])
        if found != None:
            you.gain_item([found])
        else:
            print(textwrap.fill(parser.get(section, '__no_items'), 60))
        # discard all items from this section after the first try
        perceptiondict[section] = set()
    if section in gain_item_dict:
        you.gain_item(gain_item_dict[section])
    if you.health < 1:
        message = ''
        if section in death_message:
            for word in death_message[section]:
                message += ' ' + word
                print(word)
            print(textwrap.fill(message, 60))
        print('YOU DIED; GAME OVER'.center(60))
        exit()
    if section in gamble_dict:
        gamble(you, start=gamble_dict[section][0], multiplier=gamble_dict[section][1])
    if section in quit:
        exit()
    
    #asking
    opt = parser.options(section)
    for option in parser.options(section):
        if option.startswith('__option'):
            options[option] = parser.get(section, option)
            if '^' in options[option]:
                options[option] = options[option].split('^')
            else:
                options[option] = [options[option], options[option]]
    section = ask(options, requirements, check_money, you)
    if parser.has_option(section, '__health') == True:
        heal(int(parser.get(section, '__health')), health)
    print('\n', '_'*60, '\n')
    past_sections.append(section)

