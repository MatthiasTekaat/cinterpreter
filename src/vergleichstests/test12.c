// Bezieht sich auf folgenden Test in der Tabelle der Vergleichstests in der schriftlichen Arbeit:
// Speicherzugriffsfehler wie zuvor (gemeint ist Test 11) beschrieben mit dem Unterschied, dass nun der Zeiger
// auf ein Array zwischen 3 Funktionen weitergereicht wird

#include <stdio.h>
#include <stdlib.h>

void foo(int **array){
	int array1[3] = {1,1,1};
	int array2[3] = {2,2,2};
	
	*array = array1;
}

void bar(int *array){
	int initialized[6] = {6,66,666,6666,66666,666666};
	
	for(int i=0; i<3; i++){
		int value = array[i];
		printf("%i", value);
	}
}

int main() {
	int *array;
	foo(&array);
	bar(array);
	
	return 0;
}	