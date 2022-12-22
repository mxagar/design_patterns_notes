from abc import abstractmethod

class Machine:
    def print(self, document):
        raise NotImplementedError

    def fax(self, document):
        raise NotImplementedError

    def scan(self, document):
        raise NotImplementedError

# A multi-function device works with all the
# interfaces from Machine, so it's OK
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass # we would write our implementation

    def fax(self, document):
        pass # we would write our implementation

    def scan(self, document):
        pass # we would write our implementation

# An old-fashioned printer is not expected to have all the
# functionalities in Machine!
class OldFashionedPrinter(Machine):
    def print(self, document):
        # OK for an old-fashioned printer, it can print
        pass # we would write our implementation

    def fax(self, document):
        # No operation: an old-fashioned printer cannot fax!
        pass  # do-nothing: problematic, because the interface is there!

    # An old-fashioned printer cannot scan
    def scan(self, document):
        """Not supported!"""
        # Another option to doing nothing is raising an error
        # but it crashes the code.
        raise NotImplementedError('Printer cannot scan!')

## Solution: we create classes for each functionality and then combine them!

# Abstract class: not to be instantiate, only inherited
class Printer:
    # Abstract method: not implemented
    @abstractmethod
    def print(self, document): pass

class Scanner:
    @abstractmethod
    def scan(self, document): pass

class FaxMachine:
    @abstractmethod
    def fax(self, document): pass

# Concrete classes inheriting base abstract classes
class MyPrinter(Printer):
    def print(self, document):
        print(document)

class Photocopier(Printer, Scanner):
    def print(self, document):
        print(document)

    def scan(self, document):
        pass  # something meaningful

# Abstract class which combines several abstract classes
class MultiFunctionDevice(Printer, Scanner, FaxMachine):
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass

    @abstractmethod
    def fax(self, document):
        pass
    
class MultiFunctionMachine(MultiFunctionDevice):
    #def __init__(self, printer, scanner, faxmachine):
    #    self.printer = printer
    #    self.scanner = scanner
    #    self.faxmachine = faxmachine

    def print(self, document):
        #self.printer.print(document)
        print("printing", document)
        
    def scan(self, document):
        #self.scanner.scan(document)
        print("scanning", document)
        
    def fax(self, document):
        #self.faxmachine.fax(document)
        print("faxing", document)

if __name__ == "__main__":

    my_machine = MultiFunctionMachine()
    my_machine.print('test')
    my_machine.fax('test')
    my_machine.scan('test')

    # This will raise an error
    printer = OldFashionedPrinter()
    printer.fax(123)  # nothing happens
    printer.scan(123)  # oops!
