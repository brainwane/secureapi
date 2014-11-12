#include <stdlib.h>

int foo(int n, unsigned m)
{
  if (n < m)
    return 2;
  else
    return 3;
}

void main()
{
  int x = 42;
  int y = x/0;
    char *p;
    *p = 0;

    int* k = NULL;
    int q = *k;
}

void test() {
  char x[4];
  char *y = "abcd";

  strcpy(x, y); // strcpy
}

void test2() {
  char *x = mktemp("/tmp/zxcv"); // mktemp
}

void test3(int b) {
  void *w = malloc(b * sizeof(int)); // warn
}
