gcc -Wall -g \
    test1.c \
    -o test1

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test1 2> gcc_test_output_valgrind1.txt

rm test2

gcc -Wall -g \
    test2.c \
    -o test2

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test2 2> gcc_test_output_valgrind2.txt

rm test2


gcc -Wall -g \
    test3.c \
    -o test3

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test3 2> gcc_test_output_valgrind3.txt

rm test3


gcc -Wall -g \
    test4.c \
    -o test4

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test4 2> gcc_test_output_valgrind4.txt

rm test4


gcc -Wall -g \
    test5.c \
    -o test5

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test5 2> gcc_test_output_valgrind5.txt

rm test5


gcc -Wall -g \
    test6.c \
    -o test6

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test6 2> gcc_test_output_valgrind6.txt

rm test6


gcc -Wall -g \
    test7.c \
    -o test7

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test7 2> gcc_test_output_valgrind7.txt

rm test7


gcc -Wall -g \
    test8.c \
    -o test8

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test8 2> gcc_test_output_valgrind8.txt

rm test8


gcc -Wall -g \
    test9.c \
    -o test9

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test9 2> gcc_test_output_valgrind9.txt

rm test9


gcc -Wall -g \
    test10.c \
    -o test10

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test10 2> gcc_test_output_valgrind10.txt

rm test10


gcc -Wall -g \
    test11.c \
    -o test11

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test11 2> gcc_test_output_valgrind11.txt

rm test11


gcc -Wall -g \
    test12.c \
    -o test12

valgrind --tool=memcheck --leak-check=full --track-origins=yes ./test12 2> gcc_test_output_valgrind12.txt

rm test12

