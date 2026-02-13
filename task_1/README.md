# How to change array type during building
* Build with double type

By default, array type is *double*, and to start program you just need to:

```
mkdir build
cd build
cmake..
make
./array_program.out
```
Rezults: 

```
Using double type
First 5 elements: 0 6.28e-07 1.256e-06 1.884e-06 2.512e-06
```

* Build with float type

If you want to change array type to *float*, you just need to add an option during building like this(you should stay in the same directory):

```
rm -rf *
cmake -DUSE_FLOAT=ON ..
make
./array_program.out
```

Rezults:

```
Using float type
First 5 elements: 0 6.28e-07 1.256e-06 1.884e-06 2.512e-06
```
