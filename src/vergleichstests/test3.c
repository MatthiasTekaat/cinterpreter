// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Verwendung einer definierten, aber nicht initialisierten Variable (kein initialer Wert wurde zugewiesen) wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int a;
	printf("%d", a);
	
	return 0;
}	