using System;
using System.IO;
using System.Threading;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Collections.Concurrent;

namespace cstemp
{
    class Program
    {
        public static int Main()
        {
            Console.Title = "Sort File C# Version";
            int multhreadings_number = 4;

            while (true)
            {
                string[] files = Directory.GetFiles("./");
                Dictionary<string, List<string>> common_dict = new Dictionary<string, List<string>> { };
                string common_str = "";
                bool Accepted = false;
                string Accepte_receviced = "";

                while (!Accepted)
                {
                    Console.Write("Keyin pattern : ");
                    string pattern = Console.ReadLine();
                    if (pattern == "")
                    {
                        continue;
                    }
                    Regex pattern_regex = new Regex(pattern);
                    common_dict.Clear();
                    foreach (string item in files)
                    {
                        Match pattern_group = pattern_regex.Match(item);
                        common_str = "";
                        int pattern_group_count = pattern_group.Groups.Count;
                        if (pattern_group_count > 1)
                        {
                            for (int i = 1; i < pattern_group_count; i++)
                            {
                                common_str += pattern_group.Groups[i];
                            }
                        }
                        else
                        {
                            common_str = pattern_group.Value;
                        }
                        if (common_str == "")
                        {
                            continue;
                        }
                        if (common_dict.ContainsKey(common_str))
                        {
                            common_dict[common_str].Add(item);
                        }
                        else
                        {
                            common_dict[common_str] = new List<string> { item };
                        }
                    }
                    foreach (string key in common_dict.Keys)
                    {
                        Console.WriteLine(key + " : [" + string.Join(" , ", common_dict[key]) + " ]");
                    }
                    Console.WriteLine("It is a result of match. Does it right?\n(nothing key in is Right;`inone` is put them in one folder;anything is error)");
                    Accepte_receviced = Console.ReadLine();
                    switch (Accepte_receviced)
                    {
                        case "":
                        case "inone":
                            Accepted = true;
                            break;
                        default:
                            continue;
                    }

                }
                ConcurrentQueue<Dictionary<string, List<string>>> File_Queue = new ConcurrentQueue<Dictionary<string, List<string>>> { };
                if (Accepte_receviced == "")
                {
                    foreach (string s in common_dict.Keys)
                    {
                        File_Queue.Enqueue(new Dictionary<string, List<string>> { { s, common_dict[s] } });
                    }
                }
                else if (Accepte_receviced == "inone")
                {
                    while (true)
                    {
                        Console.WriteLine("inone folder's name: ");
                        string Inone_Folder_name = Console.ReadLine();
                        if (Directory.Exists(Inone_Folder_name))
                        {
                            Console.WriteLine("Directory is exists!!!!\nPress any key to continue or Ctrl+c to stop it.");
                            Console.Read();
                        }
                        foreach (string s in common_dict.Keys)
                        {
                            File_Queue.Enqueue(new Dictionary<string, List<string>> { { Inone_Folder_name, common_dict[s] } });
                        }
                    }
                }
                List<Thread> threading_list = new List<Thread> { };
                for (int i = 0; i < multhreadings_number; i++)
                {
                    //threading_list.Add(new Thread(new ParameterizedThreadStart(SortFile)));
                    threading_list.Add(new Thread(() => SortFile(File_Queue)));
                }
                foreach (Thread t in threading_list)
                {
                    t.Start();
                }
            }
            return 0;
        }

        private static void SortFile(ConcurrentQueue<Dictionary<string, List<string>>> q)
        //private static void SortFile(object q)
        {
            while (!q.IsEmpty)
            {
                Dictionary<string, List<string>> a_dict = new Dictionary<string, List<string>> { };
                q.TryDequeue(out a_dict);
                foreach (string Folder in a_dict.Keys)
                {
                    if (Directory.Exists(Folder) == false)
                    {
                        Directory.CreateDirectory(Folder);
                        Console.WriteLine(string.Format("{0} is created.", Folder));
                    }
                    foreach (string File in a_dict[Folder])
                    {
                        Directory.Move(File, string.Format("{0}/{1}", Folder, File));
                    }
                    Console.WriteLine(string.Format("{0} is finished.", Folder));
                }
            }
        }
    }
}