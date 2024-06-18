
            typedef struct Duck Duck;

            struct Duck {
                int feet;
                int beak;
                int wings;
            };

            int main(){
                Duck ducks[2];
                Duck *daisy = &ducks[1];

                daisy->feet = 2;
                daisy->beak = 1;
                daisy->wings = 2;

                return daisy->wings;
            }
            