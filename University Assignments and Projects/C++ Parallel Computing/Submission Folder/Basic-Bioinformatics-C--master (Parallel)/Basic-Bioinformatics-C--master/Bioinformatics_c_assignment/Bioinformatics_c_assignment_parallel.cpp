#include <stdio.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <iostream>
#include <sstream>
#include <omp.h>
#include <vector>
#include <fstream>

int number_bacteria;
char** bacteria_name;
long M, M1, M2;
short code[27] = { 0, 2, 1, 2, 3, 4, 5, 6, 7, -1, 8, 9, 10, 11, -1, 12, 13, 14, 15, 16, 1, 17, 18, 5, 19, 3 };
#define encode(ch)		code[ch-'A']
#define LEN				6
#define AA_NUMBER		20
#define	EPSILON			1e-010

//dougs

//Resets the 'M' Variables back to
void Init()
{
	M2 = 1;
	for (int i = 0; i < LEN - 2; i++) {	// M2 = AA_NUMBER ^ (LEN-2);
		M2 *=     AA_NUMBER;
		M1 = M2 * AA_NUMBER;		// M1 = AA_NUMBER ^ (LEN-1);
		M = M1 *  AA_NUMBER;	        // M  = AA_NUMBER ^ (LEN);
		
		//Results in...
		/*  * M2 : 20
			* M1 : 400
			* M  : 8000

			* M2 : 400
			* M1 : 8000
			* M  : 160000

			* M2 : 8000
			* M1 : 160000
			* M  : 3200000

			* M2 : 160000
			* M1 : 3200000
			* M  : 64000000
			*/
	}
}

class Bacteria
{
private:
	long* vector;
	long* second;
	long one_l[AA_NUMBER];
	long indexs;
	long total;
	long total_l;
	long complement;

	void InitVectors()
	{
		vector = new long[M];
		second = new long[M1];
		memset(vector, 0, M * sizeof(long));
		memset(second, 0, M1 * sizeof(long));
		memset(one_l, 0, AA_NUMBER * sizeof(long));
		total = 0;
		total_l = 0;
		complement = 0;
	}

	// intialise buffer
	void init_buffer(char* buffer)
	{
		complement++;
		indexs = 0;
		for (int i = 0; i<LEN - 1; i++)
		{
			short enc = encode(buffer[i]);
			one_l[enc]++;
			total_l++;
			indexs = indexs * AA_NUMBER + enc;
		}
		second[indexs]++;
	}

	void cont_buffer(char ch)
	{
		short enc = encode(ch);
		one_l[enc]++;
		total_l++;
		long index = indexs * AA_NUMBER + enc;
		vector[index]++;
		total++;
		indexs = (indexs % M2) * AA_NUMBER + enc;
		second[indexs]++;
	}

public:
	long count;
	double* tv;
	long *ti;

	Bacteria(char* filename)
	{
		FILE * bacteria_file = fopen(filename, "r"); //opens parsed file
		InitVectors();

		char ch; //pointer
		while ((ch = fgetc(bacteria_file)) != EOF) //while the pointer is not at the end of the file 
		{
			if (ch == '>') //if the pointer returns '>'
			{
				while (fgetc(bacteria_file) != '\n'); // while pointer does not return '\n'

				char buffer[LEN - 1]; //create a buffer array 
				fread(buffer, sizeof(char), LEN - 1, bacteria_file); //reads the document line 
				init_buffer(buffer); //parse 'buffer' to init_buffer method
			}
			else if (ch != '\n') //else if pointer does not return '\n' 
				cont_buffer(ch); //parse pointer to cont_buffer method
		}

		long total_plus_complement = total + complement;
		double total_div_2 = total * 0.5;
		int i_mod_aa_number = 0;
		int i_div_aa_number = 0;
		long i_mod_M1 = 0;
		long i_div_M1 = 0;

		double one_l_div_total[AA_NUMBER]; 
		for (int i = 0; i<AA_NUMBER; i++)
			one_l_div_total[i] = (double)one_l[i] / total_l;

		double* second_div_total = new double[M1];
		for (int i = 0; i<M1; i++)
			second_div_total[i] = (double)second[i] / total_plus_complement;

		count = 0;
		double* t = new double[M];

		for (long i = 0; i<M; i++)
		{
			double p1 = second_div_total[i_div_aa_number];
			double p2 = one_l_div_total[i_mod_aa_number];
			double p3 = second_div_total[i_mod_M1];
			double p4 = one_l_div_total[i_div_M1];
			double stochastic = (p1 * p2 + p3 * p4) * total_div_2;

			if (i_mod_aa_number == AA_NUMBER - 1)
			{
				i_mod_aa_number = 0;
				i_div_aa_number++;
			}
			else
				i_mod_aa_number++;

			if (i_mod_M1 == M1 - 1)
			{
				i_mod_M1 = 0;
				i_div_M1++;
			}
			else
				i_mod_M1++;

			if (stochastic > EPSILON)
			{
				t[i] = (vector[i] - stochastic) / stochastic;
				count++;
			}
			else
				t[i] = 0;
		}

		delete second_div_total;
		delete vector;
		delete second;

		tv = new double[count];
		ti = new long[count];

		int pos = 0;

		for (long i = 0; i<M; i++)
		{
			if (t[i] != 0)
			{
				tv[pos] = t[i];
				ti[pos] = i;
				pos++;
			}
		}
		delete t;

		fclose(bacteria_file);
	}
};

	//Reads the .txt file and adds names of bacterias in the text file to a string array bacteria_name[] 
