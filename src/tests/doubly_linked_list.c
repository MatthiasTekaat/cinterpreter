#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>

typedef struct Node Node;

struct Node {
    int data;
    Node *prev;
    Node *next;
};

typedef struct {
    Node *head;
    Node *tail;
    size_t size;
} List;

Node* create_node(int data, Node *prev, Node *next) {
    Node *node = (Node*)malloc(sizeof(Node));
    node->data = data;
    node->prev = prev;
    node->next = next;
    return node;
}

List* create_list() {
    List *list = (List*)malloc(sizeof(List));
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
    return list;
}

void print_list(List *list) {
    Node *current = list->head;
    while (current != NULL) {
        printf("%d\n", current->data);
        current = current->next;
    }
    printf("\n");
}

void prepend(List *list, int data) {
    Node *new_head = create_node(data, NULL, list->head);
    if (list->head != NULL) {
        list->head->prev = new_head;
    }
    list->head = new_head;
    if (list->tail == NULL) {
        list->tail = new_head;
    }
    list->size++;
}

void append(List *list, int data) {
    Node *new_tail = create_node(data, list->tail, NULL);
    if (list->tail != NULL) {
        list->tail->next = new_tail;
    }
    list->tail = new_tail;
    if (list->head == NULL) {
        list->head = new_tail;
    }
    list->size++;
}

void free_list(List *list) {
    Node *current = list->head;
    while (current != NULL) {
        Node *next = current->next;
        free(current);
        current = next;
    }
    free(list);
}

void remove_node(List *list, Node *node) {
    if (node->prev != NULL) {
        node->prev->next = node->next;
    } else {
        list->head = node->next;
    }
    if (node->next != NULL) {
        node->next->prev = node->prev;
    } else {
        list->tail = node->prev;
    }
    free(node);
    list->size--;
}

void remove_head(List *list) {
    if (list->head != NULL) {
        remove_node(list, list->head);
    }
}

void remove_tail(List *list) {
    if (list->tail != NULL) {
        remove_node(list, list->tail);
    }
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

int main() {
    List *list = create_list();

    append(list, 2);
    prepend(list, 1);
    append(list, 3);

    print_list(list);

    Node *node = list->head->next;
    remove_head(list);
    remove_tail(list);
    remove_node(list, node);

    print_list(list);

    free_list(list);

    for (int k = 0; k < 100; k++){
        list = create_list();

        for (int i = 0; i < 100; i++){
            switch (my_rand() % 5){
                case 0:
                    prepend(list, my_rand());
                    break;
                case 1:
                    append(list, my_rand());
                    break;
                case 2:
                    remove_head(list);
                    break;
                case 3:
                    remove_tail(list);
                    break;
                case 4:
                    if (list->size > 0){
                        // choose random node
                        int index = my_rand() % list->size;
                        Node *node = list->head;
                        for (int j = 0; j < index; j++){
                            node = node->next;
                        }
                        remove_node(list, node);
                    }
                    break;
            }
        }

        print_list(list);
        
        free_list(list);
    }

    return 0;
}
