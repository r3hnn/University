#include <stdio.h>

int main()
{
    int n, i, j;

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    int pid[n], bt[n], pr[n], waiting_time[n];

    // Input
    for(i = 0; i < n; i++)
    {
        pid[i] = i + 1;

        printf("Enter the burst time: ");
        scanf("%d", &bt[i]);

        printf("Enter the priority: ");
        scanf("%d", &pr[i]);
    }

    // Sorting based on priority
    for(i = 0; i < n - 1; i++)
    {
        for(j = i + 1; j < n; j++)
        {
            if(pr[i] > pr[j])
            {
                int temp;

                // Swap priority
                temp = pr[i];
                pr[i] = pr[j];
                pr[j] = temp;

                // Swap burst time
                temp = bt[i];
                bt[i] = bt[j];
                bt[j] = temp;

                // Swap process ID
                temp = pid[i];
                pid[i] = pid[j];
                pid[j] = temp;
            }
        }
    }

    // Waiting time calculation
    waiting_time[0] = 0;

    for(i = 1; i < n; i++)
    {
        waiting_time[i] = waiting_time[i - 1] + bt[i - 1];
    }

    // Output
    printf("\nProcess\tBT\tPriority\tWT\n");

    int total = 0;

    for(i = 0; i < n; i++)
    {
        printf("P%d\t%d\t%d\t\t%d\n",
               pid[i],
               bt[i],
               pr[i],
               waiting_time[i]);

        total += waiting_time[i];
    }

    printf("The average waiting time is: %.2f\n",
           (float)total / n);

    return 0;
}