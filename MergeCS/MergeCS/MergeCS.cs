using ImageMagick;
using System;
using System.IO;
using System.Collections.Concurrent;

namespace WMD
{
    namespace MergeCS
    {
        class MergeCS
        {
            static void Main(string[] args)
            {
                OpenCL.IsEnabled = true;
                string[] folders = Directory.GetDirectories("MergePhotos");
                string[] files = Directory.GetFiles("MergePhotos");
                Directory.CreateDirectory("resultMerge");
                Console.WriteLine(DateTime.Now.ToString());

                ConcurrentQueue<worker.WorkItem> q = new ConcurrentQueue<worker.WorkItem>();
                foreach (string theFile in files)
                {
                    q.Enqueue(new worker.WorkItem { Name = theFile, IsFile = true });
                }
                foreach (string theFolder in folders)
                {
                    q.Enqueue(new worker.WorkItem { Name = theFolder, IsFile = false });
                }
                worker.worker.work(10, delegate () { Task(q); });
                Console.WriteLine(DateTime.Now.ToString() + "\n\nFinished.");
            }
            public static void Task(ConcurrentQueue<worker.WorkItem> q)
            {
                worker.WorkItem workItem;
                while (q.Count != 0 && q.TryDequeue(out workItem))
                {
                    if (workItem.IsFile)
                    {
                        using (MagickImage image = new MagickImage(workItem.Name))
                        {
                            string temp = "resultMerge/" + Path.GetFileName(workItem.Name) + ".webp";
                            image.Quality = 85;
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
}
