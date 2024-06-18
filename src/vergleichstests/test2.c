// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Freigeben von bereits freigegebenem Speicherbereich wird erkannt („Double-free“)

#include <stdio.h>
#include <stdlib.h>

int main() {
	int *q = malloc(sizeof(int));
	*q = 6;
	
	free(q);
	free(q);
	
	return 0;
}	