class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)

    # Break SRP = Single Responsibility Principle
    # Saving is a responsibility that should be handled
    # by a class that persists the complete family
    # of journal classes!
    # Giving too many responsibilities to single classes
    # creates the anti-pattern of a God Object:
    # a gigant class which does everything,
    # which is very difficult to maintain!
    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self))
        file.close()

    def load(self, filename):
        pass

    def load_from_web(self, uri):
        pass

# Persisting of objects should be handled by a spacific class
# which takes care of all faminily of journal classes.
# That way, the saving processes are all localized
# in the same spot -> easier to maintain!
class PersistenceManager:
    # Static method: it cannot access/modify either the instance or the class
    # but it can be used from both.
    # They signal that the function is independent from the class/object,
    # i.e., some kind of utility procedure; that improves mantainability.
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, "w")
        file.write(str(journal))
        file.close()

if __name__ == "__main__":

    j = Journal()
    j.add_entry("I cried today.")
    j.add_entry("I ate a bug.")
    print(f"Journal entries:\n{j}\n")

    p = PersistenceManager()
    file = r'./journal.txt'
    p.save_to_file(j, file)

    # verify!
    with open(file) as fh:
        print(fh.read())
