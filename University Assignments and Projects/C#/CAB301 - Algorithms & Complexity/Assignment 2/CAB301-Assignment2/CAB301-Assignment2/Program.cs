using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Office.Interop.Excel;
using Excel = Microsoft.Office.Interop.Excel;


namespace CAB301_Assignment2 {
    class Program {
        public static Random rnd = new Random();
        public static int for_loop_counter1 = 0;
        public static int for_loop_counter2 = 0;
        public static int if_loop_counter1 = 0;
        public static int num_smaller_counter = 0;
        public static int num_equal_counter = 0;
        public static int basic_operations = 0;
        public static int array_size = 100;
        public static int data_count = 2;
        public static int time_efficiency = 0;
        public static int test_size = 1000;
        public static int test_count = 0;
        public static float median = 0;
        public static bool brute_force = true;

        public static int[] array = { };
        public static Excel._Worksheet worksheet;
        public static Excel.Application excel;

        static void Main(string[] args) {
            excel = new Excel.Application();
            CreateExcelData();
            //RefreshData();

            // Runs the function a set amount of times
            for (int i = 1; i <= test_size; i++) {
                rnd = new Random();
                array = CreateRandomArray(array_size);
                //array = CreateFunctionalTestArray();
                //array = CreateDescendingArray(array_size);
                //array = CreateAscendingArray(array_size);

                // Increases the test count and resets variables
                int[] array_copy = new int[array_size]; 
                array.CopyTo(array_copy, 0);
                //median = BruteForceMedian(array_copy);
                median = Median(array_copy);
                if (test_count < test_size) {
                    //array_size++;
                    test_count++;
                    RefreshData();
                }
            }

            //Output
            List<int> list = array.ToList();
            if (brute_force == true) {
                Console.WriteLine("Testing for algorithm Brute Force Median");
            } else {
                Console.WriteLine("Testing for algorithm Median");
            }
            Console.WriteLine("Tested array is... ");
            list.ForEach(o => Console.Write("{0}\t", o + ","));
            Console.WriteLine(System.Environment.NewLine + "The array size " + array.Length);
            if (array.Length % 2 == 0) {
                Console.WriteLine("The array size is Even ");
                Array.Sort(array);
                float a = array[array.Length / 2 - 1];
                float b = array[array.Length / 2];
                float c = (a + b) / 2;
                Console.WriteLine("The Median using the algorithm =  " + median);
                Console.WriteLine("The actual median is =  " + c);
            } else {
                Console.WriteLine("The array size is Odd ");
                Console.WriteLine("The Median using the algorithm =  " + median);
                Console.WriteLine("The actual median is =  " + Median(array));
            }
            Console.WriteLine("The number of basic operations performed is " + basic_operations);
            Console.WriteLine("The algorithms time efficiency for this test is " + time_efficiency + "n");
            Console.ReadKey();
        }

        private static int BruteForceMedian(int[] array) {
            // Returns the median value in a given array A of n numbers. This is
            // the kth element, where k = |n/2|, if the array was sorted.
            worksheet = (Excel.Worksheet)excel.ActiveSheet;
            int k = array.Length / 2;
            for (int i = 0; i <= array.Length; i++) {
                int numsmaller = 0;
                int numequal = 0;
                for (int j = 0; j <= array.Length-1; j++) {
                    basic_operations++;
                    if (array[j] < array[i]) {
                        numsmaller++;
                    } else {
                        if (array[j] == array[i]) {
                            numequal++;
                        }
                    }
                } if ((numsmaller < k && k <= (numsmaller + numequal))) {
                    time_efficiency = basic_operations / array_size;
                    // Export to Excel
                    worksheet.Cells[1, 1] = "Basic Operations";
                    worksheet.Cells[1, 2] = "Time Efficiency";
                    worksheet.Cells[1, 3] = "Array Length";
                    worksheet.Cells[data_count, 1] = basic_operations;
                    worksheet.Cells[data_count, 2] = time_efficiency;
                    worksheet.Cells[data_count, 3] = array_size;
                    data_count++;
                    return array[i];
                }
            }
            return 0;
        }

