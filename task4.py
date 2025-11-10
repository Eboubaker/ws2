from abc import ABC, abstractmethod

class Coffee(ABC):
    def __init__(self):
        self.description = "coffee"
    
    @abstractmethod
    def get_description(self):
        pass
    
    @abstractmethod
    def get_cost(self):
        pass

class Espresso(Coffee):
    def __init__(self):
        self.description = "Espresso"
    
    def get_description(self):
        return self.description
    
    def get_cost(self):
        return 50

class HouseBlend(Coffee):
    def __init__(self):
        self.description = "House Blend"
    
    def get_description(self):
        return self.description
    
    def get_cost(self):
        return 40

class Decaf(Coffee):
    def __init__(self):
        self.description = "Decaf"
    
    def get_description(self):
        return self.description
    
    def get_cost(self):
        return 45

class DarkRoast(Coffee):
    def __init__(self):
        self.description = "Dark Roast"
    
    def get_description(self):
        return self.description
    
    def get_cost(self):
        return 55

# Condiment Base
class CondimentDecorator(Coffee):
    def __init__(self, coffee):
        self.coffee = coffee
    
    @abstractmethod
    def get_description(self):
        pass
    
    @abstractmethod
    def get_cost(self):
        pass

# CONCRETE DECORATORS - Condiments
class Milk(CondimentDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Milk"
    
    def get_cost(self):
        return self.coffee.get_cost() + 10

class Chocolate(CondimentDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Chocolate"
    
    def get_cost(self):
        return self.coffee.get_cost() + 15

class Cream(CondimentDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Cream"
    
    def get_cost(self):
        return self.coffee.get_cost() + 12

class Soy(CondimentDecorator):
    def get_description(self):
        return self.coffee.get_description() + ", Soy"
    
    def get_cost(self):
        return self.coffee.get_cost() + 8


print("=== COFFEE SHOP ORDERS ===\n")

# coffe simple
coffee1 = Espresso()
print(f"Order 1: {coffee1.get_description()}")
print(f"Cost: ${coffee1.get_cost()}\n")

# espresso + milk
coffee2 = Espresso()
coffee2 = Milk(coffee2)
print(f"Order 2: {coffee2.get_description()}")
print(f"Cost: ${coffee2.get_cost()}\n")


coffee3 = HouseBlend()
coffee3 = Milk(coffee3)
coffee3 = Chocolate(coffee3)
print(f"Order 3: {coffee3.get_description()}")
print(f"Cost: ${coffee3.get_cost()}\n")

# dark + all additives
coffee4 = DarkRoast()
coffee4 = Milk(coffee4)
coffee4 = Chocolate(coffee4)
coffee4 = Cream(coffee4)
coffee4 = Soy(coffee4)
print(f"Order 4: {coffee4.get_description()}")
print(f"Cost: ${coffee4.get_cost()}\n")

# decafe + double chocolate
coffee5 = Decaf()
coffee5 = Chocolate(coffee5)
coffee5 = Chocolate(coffee5)
print(f"Order 5: {coffee5.get_description()}")
print(f"Cost: ${coffee5.get_cost()}\n")
