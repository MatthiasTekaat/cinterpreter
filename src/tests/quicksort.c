#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

void memswap(void *a_ptr, void *b_ptr, size_t size){
    // Swap the bytes of two memory locations
    char *a = (char*)a_ptr;
    char *b = (char*)b_ptr;
    for (size_t i = 0; i < size; i++){
        char tmp = a[i];
        a[i] = b[i];
        b[i] = tmp;
    }
}

typedef int (*compare_func)(const void*, const void*);

void quicksort(
    void *ptr,
    size_t count,
    size_t size,
    int (*compare)(const void*, const void*)
){
    if (count <= 1) return;
    char *left = (char*)ptr;
    char *pivot = left + (count - 1) * size;
    char *right = pivot - size;
    while (left < right){
        while (left < pivot && compare(left, pivot) <= 0) left += size;
        while (left < right && compare(right, pivot) >= 0) right -= size;
        if (left < right) memswap(left, right, size);
    }
    if (compare(left, pivot) > 0) memswap(left, pivot, size);
    size_t left_count = (left - (char*)ptr) / size;
    size_t right_count = count - left_count - 1;
    quicksort(ptr, left_count, size, compare);
    quicksort(left + size, right_count, size, compare);
}

int compare_int(const void *a_ptr, const void *b_ptr){
    int a = *(int*)a_ptr;
    int b = *(int*)b_ptr;
    return a < b ? -1 : a > b ? 1 : 0;
}

uint32_t state = 0x12345678;

uint32_t my_rand(){
    uint32_t x = state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    state = x;
    return x;
}

void test_n(size_t n){
    // Initialize values with random numbers from 0 to 9
    int *values = malloc(n * sizeof(int));
    int counts[10];
    for (size_t i = 0; i < 10; i++){
        counts[i] = 0;
    }
    for (size_t i = 0; i < n; i++){
        int value = (int)(my_rand() % 10);
        values[i] = value;
        counts[value]++;
    }

    quicksort(values, n, sizeof(int), compare_int);

    for (size_t i = 0; i < n; i++){
        printf("%d ", (int)values[i]);
    }

    printf("\n");

    // Values should be sorted
    for (size_t i = 1; i < n; i++){
        assert(values[i - 1] <= values[i]);
    }

    // Count of each value should still be the same
    for (size_t i = 0; i < n; i++){
        counts[values[i]]--;
    }
    for (size_t i = 0; i < 10; i++){
        assert(counts[i] == 0);
    }

    free(values);
}

int main(){
    for (size_t n = 0; n < 30; n++){
        test_n(n);
    }
    test_n(100);
    return 0;
}