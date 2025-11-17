/******************************************************************************

While loop


*******************************************************************************/
#include <stdio.h>
int main ()
{
/* local variable definition */
int a = 10; //loop index

/* while loop execution */
printf("while loop execution");
while( a < 20 )
{
printf("value of a: %d\n", a);
a++;
}

printf("\n");
printf("For loop execution\n");
for(a=10;a<20;a++)
{
    printf("for looping value of a: %d\n", a);
}

printf("\n");
printf("do..while loop execution\n");
do
{
printf("value of a: %d\n", a);
a++;
}while( a < 20 );




return 0;
} 
