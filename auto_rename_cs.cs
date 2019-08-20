using System;
using System.IO;

namespace cstemp
{
    class Program
    {
        public static void folder_to_file(string path)
        {
            string[] dirs = Directory.GetDirectories(path);
            foreach (string s in dirs)
            {
                folder_to_file(s);
            }
            string[] files = Directory.GetFiles(path);
            foreach (string s in files)
            {
                Directory.Move(s, "./" + s.Substring(2).Replace("/", "_").Replace("\\", "_"));
            }
            Console.WriteLine(path + "is finished.");
        }
        public static int Main()
        {
            Console.Title = "Auto Rename cs";
            string[] dirs = Directory.GetDirectories("./");
            foreach (string s in dirs)
            {
                Console.WriteLine(s);
                folder_to_file(s);
            }
            Console.WriteLine("\n\nAll Finished.");
            Console.Read();
            return 0;
        }
    }
}