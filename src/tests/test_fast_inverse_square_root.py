from interpreter import interpret
import unittest

# https://en.wikipedia.org/wiki/Fast_inverse_square_root#Overview_of_the_code
class TestFastInverseSquareRoot(unittest.TestCase):
    def test_fast_inverse_square_root(self):
        code = """
        #include <stdint.h>
        #include <stdio.h>

        float q_rsqrt(float number){
            uint32_t i;
            float x2, y;
            const float threehalfs = 1.5F;

            x2 = number * 0.5F;
            y  = number;
            i  = * ( uint32_t * ) &y;
            i  = 0x5f3759df - ( i >> 1 );
            y  = * ( float * ) &i;
            y  = y * ( threehalfs - ( x2 * y * y ) );

            return y;
        }

        int main(){
            printf("%.10f\\n", q_rsqrt(2.0));
            return 0;
        }
        """
        
        result, stdout, _ = interpret(code)

        self.assertEqual(result, 0)

        expected = b'0.7069300413\n'

        self.assertEqual(stdout, expected)

        print(stdout)


if __name__ == "__main__":
    unittest.main()
 
 
