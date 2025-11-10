from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime

class Caliber(Enum):
    FINE = "Fine"
    MEDIUM = "Medium"
    LARGE = "Large"

class Pasta(ABC):
    def __init__(self, shape, caliber):
        self.shape = shape
        self.caliber = caliber
        self.production_time = 0
    
    @abstractmethod
    def get_description(self):
        pass
    
    @abstractmethod
    def get_production_time(self):
        pass
    
    def produce(self):
        print(f"Producing {self.get_description()}...")

class Spaghetti(Pasta):
    def __init__(self, caliber):
        super().__init__("Spaghetti", caliber)
        self._set_production_time()
    
    def get_description(self):
        return f"{self.caliber.value} {self.shape}"
    
    def get_production_time(self):
        return self.production_time
    
    def _set_production_time(self):
        base_time = 10
        if self.caliber == Caliber.FINE:
            self.production_time = base_time + 2
        elif self.caliber == Caliber.MEDIUM:
            self.production_time = base_time + 5
        else:  # LARGE
            self.production_time = base_time + 8

class Penne(Pasta):
    def __init__(self, caliber):
        super().__init__("Penne", caliber)
        self._set_production_time()
    
    def get_description(self):
        return f"{self.caliber.value} {self.shape}"
    
    def get_production_time(self):
        return self.production_time
    
    def _set_production_time(self):
        base_time = 12
        if self.caliber == Caliber.FINE:
            self.production_time = base_time + 3
        elif self.caliber == Caliber.MEDIUM:
            self.production_time = base_time + 6
        else:  # LARGE
            self.production_time = base_time + 9

class Fusilli(Pasta):
    def __init__(self, caliber):
        super().__init__("Fusilli", caliber)
        self._set_production_time()
    
    def get_description(self):
        return f"{self.caliber.value} {self.shape}"
    
    def get_production_time(self):
        return self.production_time
    
    def _set_production_time(self):
        base_time = 15
        if self.caliber == Caliber.FINE:
            self.production_time = base_time + 4
        elif self.caliber == Caliber.MEDIUM:
            self.production_time = base_time + 7
        else:  # LARGE
            self.production_time = base_time + 10

class PastaFactory:
    @staticmethod
    def create_pasta(shape, caliber):
        if shape.lower() == "spaghetti":
            return Spaghetti(caliber)
        elif shape.lower() == "penne":
            return Penne(caliber)
        elif shape.lower() == "fusilli":
            return Fusilli(caliber)
        else:
            print(f"Unknown shape: {shape}")
            return None

class ProductionBatch:
    def __init__(self, batch_id):
        self.batch_id = batch_id
        self.pastas = []
        self.batch_date = datetime.now()
    
    def add_pasta(self, pasta):
        self.pastas.append(pasta)
    
    def get_total_time(self):
        return sum(p.get_production_time() for p in self.pastas)
    
    def get_report(self):
        report = f"\n--- Batch {self.batch_id} Report ---"
        report += f"\nTotal Items: {len(self.pastas)}"
        report += f"\nTotal Production Time: {self.get_total_time()} minutes"
        report += "\nItems:"
        for pasta in self.pastas:
            report += f"\n  - {pasta.get_description()} ({pasta.get_production_time()} min)"
        return report

class ProductionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.production_line = []
            cls._instance.batches = []
            cls._instance.total_produced = 0
        return cls._instance
    
    def add_to_production(self, shape, caliber):
        pasta = PastaFactory.create_pasta(shape, caliber)
        if pasta:
            self.production_line.append(pasta)
            print(f"Added {pasta.get_description()} to production line")
    
    def start_production(self):
        if not self.production_line:
            print("Production line is empty!")
            return
        
        print("\n=== Starting Production ===")
        batch = ProductionBatch(f"BATCH-{len(self.batches) + 1}")
        
        for pasta in self.production_line:
            pasta.produce()
            batch.add_pasta(pasta)
            self.total_produced += 1
        
        self.batches.append(batch)
        print(f"\nProduced {len(self.production_line)} items")
        self.production_line.clear()
    
    def get_production_report(self):
        print("\n=== PRODUCTION REPORT ===")
        print(f"Total Batches: {len(self.batches)}")
        print(f"Total Items Produced: {self.total_produced}")
        
        for batch in self.batches:
            print(batch.get_report())

manager = ProductionManager()

print("--- Adding this to Production Line:")
manager.add_to_production("spaghetti", Caliber.FINE)
manager.add_to_production("spaghetti", Caliber.MEDIUM)
manager.add_to_production("penne", Caliber.LARGE)
manager.add_to_production("fusilli", Caliber.FINE)
manager.add_to_production("fusilli", Caliber.LARGE)

manager.start_production()

print("\n--- second Batch ---")
manager.add_to_production("penne", Caliber.FINE)
manager.add_to_production("penne", Caliber.MEDIUM)
manager.add_to_production("spaghetti", Caliber.LARGE)

manager.start_production()

manager.get_production_report()

print("\n\n=== TEST  ===")
shapes = ["spaghetti", "penne", "fusilli"]
calibers = [Caliber.FINE, Caliber.MEDIUM, Caliber.LARGE]

for shape in shapes:
    for caliber in calibers:
        pasta = PastaFactory.create_pasta(shape, caliber)
        print(f"{pasta.get_description()}: {pasta.get_production_time()} min")
