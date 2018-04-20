#include <stdio.h>
#include <stdlib.h>
#include <sys/fcntl.h>
#include <unistd.h>
#include <string.h>
#include <strings.h>

char *gen_rand_string(int len)
{
	int i;
	char buf[4096];
	char tab[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ ";
	for(i = 0 ; i < len; i ++){
		char c = tab[rand() % (sizeof(tab)-1) ];
		buf[i] = c;
	}
	buf[len] = 0;

	char *s = calloc(len+1, 1);
	memcpy(s, buf, len+1);
	return s;
}



int main(){
	int seed;
	scanf("%x", &seed);
	srand(seed);

	for(int i = 0; i < 100; i++){
		char *p = gen_rand_string(100);
		int flag = 1;
		for(int j = 0; j < 10; j++){
			if(p[j] >= 'A' && p[j] <= 'Z'){
				flag = 0;
				break;
			}
		}
		if(flag == 1){
			printf("%d:", i+1);
			for(int j = 0; j < 10; j++){
				printf("%c", p[j]);
			}
			break;
		}
	}
	return 0;
}
