// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Beim Zugriff von zwei hintereinander deklarierten Arrays a und b mit jeweils der Länge 3 werden beim iterieren (über
// eine for-Schleife) über die Grenze von Array a hinaus nicht die Elemente aus b ausgegeben, sondern der
// Speicherzugriffsfehler wird erkannt

#include <stdio.h>
#include <stdlib.h>

int main() {
	int array1[3] = {1,2,3};
	int array2[3] = {4,5,6};
	
	for(int i=0; i<5; i++){
		printf("%i", array1[i]);
	}
	
	return 0;
}	