        private static int Median(int[] function_array) {
            // Returns the median value in a given array A of n numbers
            int output;
            worksheet = (Excel.Worksheet)excel.ActiveSheet;
            if (function_array.Length == 1) {
                return function_array[0];
            } else {
                output = Select(function_array, 0, (function_array.Length / 2), function_array.Length - 1);
                time_efficiency = basic_operations / array_size;
                // Export to Excel
                worksheet.Cells[1, 1] = "Basic Operations";
                worksheet.Cells[1, 2] = "Time Efficiency";
                worksheet.Cells[1, 3] = "Array Length";
                worksheet.Cells[data_count, 1] = basic_operations;
                worksheet.Cells[data_count, 2] = time_efficiency;
                worksheet.Cells[data_count, 3] = array_size;
                data_count++;
                return output;
            }
        }

        private static int Select(int[] function_array, int l, int m, int h) {
            // Returns the value at index m in array slice A[l..h], if the slice
            // were sorted into nondecreasing order.
            int pos = Partition(function_array, l, h);
            if (pos == m) {
                return function_array[pos];
            } else if (pos > m) {
                return Select(function_array, l, m, pos - 1);
            } else if (pos < m) {
                return Select(function_array, pos + 1, m, h);
            } else {
                return 0;
            }
        }

        private static int Partition(int[] function_array, int l, int h) {
            // Partitions array slice A[l..h] by moving element A[l] to the position
            // it would have if the array slice was sorted, and by moving all
            // values in the slice smaller than A[l] to earlier positions, and all values
            // larger than or equal to A[l] to later positions. Returns the index at which
            // the ‘pivot’ element formerly at location A[l] is placed.
            int pivotval = function_array[l];
            int pivotloc = l;
            for (int j = l + 1; j <= h; j++) {
                basic_operations++;
                if (function_array[j] < pivotval) {
                    pivotloc++;
                    //Swap
                    int temp = function_array[pivotloc];
                    function_array[pivotloc] = function_array[j];
                    function_array[j] = temp;
                }
            }
            //Swap
            int temp_2 = function_array[pivotloc];
            function_array[pivotloc] = function_array[l];
            function_array[l] = temp_2;
            return pivotloc;
        }

        // Creates array with random values
        private static int[] CreateRandomArray(int arraySize) {
            rnd = new Random();
            int[] temp_array = new int[arraySize];
            for (int i = 0; i < temp_array.Length; i++) {
                temp_array[i] = rnd.Next(1, 1000);
            }
            return temp_array;
        }

        // Creates array with ascending values
        private static int[] CreateAscendingArray(int arraySize) {
            int[] temp_array = new int[arraySize];
            int counter = 1;
            for (int i = 0; i < temp_array.Length; i++) {
                temp_array[i] = counter++;
            }
            return temp_array;
        }

        // Creates array with descending values
        private static int[] CreateDescendingArray(int arraySize) {
            int[] temp_array = new int[arraySize];
            int counter = arraySize;
            for (int i = 0; i < temp_array.Length; i++) {
                temp_array[i] = counter--;
            }
            return temp_array;
        }

        // Creates array with set values
        private static int[] CreateFunctionalTestArray() {
            int[] temp_array = {5, 4, 6, 3, 7, 2, 8, 1, 9}; 
            return temp_array;
        }

        // Function to refresh Data
        private static void RefreshData() {
            basic_operations = 0;
            for_loop_counter1 = 0;
            for_loop_counter2 = 0;
            if_loop_counter1 = 0;
            num_smaller_counter = 0;
            num_equal_counter = 0;
            time_efficiency = 0;
            median = 0;
        }

        // Function to setup Excel
        private static void CreateExcelData() {
            excel.Visible = true;
            excel.Workbooks.Add();
        }
    }
}
