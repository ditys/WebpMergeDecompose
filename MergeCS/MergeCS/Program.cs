using ImageMagick;
using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace MergeCS
{
    class Program
    {
        struct WorkItem
        {
            public string Name;
            public bool IsFile;
        }
        static void Main(string[] args)
        {
            OpenCL.IsEnabled = true;
            string[] folders = Directory.GetDirectories("MergePhotos");
            string[] files = Directory.GetFiles("MergePhotos");
            Directory.CreateDirectory("resultMerge");
            Console.WriteLine(DateTime.Now.ToString());

            Queue<WorkItem> q = new Queue<WorkItem>();
            foreach (string theFile in files)
            {
                q.Enqueue(new WorkItem{Name = theFile,IsFile =true });
            }
            foreach (string theFolder in folders)
            {
                q.Enqueue(new WorkItem { Name = theFolder, IsFile = false });
            }
            Thread[] Threads = new Thread[10];
            try
            {
                for (int i = 0; i < 10; i++)
                {
                    Threads[i] = new Thread(new ThreadStart(delegate ()
                    {
                        Worker(q);
                    }));
                    Threads[i].Start();
                }
                for (int i = 0; i < 10; i++)
                {
                    Threads[i].Join();
                }
            }
            catch (MagickException e)
            {
                Console.WriteLine(e.ToString());
            }
            Console.WriteLine(DateTime.Now.ToString() + "\n\nFinished.");
        }
        static void Worker(Queue<WorkItem> q)
        {
            while (q.Count != 0)
            {
                WorkItem workItem = q.Dequeue();
                if (workItem.IsFile)
                {
                    using (MagickImage image = new MagickImage(workItem.Name))
                    {
                        string temp = "resultMerge/" + Path.GetFileName(workItem.Name) + ".webp";
                        image.Quality = 80;
                        image.Write(temp);
                        Console.WriteLine(temp);
                    }
                }
                else
                {
                    using (MagickImageCollection collection = new MagickImageCollection())
                    {
                        string[] mergeFiles = Directory.GetFiles(workItem.Name);
                        foreach (string i in mergeFiles)
                        {
                            collection.Add(i);
                        }
                        QuantizeSettings settings = new QuantizeSettings();
                        settings.Colors = 256;
                        collection.Quantize(settings);
                        collection.Optimize();
                        string temp = string.Format("resultMerge/{0}.webp", workItem.Name.Substring(workItem.Name.LastIndexOf('/') + 1));
                        collection.Write(temp);
                        Console.WriteLine(temp);
                    }
                }

            }
        }
    }

}
