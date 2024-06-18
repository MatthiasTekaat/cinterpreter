// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Zugriff auf Pointer, dessen Speicher bereits freigegeben wurde, wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int *q = malloc(sizeof(int));
	*q = 6;
	free(q);
	printf("%d", *q);
	
	return 0;
}	