// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Schreibzugriff außerhalb des Speicherbereichs eines Arrays wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int intArray[3] = {1,3,9};
	intArray[3] = 11;
	
	return 0;
}	