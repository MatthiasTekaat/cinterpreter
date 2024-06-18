#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

typedef struct Node Node;

struct Node {
    int data;
    Node *next;
};

Node* create_node(int data) {
    Node *node = (Node*)malloc(sizeof(Node));
    node->data = data;
    node->next = NULL;
    return node;
}

void print_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
}

Node* prepend(Node *head, int data) {
    Node *new_head = create_node(data);
    new_head->next = head;
    return new_head;
}

void free_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        Node *next = current->next;
        free(current);
        current = next;
    }
}

int main() {
    Node *head = NULL;

    int values[9] = {5, 6, 2, 9, 5, 1, 4, 1, 3};

    size_t length = sizeof(values) / sizeof(int);

    for (size_t i = 0; i < length; i++) {
        head = prepend(head, values[i]);
    }

    print_list(head);

    free_list(head);

    return 0;
}
