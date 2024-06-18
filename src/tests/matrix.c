#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>

typedef struct {
    double *values;
    int m, n;
} Matrix;

#define at(M, i, j) (M->values[(i) * M->n + (j)])

Matrix* zeros(int m, int n) {
    Matrix *A = malloc(sizeof(Matrix));
    A->m = m;
    A->n = n;
    A->values = malloc(sizeof(double) * m * n);
    for (int i = 0; i < m * n; i++) {
        A->values[i] = 0.0;
    }
    return A;
}

void free_matrix(Matrix *A) {
    free(A->values);
    free(A);
}

Matrix* eye(int n) {
    Matrix *A = zeros(n, n);
    for (int i = 0; i < n; i++) {
        at(A, i, i) = 1.0;
    }
    return A;
}

void print(Matrix *A) {
    printf("%d-by-%d matrix:\n", A->m, A->n);
    for (int i = 0; i < A->m; i++) {
        for (int j = 0; j < A->n; j++) {
            printf("%10.6f ", at(A, i, j));
        }
        printf("\n");
    }
    printf("\n");
}

Matrix* mul(Matrix *A, Matrix *B) {
    assert(A->n == B->m);
    Matrix *C = zeros(A->m, B->n);
    for (int i = 0; i < A->m; i++) {
        for (int j = 0; j < B->n; j++) {
            double sum = 0.0;
            for (int k = 0; k < A->n; k++) {
                sum += at(A, i, k) * at(B, k, j);
            }
            at(C, i, j) = sum;
        }
    }
    return C;
}

Matrix* sub(Matrix *A, Matrix *B) {
    assert(A->m == B->m && A->n == B->n);
    Matrix *C = zeros(A->m, A->n);
    for (int i = 0; i < A->m * A->n; i++) {
        C->values[i] = A->values[i] - B->values[i];
    }
    return C;
}

double frob(Matrix *A) {
    double sum = 0.0;
    for (int i = 0; i < A->m * A->n; i++) {
        double value = A->values[i];
        sum += value * value;
    }
    return sqrt(sum);
}

Matrix* transpose(Matrix *A) {
    Matrix *B = zeros(A->n, A->m);
    for (int i = 0; i < A->m; i++) {
        for (int j = 0; j < A->n; j++) {
            at(B, j, i) = at(A, i, j);
        }
    }
    return B;
}

void swap_rows(Matrix *A, int i, int j) {
    for (int k = 0; k < A->n; k++) {
        double temp = at(A, i, k);
        at(A, i, k) = at(A, j, k);
        at(A, j, k) = temp;
    }
}

Matrix* copy(Matrix *A) {
    Matrix *B = zeros(A->m, A->n);
    for (int i = 0; i < A->m * A->n; i++) {
        B->values[i] = A->values[i];
    }
    return B;
}

Matrix* inv(Matrix *A){
    // Invert a matrix using Gauss-Jordan elimination
    // with partial pivoting.
    assert(A->m == A->n);
    int n = A->m;
    A = copy(A);
    Matrix *B = eye(n);

    // Forward elimination
    for (int i = 0; i < n; i++) {
        // Find pivot
        double pivot = at(A, i, i);
        int pivot_row = i;
        for (int j = i + 1; j < n; j++) {
            double value = at(A, j, i);
            if (fabs(value) > fabs(pivot)) {
                pivot = value;
                pivot_row = j;
            }
        }

        // Swap rows if necessary
        if (pivot_row != i) {
            swap_rows(A, i, pivot_row);
            swap_rows(B, i, pivot_row);
        }

        // Divide row by pivot
        for (int j = 0; j < n; j++) {
            at(B, i, j) /= pivot;
            at(A, i, j) /= pivot;
        }

        // Eliminate column
        for (int j = i + 1; j < n; j++) {
            double factor = at(A, j, i);
            for (int k = 0; k < n; k++) {
                at(A, j, k) -= factor * at(A, i, k);
                at(B, j, k) -= factor * at(B, i, k);
            }
        }
    }

    // Backward elimination
    for (int i = A->m - 1; i >= 0; i--) {
        for (int j = 0; j < i; j++) {
            double factor = at(A, j, i);
            for (int k = 0; k < A->m; k++) {
                at(A, j, k) -= factor * at(A, i, k);
                at(B, j, k) -= factor * at(B, i, k);
            }
        }
    }

    free_matrix(A);
    
    return B;
}

bool allclose(Matrix *A, Matrix *B, double tol) {
    assert(A->m == B->m && A->n == B->n);
    for (int i = 0; i < A->m * A->n; i++) {
        double diff = fabs(A->values[i] - B->values[i]);
        if (diff > tol) {
            return false;
        }
    }
    return true;
}

uint32_t state = 0x12345678;

uint32_t my_randint(){
    uint32_t x = state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    state = x;
    return x;
}

double my_randdouble() {
    return (my_randint() - 1) / (double) 0xffffffff;
}

Matrix* mat_rand(int m, int n) {
    Matrix *A = zeros(m, n);
    for (int i = 0; i < m * n; i++) {
        A->values[i] = my_randdouble();
    }
    return A;
}

void test_inverse_3x3(){
    // {{7, 2, 1}, {0, 3, -1}, {-3, 4, -2}}
    Matrix *A = zeros(3, 3);
    at(A, 0, 0) = 7.0;
    at(A, 0, 1) = 2.0;
    at(A, 0, 2) = 1.0;
    at(A, 1, 0) = 0.0;
    at(A, 1, 1) = 3.0;
    at(A, 1, 2) = -1.0;
    at(A, 2, 0) = -3.0;
    at(A, 2, 1) = 4.0;
    at(A, 2, 2) = -2.0;

    // Expected inverse: {{-2, 8, -5}, {3, -11, 7}, {9, -34, 21}}
    Matrix *Ainv = zeros(3, 3);
    at(Ainv, 0, 0) = -2.0;
    at(Ainv, 0, 1) = 8.0;
    at(Ainv, 0, 2) = -5.0;
    at(Ainv, 1, 0) = 3.0;
    at(Ainv, 1, 1) = -11.0;
    at(Ainv, 1, 2) = 7.0;
    at(Ainv, 2, 0) = 9.0;
    at(Ainv, 2, 1) = -34.0;
    at(Ainv, 2, 2) = 21.0;

    Matrix *B = inv(A);

    assert(allclose(Ainv, B, 1e-10));

    print(B);

    // Multiplying matrix with its inverse should result in identity matrix
    Matrix *AB = mul(A, B);

    Matrix *I = eye(3);
    
    Matrix *D = sub(I, AB);

    double error = frob(D);

    assert(error < 1e-10);

    free_matrix(A);
    free_matrix(B);
    free_matrix(Ainv);
    free_matrix(AB);
    free_matrix(I);
    free_matrix(D);
}

void test_inverse_large(){
    int n = 20;
    Matrix *A = mat_rand(n, n);
    Matrix *B = inv(A);
    Matrix *I = eye(n);
    Matrix *AB = mul(A, B);
    Matrix *D = sub(I, AB);
    double error = frob(D);
    assert(error < 1e-10);
    free_matrix(A);
    free_matrix(B);
    free_matrix(I);
    free_matrix(AB);
    free_matrix(D);
}

int main() {
    test_inverse_3x3();
    test_inverse_large();

    return 0;
}