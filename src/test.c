int *ptr;
int *ptr1=NULL;
int arr12[2][3];
int hh;

int *q;

int arr[2][3] = {{1, 2, 3},{4, 5, 6}};
int myNumbers[4] = {25, 50, 75, 100};



int** ptr1;
int c;

struct my_struct {
    int i;
    int abi[3];
    char c;
    float f;
    char s[30];
};






int a=0;
int b=1;
int t=(3+2+4)*2*b;


//Ebene 0
int test(int a){
    if (ptr1 == NULL){
        ptr1 = &b;
    }
    int* ptr;
    //free(ptr);
    ptr = malloc(2 * sizeof(size_t));
    ptr[0] = b;
    //int zzzz =5/0;
    //q = malloc(sizeof(int));
    q=&b;
    *q=6;

    int q1 = *(myNumbers+1);
    int q2 = myNumbers[1];


    c=6;
    int b=0;

    //ptr[1] = 7;
    int i=1;
    while(i <= 100) {
        printf("Zahl %d und Quadrat der Zahl: %d \n", i,i*i);
        i++;
        if (i==5){
            break;
        }
    }
    //int j=1;
    for(int j=0; j<20; j++) {
        if (j == 3){
            continue;
        }
	    printf("Zahl %d\n", j+1);


	    if (j == 10){
            break;
        }
    }
    return a*b;
}

int main() {
    arr12[1][1]=5;
    int b = arr12[1][1];
    q = malloc(sizeof(int));
    *q=6;

    struct my_struct example_struct = {1, {5,6,7},'A', 3.14, "Hello World"};
    struct my_struct z1;
    example_struct.i=5;
    struct my_struct instanz;
    struct my_struct *zeiger = &instanz;
    zeiger->i=5;
    int r = zeiger->i;



    z1.abi[1]=5;
    int e = example_struct.i;
    int q1 = *(myNumbers+1+2);

    *(myNumbers+2)=5;
    myNumbers[1]=10;

    arr[1][2] = 99;
    int q3 = arr[1][2];
    int x = 5;
    //printf("%d\\n", x);
    int j =test(7);
    return x*5;
}

//int test(*a){
//Ebene 1a
//a=5;
//}

//int test1(){
//Ebene 1b (Kind von Ebene 0)
//test(&b);
//}

