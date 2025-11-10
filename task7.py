from abc import ABC, abstractmethod
from datetime import datetime

class BillDispenser(ABC):
    def __init__(self, denomination, available_count):
        self.denomination = denomination
        self.available_count = available_count
        self.next_dispenser = None
    
    def set_next(self, dispenser):
        self.next_dispenser = dispenser
        return dispenser
    
    def dispense(self, amount, transaction):
        # Calculate how many bills of this denomination to dispense
        num_bills = self.can_dispense(amount)
        
        if num_bills > 0:
            transaction.add_bills(self.denomination, num_bills)
            self.available_count -= num_bills
            remaining = amount - (num_bills * self.denomination)
            print(f"Dispensing {num_bills} x {self.denomination} DZD bills")
        else:
            remaining = amount
        
        # Pass to next dispenser if there's remaining amount
        if remaining > 0 and self.next_dispenser:
            return self.next_dispenser.dispense(remaining, transaction)
        elif remaining > 0:
            print(f"Cannot dispense remaining {remaining} DZD")
            return False
        
        return True
    
    @abstractmethod
    def can_dispense(self, amount):
        pass

class Dispenser2000(BillDispenser):
    def __init__(self, count):
        super().__init__(2000, count)
    
    def can_dispense(self, amount):
        # Calculate optimal number of bills
        num_bills = min(amount // self.denomination, self.available_count)
        return num_bills

class Dispenser1000(BillDispenser):
    def __init__(self, count):
        super().__init__(1000, count)
    
    def can_dispense(self, amount):
        num_bills = min(amount // self.denomination, self.available_count)
        return num_bills

class Dispenser500(BillDispenser):
    def __init__(self, count):
        super().__init__(500, count)
    
    def can_dispense(self, amount):
        num_bills = min(amount // self.denomination, self.available_count)
        return num_bills

class Dispenser200(BillDispenser):
    def __init__(self, count):
        super().__init__(200, count)
    
    def can_dispense(self, amount):
        num_bills = min(amount // self.denomination, self.available_count)
        return num_bills

class Transaction:
    _counter = 0
    
    def __init__(self, amount):
        Transaction._counter += 1
        self.transaction_id = f"TXN{Transaction._counter:04d}"
        self.requested_amount = amount
        self.bills = {}
        self.timestamp = datetime.now()
        self.success = False
    
    def add_bills(self, denomination, count):
        self.bills[denomination] = count
    
    def get_total(self):
        return sum(denom * count for denom, count in self.bills.items())
    
    def get_receipt(self):
        receipt = f"\n{'='*40}"
        receipt += f"\n        ATM RECEIPT"
        receipt += f"\n{'='*40}"
        receipt += f"\nTransaction ID: {self.transaction_id}"
        receipt += f"\nDate: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        receipt += f"\nRequested: {self.requested_amount} DZD"
        receipt += f"\n{'-'*40}"
        
        if self.bills:
            receipt += f"\nDispensed Bills:"
            total_bills = 0
            for denom in sorted(self.bills.keys(), reverse=True):
                count = self.bills[denom]
                receipt += f"\n  {count} x {denom} DZD = {count * denom} DZD"
                total_bills += count
            receipt += f"\n{'-'*40}"
            receipt += f"\nTotal Bills: {total_bills}"
            receipt += f"\nTotal Amount: {self.get_total()} DZD"
            receipt += f"\nStatus: {'SUCCESS' if self.success else 'FAILED'}"
        else:
            receipt += f"\nStatus: FAILED - Cannot dispense"
        
        receipt += f"\n{'='*40}\n"
        return receipt

class ATM:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Initialize dispensers with starting bills
        self.dispenser_2000 = Dispenser2000(10)
        self.dispenser_1000 = Dispenser1000(10)
        self.dispenser_500 = Dispenser500(10)
        self.dispenser_200 = Dispenser200(10)
        
        # Build the chain (largest to smallest for optimization)
        self.dispenser_chain = self.dispenser_2000
        self.dispenser_2000.set_next(self.dispenser_1000)
        self.dispenser_1000.set_next(self.dispenser_500)
        self.dispenser_500.set_next(self.dispenser_200)
        
        self.transactions = []
    
    def withdraw(self, amount):
        print(f"\n--- Withdrawal Request: {amount} DZD ---")
        
        # Validation
        if amount <= 0:
            print("Invalid amount!")
            return None
        
        if amount % 200 != 0:
            print("Amount must be multiple of 200 DZD!")
            return None
        
        # Create transaction
        transaction = Transaction(amount)
        
        # Try to dispense
        success = self.dispenser_chain.dispense(amount, transaction)
        transaction.success = success
        
        if success:
            self.transactions.append(transaction)
            print(f"Transaction successful!")
        else:
            print(f"Transaction failed!")
            self._restore_bills(transaction)
        
        return transaction
    
    def _restore_bills(self, transaction):
        # Restore bills if transaction failed
        for denom, count in transaction.bills.items():
            if denom == 2000:
                self.dispenser_2000.available_count += count
            elif denom == 1000:
                self.dispenser_1000.available_count += count
            elif denom == 500:
                self.dispenser_500.available_count += count
            elif denom == 200:
                self.dispenser_200.available_count += count
    
    def check_balance(self):
        print("\n--- ATM Bill Inventory ---")
        total = 0
        
        dispensers = [
            self.dispenser_2000,
            self.dispenser_1000,
            self.dispenser_500,
            self.dispenser_200
        ]
        
        for dispenser in dispensers:
            value = dispenser.denomination * dispenser.available_count
            total += value
            print(f"{dispenser.denomination} DZD: {dispenser.available_count} bills = {value} DZD")
        
        print(f"Total Available: {total} DZD")
    
    def refill_bills(self, denomination, count):
        print(f"\nRefilling {count} x {denomination} DZD bills")
        if denomination == 2000:
            self.dispenser_2000.available_count += count
        elif denomination == 1000:
            self.dispenser_1000.available_count += count
        elif denomination == 500:
            self.dispenser_500.available_count += count
        elif denomination == 200:
            self.dispenser_200.available_count += count


print("=== Atm simulation ===")

atm = ATM()

atm.check_balance()

# case 1: normal withdraw
txn1 = atm.withdraw(5700)
if txn1:
    print(txn1.get_receipt())

# case 2: multiple dispensers will be usedd
txn2 = atm.withdraw(3400)
if txn2:
    print(txn2.get_receipt())

# case 3: Invalid amount (not multiple of 200)
txn3 = atm.withdraw(2150)

#  Case 4: Large withdrawal
txn4 = atm.withdraw(8000)
if txn4:
    print(txn4.get_receipt())

atm.check_balance()

# case 5: too much amount
txn5 = atm.withdraw(50000)

# case 6: only small denominations left
txn6 = atm.withdraw(1000)
if txn6:
    print(txn6.get_receipt())

atm.check_balance()

# Refill and test
atm.refill_bills(2000, 5)
atm.withdraw(4000)