void ReadInputFile(char* input_name)
{
	FILE* input_file = fopen(input_name, "r");
	fscanf(input_file, "%d", &number_bacteria);
	bacteria_name = new char*[number_bacteria]; //Create a list of bacteria names 

	for (long i = 0; i<number_bacteria; i++) // For # of bacteria'
	{
		bacteria_name[i] = new char[20]; //add a new char[20] field to bacteria_name[i]
		fscanf(input_file, "%s", bacteria_name[i]); //Reads .txt and adds string of bacteria name to bacteria_name[i]
		strcat(bacteria_name[i], ".faa"); //Concatenates parameters
	}
	fclose(input_file);
}

double CompareBacteria(Bacteria* b1, Bacteria* b2)
{
	double correlation = 0; //correlation means comparrison value
	double vector_len1 = 0;
	double vector_len2 = 0;
	long p1 = 0;
	long p2 = 0;
	while (p1 < b1->count && p2 < b2->count)
	{
		long n1 = b1->ti[p1];
		long n2 = b2->ti[p2];
		if (n1 < n2)
		{
			double t1 = b1->tv[p1];
			vector_len1 += (t1 * t1);
			p1++;
		}
		else if (n2 < n1)
		{
			double t2 = b2->tv[p2];
			p2++;
			vector_len2 += (t2 * t2);
		}
		else
		{
			double t1 = b1->tv[p1++];
			double t2 = b2->tv[p2++];
			vector_len1 += (t1 * t1);
			vector_len2 += (t2 * t2);
			correlation += t1 * t2;
		}
	}
	while (p1 < b1->count)
	{
		long n1 = b1->ti[p1];
		double t1 = b1->tv[p1++];
		vector_len1 += (t1 * t1);
	}
	while (p2 < b2->count)
	{
		long n2 = b2->ti[p2];
		double t2 = b2->tv[p2++];
		vector_len2 += (t2 * t2);
	}

	return correlation / (sqrt(vector_len1) * sqrt(vector_len2));
}

void CompareAllBacteria()
{
	Bacteria** b = new Bacteria*[number_bacteria]; //creates an array of the class Bacteria b[]
	omp_set_num_threads(17);
#pragma omp parallel
	{
#pragma omp for 
			for (int i = 0; i < number_bacteria; i++)           //for the number of bacteria recognised in the text file...
		{
			printf("load %d of %d\n", i + 1, number_bacteria);  //print to the console a loading message for the next line
			b[i] = new Bacteria(bacteria_name[i]);              //create a new instance of the Bacteria class and add it to the previosuly created array b[]
		}
	}

	//double* storage_sequel = new double[number_bacteria*number_bacteria];
	//double* storage_parallel = new double[number_bacteria*number_bacteria];

	////sequential
	//for (int i = 0; i < number_bacteria - 1; i++) //for the number of bacteria...
	//	for (int j = i + 1; j < number_bacteria; j++) //assess each bacteria against one another 
	//	{
	//		printf("%2d %2d -> ", i, j);
	//		double correlation = CompareBacteria(b[i], b[j]); //compares the provided bacteria' and assigns the comparison value to 'correlation' 
	//		storage_sequel[j-1] = CompareBacteria(b[i], b[j]);
	//		printf("%.20lf\n", correlation); //prints the value of 'correlation' to the screen
	//		
	//	}
	omp_set_num_threads(17);
#pragma omp parallel
	{
#pragma omp for 
		for (int i = 0; i < number_bacteria - 1; i++)                  //for the number of bacteria...
			for (int j = i + 1; j < number_bacteria; j++)              //assess each bacteria against one another 
			{
				double correlation = CompareBacteria(b[i], b[j]);      //compares the provided bacteria' and assigns the comparison value to 'correlation' 			                                                       
				printf("%2d %2d -> %.20lf\n",i, j, correlation);                       //prints the value of 'correlation' to the screen
			}
	}

	//for (int i = 0; i < (number_bacteria*number_bacteria); i++) 
	//{
	//	if (storage_parallel[i] == storage_parallel[i]) {
	//		printf("Id %2d results match\n", i);
	//	}
	//	else 
	//	{
	//		printf("Id %2d results do not match\n", i);
	//	}
	//}
}


int main(int argc, char * argv[])
{
	time_t t1 = time(NULL); //Starts application timer

	Init(); //intialises parameters
	ReadInputFile(argv[1]); //reads the text file and adds bacteria names to an array []
	CompareAllBacteria(); //Creates and instantiates Bacteria() class instances and adds them to the array,
						  //Then compares all instances against each other and ouputs the results

	time_t t2 = time(NULL); //stops application timer
	printf("time elapsed: %d seconds\n", t2 - t1); //outputs elapsed time to user
	int threads = omp_get_max_threads();
	//printf("%d max threads", threads);
	system("pause");

	return 0;
}