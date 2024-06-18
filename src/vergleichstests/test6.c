// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Lesezugriff außerhalb des Speicherbereichs eines Arrays wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int intArray[3] = {1,3,9};
	printf("%d", intArray[3]);
	
	return 0;
}	