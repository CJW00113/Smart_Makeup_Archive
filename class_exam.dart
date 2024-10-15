class Point {
  double _x = 0;
  double _y = 0;

  Point(double x, double y) {
    this._x = x;
    this._y = y;
  }

  double get x => _x;
  double get y => _y;

  set x(double x) => _x = x;
  set y(double y) => _y = y;
  // set x(double x) {
  //   _x = x;
  // }

  // set y(double y) {
  //   _y = y;
  // }

  void display() {
    print("{${_x}, ${_y}}");
  }
}

void main() {
  Point p1 = new Point(10, 20);
  p1.x = 11.3;
  p1.y = 223.2;

  print(p1.x);
  print(p1.y);
}
