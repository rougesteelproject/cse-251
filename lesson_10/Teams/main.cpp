/*
Course: CSE 251
File: team1.cpp

Instructions:

This program will process a list of integers and display which ones are prime.

TODO
- Convert this program to use N pthreads.
- each thread will process 1/N of the array of numbers.
- Create any functions you need
*/

#include <cstdlib>
#include <iostream>
#include <pthread.h>

#ifdef _WIN32
#include <io.h>
#else
#include <unistd.h>
#endif

#include <pthread.h>
#include <time.h>

using namespace std;

#define NUMBERS 100

struct args {
  int *array;
  int start;
  int end;
};

// ----------------------------------------------------------------------------
int isPrime(int number) {
  if (number <= 3 && number > 1)
    return 1; // as 2 and 3 are prime
  else if (number % 2 == 0 || number % 3 == 0)
    return 0; // check if number is divisible by 2 or 3
  else {
    for (unsigned int i = 5; i * i <= number; i += 6) {
      if (number % i == 0 || number % (i + 2) == 0)
        return 0;
    }
    return 1;
  }
}

// ----------------------------------------------------------------------------

// ----------------------------------------------------------------------------
void findPrimes(void *record) {
  cout << endl << "Starting findPrimes" << endl;

  // Get the structure used to pass arguments
  struct args *arguments = (struct args *)record;

  // Loop through the array looking for prime numbers
  for (int i = arguments->start; i < arguments->end; i++) {
    if (isPrime(arguments->array[i]) == 1) {
      cout << arguments->array[i] << endl;
    }
  }

  return;
}
// ----------------------------------------------------------------------------

void *isPrimeThreaded(void *record) {
  struct args *arguments = (struct args *)record;

  for (int i = arguments->start; i < arguments->end; i++) {
    if (isPrime(arguments->array[i]) == 1) {
      cout << arguments->array[i] << endl;
    }
  }
  return NULL;
}

void findThreadedPrimes(void *record) {
  cout << endl << "Starting findThreadedPrimes" << endl;

  struct args *arguments = (struct args *)record;

  // Do threading here
  pthread_t threads[10];

  for (int i = 0; i < 10; i++) {
    pthread_create(&threads[i], NULL, &isPrimeThreaded, &arguments);
  }

  for (int i = 0; i < 10; ++i) {
    pthread_join(threads[i], NULL);
  }
}

// ----------------------------------------------------------------------------
int main() {
  srand(time(0));

  // Create the array of numbers and assign random values to them
  int arrayValues[NUMBERS];
  for (int i = 0; i < NUMBERS; i++) {
    arrayValues[i] = rand() % 1000000000;
    cout << arrayValues[i] << ", ";
  }
  cout << endl;

  // Create structure that will be used to pass the array and the
  // start of end of the array to another function
  struct args rec = {arrayValues, 0, NUMBERS - 1};

  // Find the primes in the array
  // findPrimes(&rec);
  findThreadedPrimes((void *)&rec);

  return 0;
}