gcc -Wall -Wextra -Werror -fsanitize=address,undefined \
    doubly_linked_list.c \
    -o main

./main > doubly_linked_list_expected.txt

rm main

gcc -Wall -Wextra -pedantic -fsanitize=address,undefined \
    matrix.c \
    -o main -lm

./main > matrix_expected.txt

rm main

gcc -Wall -Wextra -pedantic -fsanitize=address,undefined \
    quicksort.c \
    -o main -lm

./main > quicksort_expected.txt

rm main
