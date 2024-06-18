#include <stddef.h>
#include <assert.h>

size_t strlen(const char *s){
    size_t n = 0;
    while (s[n] != '\0') n++;
    return n;
}

int cmp_uchar(const void *a, const void *b){
    unsigned char c1 = *(unsigned char *)a;
    unsigned char c2 = *(unsigned char *)b;
    return (c1 > c2) - (c1 < c2);
}

int strcmp(const char *a, const char *b){
    while (*a && *a == *b){
        a++;
        b++;
    }
    return cmp_uchar(a, b);
}

int strncmp(const char *a, const char *b, size_t n){
    while (n > 0 && *a && *a == *b){
        a++;
        b++;
        n--;
    }
    if (n == 0) return 0;
    return cmp_uchar(a, b);
}

char* strcpy(char *dest, const char *src){
    char *ret = dest;
    while (*src){
        *dest++ = *src++;
    }
    *dest = '\0';
    return ret;
}

char* strcat(char *dest, const char *src){
    char *ret = dest;
    while (*dest) dest++;
    while (*src) *dest++ = *src++;
    *dest = '\0';
    return ret;
}

char* strchr(const char *s, int c){
    while (*s && *s != (char)c) s++;
    if (*s == (char)c) return (char*)s;
    return NULL;
}

char* strrchr(const char *s, int c){
    const char *last = NULL;
    do {
        if (*s == (char)c) last = s;
    } while (*s++);
    return (char*)last;
}

char* strpbrk(const char *s, const char *accept){
    for (; *s; s++){
        if (strchr(accept, *s)) return (char*)s;
    }
    return NULL;
}

size_t strspn(const char *s, const char *accept){
    size_t n = 0;
    while (*s && strchr(accept, *s++)) n++;
    return n;
}

size_t strcspn(const char *s, const char *reject){
    size_t n = 0;
    while (*s){
        if (strchr(reject, *s++)) return n;
        n++;
    }
    return n;
}

char* strstr(const char *haystack, const char *needle){
    size_t n = strlen(needle);
    while (*haystack){
        if (0 == strncmp(haystack, needle, n)) return (char*)haystack;
        haystack++;
    }
    return NULL;
}

int memcmp(const void *ptr1, const void *ptr2, size_t n){
    const unsigned char *p1 = ptr1;
    const unsigned char *p2 = ptr2;
    while (n > 0 && *p1 == *p2){
        p1++;
        p2++;
        n--;
    }
    if (n == 0) return 0;
    return cmp_uchar(p1, p2);
}

void* memcpy(void *dest, const void *src, size_t n){
    char *d = dest;
    const char *s = src;

    // Assert that the memory regions do not overlap
    assert((s > d + n) || (d > s + n));

    while (n--) *d++ = *s++;
    return dest;
}

void* memmove(void *dest, const void *src, size_t n){
    char *d = dest;
    const char *s = src;
    if (d < s){
        while (n--) *d++ = *s++;
    }else{
        d += n;
        s += n;
        while (n--) *--d = *--s;
    }
    return dest;
}

void* memset(void *dest, int c, size_t n){
    unsigned char *d = dest;
    while (n--) *d++ = (unsigned char)c;
    return dest;
}

void* memchr(const void *ptr, int value, size_t n){
    const unsigned char *p = ptr;
    while (n-- && *p != (unsigned char)value) p++;
    if (n == 0) return NULL;
    return (void *)p;
}

int char2int(char c){
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'z') return c - 'a' + 10;
    if (c >= 'A' && c <= 'Z') return c - 'A' + 10;
    return -1;
}

// TODO make stdlib.h tests, where this function actually belongs to
long long strtoll(const char *s, char **endptr, int base){
    long long result = 0;
    int is_negative = 0;

    if (*s == '-'){
        is_negative = 1;
        s++;
    }

    // Auto-detect base
    if (base == 0){
        if (*s == '0'){
            s++;
            if (*s == 'x' || *s == 'X'){
                base = 16;
                s++;
            }else{
                base = 8;
            }
        }else{
            base = 10;
        }
    }

    while (*s){
        int digit = char2int(*s);

        if (digit < 0 || digit >= base) break;

        // TODO check overflow and set errno = ERANGE
        result = result * base + digit;
        s++;
    }

    // TODO how to indicate error when there were no (valid) digits?

    // TODO what should the value of endptr be in case of errors?
    if (endptr){
        *endptr = (char*)s;
    }

    if (is_negative){
        // TODO check overflow and set errno = ERANGE
        result = -result;
    }
    return result;
}