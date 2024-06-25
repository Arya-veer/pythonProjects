"""
Machine
    - Select Product
    - Pay Money
    - Get Product
    - Refill
Machine has Slots
Slot has Items
Slot has Price
Slot has Quantity
"""

# Linting: Linters are tools that analyze source code to flag programming errors, bugs, stylistic errors, and suspicious constructs.

class Item:
    def __init__(self,name:str) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return f"Item: {self.name}"
    

class Slot:
    def __init__(self) -> None:
        self.items = []
        self.price = 0
        self.quantity = 0
    
    def __str__(self) -> str:
        if self.quantity == 0:
            return f"Slot: Empty"
        return f"Slot: {self.items[0]}, Item=>{self.price}, Quantity=>{self.quantity}"
    
    def get_item(self) -> Item:
        if self.quantity == 0:
            return None
        self.quantity -= 1
        if self.quantity == 0:
            self.price = 0
        return self.items.pop(0)

    def add_item(self,item:Item,quantity:int,price:int|None=None)->None:
        
        for _ in range(quantity):
            self.items.append(Item(item))
        if self.quantity == 0:
            self.price = price
        self.quantity += quantity

class VendingMachine:
    
    def __init__(self,rows:int=6,cols:int=5) -> None:
        self.slots = {}
        # 30 slots, 11-15, 21-25, 31-35, 41-45, 51-55, 61-65
        for row in range(1,rows+1):
            for col in range(1,cols+1):
                self.slots[f"{row}{col}"] = Slot()

        self.selected_slot = None
        self.paid_amount = 0
                
    def __str__(self) -> str:
        return f"VendingMachine\n" + "\n".join([f"{slot}: {self.slots[slot]}" for slot in self.slots])

    def select_product(self,slot:str):
        try:
            self.selected_slot = self.slots[slot]
            print(f"You selected {self.selected_slot.items[0]} having price = {self.selected_slot.price}")
        except KeyError:
            print(f"Invalid Slot: {slot}")
            
    def pay_money(self,amount:int) -> None:
        if self.selected_slot is None or self.selected_slot.quantity == 0:
            print("Please select a valid slot")
            return 
        self.paid_amount += amount
        print(f"You have paid {amount}")
        if(self.paid_amount < self.selected_slot.price):
            print(f"Please pay {self.selected_slot.price-amount} more")
            return
        if amount > self.selected_slot.price:
            print(f"Please collect your product")
        else:
            print(f"Please collect your product and a refund of {self.paid_amount-self.selected_slot.price}")
        item = self.selected_slot.get_item()
        print(f"Thank you for shopping with us, your item is {item}")
        return item
    
    
    
    def refill(self,slot:str,item:str,price:int|None,quantity:int)->None:
        try:
            self.slots[slot].add_item(item,quantity,price)
        except KeyError:
            print(f"Invalid Slot: {slot}")


def main()->None:
    
    vm = VendingMachine()
    print(vm)
    vm.refill("11","Coke",10,5)
    vm.refill("12","Pepsi",15,5)
    vm.refill("13","Kurkure",20,5)
    vm.refill("24","Lays",25,5)
    print(vm)
    vm.select_product("24")
    vm.pay_money(20)
    vm.pay_money(5)
    print(vm)
    

if __name__ == "__main__":
    main()