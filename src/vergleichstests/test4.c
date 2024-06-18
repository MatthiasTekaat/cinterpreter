// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Ungültige Konvertierung eines Pointers (der Pointer wurde auf einen falschen Datentyp konveriert) wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int *intPtr;
	int *intPtr2 = 3;
	intPtr = (double *)intPtr2;
	
	return 0;
}	