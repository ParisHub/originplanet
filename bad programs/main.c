#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int helloc(void) {
    printf("Hello, C.\n");
    return 0;
}

int createHtml(void) {
    FILE *file = fopen("main.html", "w");
    if (file == NULL) {
        printf("Failed to create file\n");
        return 1;
    }
    fprintf(file, 
        "<!DOCTYPE html>\n"
        "<html lang=\"de\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "    <title>HK</title>\n"
        "</head>\n"
        "<body>\n"
        "    <h1>Welcome</h1>\n"
        "</body>\n"
        "</html>\n"
    );
}

int main(int argc, char* argv[]) {
    createHtml();
    
    if (strcmp( argv[1], "helloc") == 0){
        helloc();
        return 0;
    } else if (strcmp( argv[1], "chtml") == 0){
        createHtml();
        return 0;
    }

    system("pause");
    return 0;
}





