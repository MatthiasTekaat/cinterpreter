// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Division durch Null wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int a=18;
	int b=0;
	double c=a/b;
	printf("%d", c);
	
	return 0;
}	