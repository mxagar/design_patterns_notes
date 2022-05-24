/*
 * From the Udemy course "Design Patterns in Modern C++"
 * https://www.udemy.com/course/patterns-cplusplus/
 * by Dmitri Nesteruk.
 * 
 * Single Responsibility Principle
 * 
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <boost/lexical_cast.hpp>
using namespace std;

struct Journal
{
  string title;
  vector<string> entries;

  // explicit: the constructor must have this form
  // Journal J("my tytle"); // OK
  // Journal J = "my title"; // WRONG
  explicit Journal(const string& title)
    : title{title}
  {
  }

  void add(const string& entry);

  // persistence is a separate concern
  void save(const string& filename);
};

void Journal::add(const string& entry)
{
  // static: 
  // - class members (variables): one exists for the class, all objects share it
  // - class methods (functions): can be used even though no object exists: class::method()
  // - outside a class: it means function/variable are bound only to the scope of the source file,
  //      it exists only there;
  //      advantage: we can repeat names in other files
  // boost::lexical_cast: casting with boost
  static int count = 1; // static class member: called only once, one for the class / all objects share the same
  entries.push_back(boost::lexical_cast<string>(count++) + ": " + entry);
}

// `Journal` focuses only on adding and storing entries in memory
// If we assign to it the responsibility of saving to disk, we're extending
// its responsibilities.
// If we decide to change the saving to be in a data base instead of in a TXT,
// we might want to do it for all similar classes,
// so having everything in a centralized place is very helpful:
// we don't need to change the separate classes, but just the `PersistenceManager`!
void Journal::save(const string& filename)
{
  // ofs: output filestream: we open a file and save lines to it
  ofstream ofs(filename);
  for (auto& s : entries)
    ofs << s << endl;
}

// Principle of Separation of Concerns: each class is concerned with one issue
// See comments in `Journal::save()`
struct PersistenceManager
{
  // static method: can be called even without PM is not instantiated
  // example: PersistenceManager::save(journal, "diary.txt")
  static void save(const Journal& j, const string& filename)
  {
    ofstream ofs(filename);
    for (auto& s : j.entries)
      ofs << s << endl;
  }

  // Other save() functions of similar classes would go here, too

};

int main()
{
  Journal journal{"Dear Diary"};
  journal.add("I ate a bug");
  journal.add("I cried today");

  // Instead of using class-specific method
  // we use PM below
  //journal.save("diary.txt");

  // Since save is static,
  // we can use it without instantiating PM!
  //PersistenceManager pm;
  //pm.save(journal, "diary.txt");
  PersistenceManager::save(journal, "diary.txt");

  return 0;
}