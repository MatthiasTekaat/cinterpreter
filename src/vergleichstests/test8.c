// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Überschreiten des Wertebereichs eines Datentyps (z.B. Integer-Overflow, bei dem der Wertebereich
// im Positiven bis 2.147.483.647 geht) wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int a = 2147483647;
	int b = 2;
	int result = a+b;
	printf("%d", result);
	
	return 0;
}	