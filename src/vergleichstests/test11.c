// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Beim Zugriff über einen Zeiger auf ein Array in einer anderen Funktion (lokaler Scope, welcher nach Beendigung der
// Funktion gelöscht sein sollte) wird als Speicherzugriffsfehler erkannt

#include <stdio.h>
#include <stdlib.h>

void foo(char **string){
	char local[] = "Hello, World!";
	*string = local;
}

int main() {
	char *string;
	foo(&string);
	
	printf("String content: %s", string);
	
	return 0;
}	