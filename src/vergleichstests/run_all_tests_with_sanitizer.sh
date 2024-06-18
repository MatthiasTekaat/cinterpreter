gcc -Wall -g -fsanitize=address,undefined \
    test1.c \
    -o test1

./test1 2> gcc_test_output_sanitizer1.txt

rm test1

gcc -Wall -g -fsanitize=address,undefined \
    test2.c \
    -o test2

./test2 2> gcc_test_output_sanitizer2.txt

rm test2


gcc -Wall -g -fsanitize=address,undefined \
    test3.c \
    -o test3

./test3 2> gcc_test_output_sanitizer3.txt

rm test3


gcc -Wall -g -fsanitize=address,undefined \
    test4.c \
    -o test4

./test4 2> gcc_test_output_sanitizer4.txt

rm test4


gcc -Wall -g -fsanitize=address,undefined \
    test5.c \
    -o test5

./test5 2> gcc_test_output_sanitizer5.txt

rm test5


gcc -Wall -g -fsanitize=address,undefined \
    test6.c \
    -o test6

./test6 2> gcc_test_output_sanitizer6.txt

rm test6


gcc -Wall -g -fsanitize=address,undefined \
    test7.c \
    -o test7

./test7 2> gcc_test_output_sanitizer7.txt

rm test7


gcc -Wall -g -fsanitize=address,undefined \
    test8.c \
    -o test8

./test8 2> gcc_test_output_sanitizer8.txt

rm test8


gcc -Wall -g -fsanitize=address,undefined \
    test9.c \
    -o test9

./test9 2> gcc_test_output_sanitizer9.txt

rm test9


gcc -Wall -g -fsanitize=address,undefined \
    test10.c \
    -o test10

./test10 2> gcc_test_output_sanitizer10.txt

rm test10


gcc -Wall -g -fsanitize=address,undefined \
    test11.c \
    -o test11

./test11 2> gcc_test_output_sanitizer11.txt

rm test11


gcc -Wall -g -fsanitize=address,undefined \
    test12.c \
    -o test12

./test12 2> gcc_test_output_sanitizer12.txt

rm test12

