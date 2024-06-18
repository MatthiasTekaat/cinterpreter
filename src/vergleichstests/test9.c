// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Shift in das Vorzeichen-Bit eines vorzeichenbehafteten Integers wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int a = -2147483648;
	a--;

	printf("%d", a);
	
	return 0;
}	