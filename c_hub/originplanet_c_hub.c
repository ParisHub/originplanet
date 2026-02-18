#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int parse_simple_addition(const char *expr, long *out_value) {
    const char *plus;
    char left_buf[64];
    char right_buf[64];
    char *end_ptr;
    long left;
    long right;
    size_t left_len;
    size_t right_len;

    if (!expr || !out_value) {
        return 0;
    }

    plus = strchr(expr, '+');
    if (!plus) {
        return 0;
    }

    left_len = (size_t)(plus - expr);
    right_len = strlen(plus + 1);

    if (left_len == 0 || right_len == 0 || left_len >= sizeof(left_buf) || right_len >= sizeof(right_buf)) {
        return 0;
    }

    memcpy(left_buf, expr, left_len);
    left_buf[left_len] = '\0';
    memcpy(right_buf, plus + 1, right_len);
    right_buf[right_len] = '\0';

    left = strtol(left_buf, &end_ptr, 10);
    if (*end_ptr != '\0') {
        return 0;
    }

    right = strtol(right_buf, &end_ptr, 10);
    if (*end_ptr != '\0') {
        return 0;
    }

    *out_value = left + right;
    return 1;
}

static void print_usage(void) {
    fprintf(stderr, "Usage: originplanet_c_hub --eval <expression>\n");
    fprintf(stderr, "Example: originplanet_c_hub --eval 2+3\n");
}

int main(int argc, char **argv) {
    long result = 0;
    const char *expression = NULL;

    if (argc == 3 && strcmp(argv[1], "--eval") == 0) {
        expression = argv[2];
    } else {
        print_usage();
        return 2;
    }

    if (!parse_simple_addition(expression, &result)) {
        fprintf(stderr, "Unsupported expression: %s\n", expression);
        return 3;
    }

    printf("%ld\n", result);
    return 0;
}
