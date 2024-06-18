from interpreter import interpret
import unittest

with open("strings.c") as f:
    strings_code = f.read()

def make_main(code):
    return strings_code + """
    #include <assert.h>

    int main() {
        %s
    }
    """ % code

class TestStrings(unittest.TestCase):

    def test_strlen(self):
        code = """
        assert(strlen("") == 0);
        assert(strlen("a") == 1);
        assert(strlen("hello") == 5);

        const char *s = "hello";
        return (int)strlen(s);
        """
        result, _, _ = interpret(make_main(code))

        self.assertEqual(result, 5)

    def test_strlen_null(self):
        code = """
        return strlen(NULL);
        """
        with self.assertRaises(NullPointerException):
            interpret(make_main(code))

    def test_strcmp(self):
        code = """
        assert(strcmp("", "") == 0);
        assert(strcmp("a", "a") == 0);
        assert(strcmp("hello", "hello") == 0);

        assert(strcmp("a", "b") < 0);
        assert(strcmp("a", "ab") < 0);
        assert(strcmp("a", "aa") < 0);
        assert(strcmp("aa", "ab") < 0);

        assert(strcmp("b", "a") > 0);
        assert(strcmp("ab", "a") > 0);
        assert(strcmp("aa", "a") > 0);
        assert(strcmp("ab", "aa") > 0);

        const char *s = "hello";
        return strcmp(s, "hello");
        """
        result, _, _ = interpret(make_main(code))

        self.assertEqual(result, 0)
    
    def test_strncmp(self):
        code = """
        assert(strncmp("", "", 0) == 0);
        assert(strncmp("a", "a", 0) == 0);
        assert(strncmp("hello", "hello", 0) == 0);

        assert(strncmp("a", "b", 1) < 0);
        assert(strncmp("a", "ab", 1) == 0);
        assert(strncmp("a", "aa", 1) == 0);
        assert(strncmp("aa", "ab", 2) < 0);

        assert(strncmp("b", "a", 1) > 0);
        assert(strncmp("ab", "a", 1) == 0);
        assert(strncmp("aa", "a", 1) == 0);
        assert(strncmp("ab", "aa", 2) > 0);

        const char *s = "hello";
        return strncmp(s, "hello", 5);
        """
        result, _, _ = interpret(make_main(code))

        self.assertEqual(result, 0)

    def test_strcpy(self):
        code = """
        char s[10];
        char *ptr = strcpy(s, "he");
        assert(ptr == s);
        assert(strcmp(s, "he") == 0);
        ptr = strcpy(s + 2, "llo");
        assert(ptr == s + 2);
        assert(strcmp(s, "hello") == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)
    
    def test_strcar(self):
        code = """
        char s[12] = "hello";
        char *ptr = strcat(s, " world");
        assert(ptr == s);
        assert(strcmp(s, "hello world") == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)
    
    def test_strchr(self):
        code = """
        char s[5] = "abcd";
        char *ptr = strchr(s, 'c');
        assert(ptr == s + 2);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_strrchr(self):
        code = """
        char s[6] = "abcda";
        char *ptr = strrchr(s, 'a');
        assert(ptr == s + 4);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_strpbrk(self):
        code = """
        char s[5] = "abcd";
        char *ptr = strpbrk(s, "xyzcd");
        assert(ptr == s + 2);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_strspn(self):
        code = """
        char s[5] = "abcd";
        assert(strspn(s, "abc") == 3);
        assert(strspn(s, "xyz") == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_strcspn(self):
        code = """
        char s[5] = "abcd";
        assert(strcspn(s, "xyzd") == 3);
        assert(strcspn(s, "abc") == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_strstr(self):
        code = """
        char s[5] = "abcd";
        char *ptr = strstr(s, "bc");
        assert(ptr == s + 1);
        ptr = strstr(s, "xyz");
        assert(ptr == NULL);
        ptr = strstr(s, "");
        assert(ptr == s);
        char *tmp = "";
        ptr = strstr(tmp, "");
        assert(ptr == tmp);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_memcmp(self):
        code = """
        char s1[10] = "ababbabab";
        char s2[10] = "baabbabab";
        assert(memcmp(s1, s2, 1) < 0);
        assert(memcmp(s2, s1, 1) > 0);
        assert(memcmp(s1 + 1, s2, 2) == 0);
        assert(memcmp(s1 + 2, s2 + 2, 7) == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_memcpy(self):
        code = """
        char s1[10] = "ababbabab";
        char s2[10];
        char *ptr = memcpy(s2, s1, 10);
        assert(ptr == s2);
        assert(memcmp(s1, s2, 10) == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_memcpy_overlap(self):
        code = """
        char s[] = "aaaaaaaa";
        memcpy(s + 1, s, 1);
        return 0;
        """
        with self.assertRaises(AssertionError):
            interpret(make_main(code))

    def test_memmove(self):
        code = """
        char s[5] = "abcd";
        char *ptr = memmove(s, s + 1, 3);
        assert(ptr == s);
        assert(strcmp(s, "abcd"));
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_memset(self):
        code = """
        char s[5] = "abcd";
        char *ptr = memset(s, 'a', 4);
        assert(ptr == s);
        assert(strcmp(s, "aaaa") == 0);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)
    
    def test_memchr(self):
        code = """
        char s[5] = "abcd";
        char *ptr = memchr(s, 'c', 4);
        assert(ptr == s + 2);
        return 0;
        """
        result, _, _ = interpret(make_main(code))
        
        self.assertEqual(result, 0)

    def test_strtoll(self):
        code = """
        assert(strtoll("0", NULL, 10) == 0);
        assert(strtoll("-0x10", NULL, 0) == -16);
        assert(strtoll("0XABC", NULL, 0) == 2748);
        assert(strtoll("Z", NULL, 36) == 35);
        assert(strtoll("0123", NULL, 0) == 83);
        char s[] = "12345abc";
        char *endptr = NULL;
        assert(strtoll(s, &endptr, 10) == 12345);
        assert(endptr == s + 5);
        return 0;
        """
        result, _, _ = interpret(make_main(code))

        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
