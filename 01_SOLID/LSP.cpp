/*
 * From the Udemy course "Design Patterns in Modern C++"
 * https://www.udemy.com/course/patterns-cplusplus/
 * by Dmitri Nesteruk.
 * 
 * Liskov Substitution Principle
 * Objects in a program should be replaceable with instances of their subtypes
 * w/o altering the correctness of the program, and vice versa
 * 
 */

#include <iostream>

class Rectangle
{
// Protexted: accessible from within the class, inherited class & children
protected:
  int width, height;
public:
  Rectangle(const int width, const int height)
    : width{width}, height{height} { }

  // set_* is virtual so that they are overridden in child class Square
  int get_width() const { return width; }
  virtual void set_width(const int width) { this->width = width; }
  int get_height() const { return height; }
  virtual void set_height(const int height) { this->height = height; }

  int area() const { return width * height; }
};

// Square is inherited from Rectangle
// It sounds plausible, but doing so, when we redefine the set_*
// methods, the Liskov substitution principle is broken!
// We cannot substitute a square by a rectangle
class Square : public Rectangle
{
public:
  Square(int size): Rectangle(size,size) {}
  // We override virtual set_* functions
  void set_width(const int width) override {
    // Setting both the height and the width with size
    // is correct for the Square, but wrong for the Rectangle.
    // We are breaking the Liskov substitution principle!
    this->width = height = width;
  }
  void set_height(const int height) override {
    this->height = width = height;
  }
};

// Possible solutions to avoid breaking Liskov:
// - Square maybe should not be inherited from Rectangle
// - Instead, we could use Rectangle, and (1) add a flag inside to denote when it's a square
// - or, (2) we can use a factory with Rectangles.
// The factory creates rectangles or squares, but it always returns Rectangles.
struct RectangleFactory
{
  // Static functions: they can be called without instantiating RectangleFactory
  // Functions to be implemented.
  static Rectangle create_rectangle(int w, int h);
  static Rectangle create_square(int size);
};

// This function processes Rectangles passed by reference
// so we can pass also Squares.
// BUT: Since the Liskov substitution principe is broken,
// it won't work as expected.
void process(Rectangle& r)
{
  int w = r.get_width();
  r.set_height(10);

  std::cout << "expected area = " << (w * 10) 
    << ", got " << r.area() << std::endl;
}

int main()
{
  Rectangle r{ 5,5 };
  process(r);

  Square s{ 5 };
  process(s);

  //getchar();
  return 0;
}