import Grammar
import random

def main():
    Building = Grammar.Grammar()
    Building.generate_parent()
    Building.generate_child(random.randint(1,30))
    Building.generate_outline()
    Building.display()

if __name__ == '__main__':
    main()