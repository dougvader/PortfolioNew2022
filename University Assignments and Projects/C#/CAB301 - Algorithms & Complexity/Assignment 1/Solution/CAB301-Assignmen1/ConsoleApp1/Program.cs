using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Office.Interop.Excel;
using Excel = Microsoft.Office.Interop.Excel; 


namespace ConsoleApp1{
    class Program {
        // Variable instantiations
        public static Random rnd = new Random();
        public static int MaxValue = 0;
        public static int MinValue = 0;
        public static int BasicCounter = 0;
        public static int MaxCounter = 0;
        public static int MinCounter = 0;
        public static int testSize = 100;
        public static int data_count = 2;
        public static int arraySize = 10;
        public static int testCount = 1;
        public static int[] array;
        public static Excel._Worksheet worksheet;
        public static Excel.Application excel;

        // Main Executable
        static void Main(string[] args) {
            excel = new Excel.Application();
            CreateExcelData();

            // Runs the function a set amount of times
            for (int i = 1; i <= testSize; i++) {
                rnd = new Random();
                array = CreateRandomArray(arraySize);
                //array = CreateAscendingArray(arraySize); 
                //array = CreateDescendingArray(arraySize);
                //array = CreateFunctionalTestArray();

                // Increases the test count and resets variables
                MaxMin2(array);
                if (testCount < testSize) {
                    //arraySize++;
                    testCount++;
                    RefreshData();
                }
            }

            // Prints single test result to console
            Console.WriteLine("The highest number in the array is - " + MaxValue);
            Console.WriteLine("The lowest number in the array is - " + MinValue);
            Console.WriteLine("The array size is - " + arraySize);
            Console.WriteLine("The number of basic operations performed is - " + (MinCounter + BasicCounter));
            Console.WriteLine("The MaxValue operation is performed " + MaxCounter + " times");
            Console.WriteLine("The MinValue operation is performed " + MinCounter + " times");
            List<int> list = array.ToList();
            Console.WriteLine("The array consists of the following;");
            list.ForEach(o => Console.Write("{0}\t", o));
            Console.ReadLine();
        }

        // Main Algorithm 
        private static void MaxMin2(int[] n) {
            // Finds the maximum and minimum numbers in an array
            // Input parameter: An array A of n numbers, where n ≥ 1
            // array, MaxValue and MinValue, respectively
            worksheet = (Excel.Worksheet)excel.ActiveSheet;
            MaxValue = n[0];
            MinValue = n[0];
            for (int i = 1; i <= n.Length - 1; i++) {
                BasicCounter++;
                if (n[i] > MaxValue) {
                    MaxValue = n[i];
                    MaxCounter++;
                } else {
                    if (n[i] < MinValue) {
                        MinValue = n[i];
                        MinCounter++;
                    }
                }
            }
            // Export to Excel
            worksheet.Cells[1, 1] = "Array Length";
            worksheet.Cells[1, 2] = "Basic Operations";
            worksheet.Cells[data_count, 1] = n.Length;
            worksheet.Cells[data_count, 2] = MinCounter + BasicCounter;
            data_count++;
        }

        // Function to refresh Data
        private static void RefreshData() {
            MaxValue = 0;
            MinValue = 0;
            BasicCounter = 0;
            MaxCounter = 0;
            MinCounter = 0;
        }

        // Function to setup Excel
        private static void CreateExcelData() {
            excel.Visible = true;
            excel.Workbooks.Add();
        }

        // Creates array with random values
        private static int[] CreateRandomArray(int arraySize) {
            rnd = new Random();
            array = new int[arraySize];
            for (int i = 0; i < array.Length; i++) {
                array[i] = rnd.Next(1, 100);
            }
            return array;
        }

        // Creates array with ascending values
        private static int[] CreateAscendingArray(int arraySize) {
            array = new int[arraySize];
            int counter = 1; 
            for (int i = 0; i < array.Length; i++) {
                array[i] = counter++;
            }
            return array;
        }

        // Creates array with descending values
        private static int[] CreateDescendingArray(int arraySize) {
            array = new int[arraySize];
            int counter = arraySize;
            for (int i = 0; i < array.Length; i++) {
                array[i] = counter--;
            }
            return array;
        }

        // Creates array with set values
        private static int[] CreateFunctionalTestArray() {
            int[] array = {5,4,6,3,7,2,8,1,9};
            return array;
        }
    }
}
