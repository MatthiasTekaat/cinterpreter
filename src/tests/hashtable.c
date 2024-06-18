#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

typedef struct Node {
    int key;
    int value;
    struct Node *next;
} Node;

typedef struct {
    Node **buckets;
    size_t num_buckets;
    size_t size;
} HashTable;

void hashtable_init(HashTable *table, size_t num_buckets){
    table->buckets = malloc(num_buckets * sizeof(Node*));
    for (size_t i = 0; i < num_buckets; i++){
        table->buckets[i] = NULL;
    }
    table->num_buckets = num_buckets;
    table->size = 0;
}

void hashtable_free(HashTable *table){
    for (size_t i = 0; i < table->num_buckets; i++){
        Node *node = table->buckets[i];
        while (node){
            Node *next = node->next;
            free(node);
            node = next;
        }
    }
    free(table->buckets);
}

Node *hashtable_find(HashTable *table, int key){
    if (table->size == 0) return NULL;
    size_t index = key % table->num_buckets;
    Node *node = table->buckets[index];
    while (node){
        if (node->key == key) return node;
        node = node->next;
    }
    return NULL;
}

Node* new_node(int key, int value, Node *next){
    Node *node = malloc(sizeof(Node));
    node->key = key;
    node->value = value;
    node->next = next;
    return node;
}

bool hashtable_insert(HashTable *table, int key, int value);

void hashtable_resize(HashTable *table, size_t new_num_buckets){
    HashTable new_table;
    hashtable_init(&new_table, new_num_buckets);
    for (size_t i = 0; i < table->num_buckets; i++){
        Node *node = table->buckets[i];
        while (node){
            hashtable_insert(&new_table, node->key, node->value);
            node = node->next;
        }
    }
    hashtable_free(table);
    *table = new_table;
}

bool hashtable_insert(HashTable *table, int key, int value){
    if (table->size >= table->num_buckets){
        size_t new_num_buckets = table->num_buckets * 9 / 8 + 1;
        hashtable_resize(table, new_num_buckets);
    }

    // table->num_buckets is always greater than 0 at this point
    size_t index = key % table->num_buckets;
    Node *node = table->buckets[index];
    while (node){
        // If the key is already in the table, overwrite the value
        if (node->key == key){
            node->value = value;
            return false;
        }
        node = node->next;
    }
    table->buckets[index] = new_node(key, value, table->buckets[index]);
    table->size++;
    return true;
}

bool hashtable_remove(HashTable *table, int key){
    if (table->size == 0) return false;
    size_t index = key % table->num_buckets;
    Node *node = table->buckets[index];
    Node *prev = NULL;
    while (node){
        if (node->key == key){
            if (prev){
                prev->next = node->next;
            } else {
                table->buckets[index] = node->next;
            }
            free(node);
            table->size--;
            return true;
        }
        prev = node;
        node = node->next;
    }
    return false;
}

void test_simple(){
    HashTable table;
    hashtable_init(&table, 10);
    assert(table.size == 0);
    assert(hashtable_find(&table, 0) == NULL);
    assert(hashtable_find(&table, 1) == NULL);
    hashtable_insert(&table, 1, 10);
    assert(table.size == 1);
    assert(hashtable_find(&table, 0) == NULL);
    assert(hashtable_find(&table, 1)->value == 10);
    hashtable_insert(&table, 2, 20);
    assert(table.size == 2);
    assert(hashtable_find(&table, 0) == NULL);
    assert(hashtable_find(&table, 1)->value == 10);
    assert(hashtable_find(&table, 2)->value == 20);
    hashtable_insert(&table, 1, 1);
    assert(table.size == 2);
    assert(hashtable_find(&table, 0) == NULL);
    assert(hashtable_find(&table, 1)->value == 1);
    assert(hashtable_find(&table, 2)->value == 20);
    assert(hashtable_remove(&table, 0) == false);
    assert(hashtable_remove(&table, 1) == true);
    assert(hashtable_remove(&table, 1) == false);
    assert(hashtable_find(&table, 0) == NULL);
    assert(hashtable_find(&table, 1) == NULL);
    assert(hashtable_find(&table, 2)->value == 20);
    assert(hashtable_remove(&table, 2) == true);
    assert(hashtable_find(&table, 0) == NULL);
    assert(hashtable_find(&table, 1) == NULL);
    assert(hashtable_find(&table, 2) == NULL);
    assert(table.size == 0);
    hashtable_free(&table);
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

typedef struct {
    int *keys;
    int *values;
    size_t size;
    size_t capacity;
} ArrayTable;

void arraytable_init(ArrayTable *table){
    table->keys = NULL;
    table->values = NULL;
    table->size = 0;
    table->capacity = 0;
}

void arraytable_free(ArrayTable *table){
    free(table->keys);
    free(table->values);
}

void arraytable_reserve(ArrayTable *table, size_t capacity){
    if (table->capacity < capacity){
        table->keys = realloc(table->keys, capacity * sizeof(int));
        table->values = realloc(table->values, capacity * sizeof(int));
        table->capacity = capacity;
    }
}

size_t arraytable_find(ArrayTable *table, int key){
    for (size_t i = 0; i < table->size; i++){
        if (table->keys[i] == key) return i;
    }
    return table->size;
}

bool arraytable_insert(ArrayTable *table, int key, int value){
    if (table->size >= table->capacity){
        size_t new_capacity = table->capacity * 5 / 4 + 1;
        arraytable_reserve(table, new_capacity);
    }
    size_t index = arraytable_find(table, key);
    // If the key is already in the table, overwrite the value
    if (index < table->size){
        table->values[index] = value;
        return false;
    } else {
        table->keys[table->size] = key;
        table->values[table->size] = value;
        table->size++;
        return true;
    }
}

bool arraytable_remove(ArrayTable *table, int key){
    size_t index = arraytable_find(table, key);
    if (index < table->size){
        table->keys[index] = table->keys[table->size - 1];
        table->values[index] = table->values[table->size - 1];
        table->size--;
        return true;
    } else {
        return false;
    }
}

void test_random(size_t n){
    HashTable table;
    hashtable_init(&table, 0);

    ArrayTable arraytable;
    arraytable_init(&arraytable);

    for (size_t i = 0; i < n; i++){
        int key = (int)(my_rand() % 10);
        int value = (int)(my_rand() % 100);

        switch (my_rand() % 3){
            case 0:{
                bool result1 = hashtable_insert(&table, key, value);
                bool result2 = arraytable_insert(&arraytable, key, value);
                assert(result1 == result2);
                break;
            }
            case 1:{
                bool result1 = hashtable_remove(&table, key);
                bool result2 = arraytable_remove(&arraytable, key);
                assert(result1 == result2);
                break;
            }
            case 2:{
                Node *node = hashtable_find(&table, key);
                size_t index = arraytable_find(&arraytable, key);
                if (node){
                    assert(index < arraytable.size);
                    assert(node->value == arraytable.values[index]);
                } else {
                    assert(index == arraytable.size);
                }
                break;
            }
            assert(table.size == arraytable.size);
        }

        for (size_t i = 0; i < arraytable.size; i++){
            Node *node = hashtable_find(&table, arraytable.keys[i]);
            assert(node != NULL);
            assert(node->value == arraytable.values[i]);
        }
    }

    hashtable_free(&table);
    arraytable_free(&arraytable);
}

int main(){
    test_simple();
    for (size_t n = 0; n < 20; n++){
        test_random(n);
    }
    return 0;
}