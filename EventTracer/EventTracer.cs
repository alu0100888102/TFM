using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Security.Permissions;
using Newtonsoft.Json;
using System.Xml;
using System.Windows.Forms;

using Microsoft.Diagnostics.Symbols;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Session;
using Microsoft.Diagnostics.Tracing.Parsers;
using Microsoft.Diagnostics.Tracing.Parsers.Kernel;
using System.Threading;
using System.IO;

namespace EventTracer
{
    class Tracingfromfile
    {
        static List<int> tracking; //Process being tracked
        static TraceEventSession kernelSession; //Session
        static Process baseProcess; //This will execute the file
        static string dumpfile; //Output file, JSON format
        static XmlDocument d;   //XmlDocument that will access to data
        static OpenFileDialog finder;

        static void Main(string[] args)
        {
            //Check admin privileges
            if (TraceEventSession.IsElevated() == false)
            {
                Console.WriteLine("Please run me as Administrator");
                Console.ReadLine();
                return;
            }
            Thread t = new Thread((ThreadStart)(() =>
            {
                //Get the file to analyze
                string filePath = string.Empty;
                Tracingfromfile.finder = new OpenFileDialog();
                finder.Title = "File to analyze";
                Console.WriteLine("File to analyze");
                finder.ShowDialog();
                filePath = finder.FileName;
                if (!File.Exists(filePath))
                {
                    Console.WriteLine("The input file {0} does not exists", filePath);
                    Console.ReadLine();
                    return;
                }
                Console.WriteLine(filePath);


                //Get output file
                Console.WriteLine("Output file");
                finder.Title = "Output file";
                finder.ShowDialog();
                dumpfile = finder.FileName;
                if(dumpfile == filePath)
                {
                    Console.WriteLine("Choose an output file");
                    return;
                }
                Console.WriteLine(dumpfile);
                try
                {
                    System.IO.File.WriteAllText(dumpfile, string.Empty);
                }
                catch (IOException e)
                {
                    Console.WriteLine("Unable to open Output File: {0}", e);
                    return;
                }

                Tracingfromfile tracer = new Tracingfromfile(filePath);
                tracer.begin();
            }));
            t.SetApartmentState(ApartmentState.STA);
            t.Start();
        }

        //Start the tracking
        public void begin()
        {

            try
            {
                ThreadStart ths = new ThreadStart(() =>
                {
                    Thread.Sleep(1000);
                    baseProcess.Start();
                    Console.WriteLine("Starting process");
                    Tracingfromfile.tracking.Add(baseProcess.Id); //Starts tracking the process we created
                });
                Thread th = new Thread(ths);
                th.Start();
                kernelSession.Source.Process(); //Starts the tracer
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }

        //Builder
        public Tracingfromfile(string filename)
        {

            tracking = new List<int>();
            d = new XmlDocument();
            //Initializing ETW session
            kernelSession = new TraceEventSession("ChaChaRealSmooth");
            Console.CancelKeyPress += delegate (object sender, ConsoleCancelEventArgs e) { kernelSession.Dispose(); };

            //subscribe to kernel events
            kernelSession.EnableKernelProvider(KernelTraceEventParser.Keywords.All);

            //Setup function handlers
            kernelSession.Source.Kernel.ProcessStart += processStarted;
            kernelSession.Source.Kernel.ProcessStop += processStopped;
            kernelSession.Source.Kernel.UdpIpRecv += general;
            kernelSession.Source.Kernel.UdpIpSend += general;
            //kernelSession.Source.Kernel.UdpIpFail += general;
            kernelSession.Source.Kernel.ImageLoadGroup += general;
            kernelSession.Source.Kernel.ImageUnloadGroup += general;
            kernelSession.Source.Kernel.SystemConfigNIC += general;
            kernelSession.Source.Kernel.SystemConfigVideo += general;
            kernelSession.Source.Kernel.SystemConfigServices += general;
            kernelSession.Source.Kernel.SystemConfigPower += general;
            kernelSession.Source.Kernel.SystemConfigIRQ += general;
            kernelSession.Source.Kernel.SystemConfigPnP += general;
            kernelSession.Source.Kernel.SystemConfigNetwork += general;
            kernelSession.Source.Kernel.SystemConfigIDEChannel += general;
            kernelSession.Source.Kernel.SystemConfigLogDisk += general;
            kernelSession.Source.Kernel.SystemConfigPhyDisk += general;
            //kernelSession.Source.Kernel.TcpIpConnectIPV6 += general;
            //kernelSession.Source.Kernel.TcpIpDisconnectIPV6 += general;
            kernelSession.Source.Kernel.PerfInfoISR += general;
            kernelSession.Source.Kernel.PerfInfoDPC += general;
            kernelSession.Source.Kernel.SystemConfigCPU += general;
            kernelSession.Source.Kernel.DiskIORead += general;
            kernelSession.Source.Kernel.DiskIOWrite += general;
            kernelSession.Source.Kernel.DiskIODriverMajorFunctionCall += general;
            kernelSession.Source.Kernel.DiskIODriverMajorFunctionReturn += general;
            kernelSession.Source.Kernel.ThreadStartGroup += general;
            kernelSession.Source.Kernel.ThreadEndGroup += general;
            kernelSession.Source.Kernel.TcpIpSend += general;
            kernelSession.Source.Kernel.TcpIpRecv += general;
            //kernelSession.Source.Kernel.TcpIpDisconnect += general;
            //kernelSession.Source.Kernel.TcpIpConnect += general;
            kernelSession.Source.Kernel.TcpIpSendIPV6 += general;
            kernelSession.Source.Kernel.TcpIpRecvIPV6 += general;
            //kernelSession.Source.Kernel.FileIOMapFile += general;
            //kernelSession.Source.Kernel.FileIOUnmapFile += general;
            //kernelSession.Source.Kernel.FileIOWrite += general;
            //kernelSession.Source.Kernel.FileIORead += general;
            kernelSession.Source.Kernel.FileIOFileCreate += general;
            kernelSession.Source.Kernel.FileIOFileDelete += general;
            //kernelSession.Source.Kernel.All += general;

            //setting up the staring process
            baseProcess = new Process();
            baseProcess.StartInfo.UseShellExecute = true;
            baseProcess.StartInfo.FileName = filename;
            baseProcess.StartInfo.CreateNoWindow = false;
        }

        private static void general(TraceEvent data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                Tracingfromfile.d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile,JsonConvert.SerializeXmlNode(d)+ "\n");
            }
        }

       
        private static void processStarted(ProcessTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                Tracingfromfile.d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, JsonConvert.SerializeXmlNode(d) + "\n");
            }
            else if (Tracingfromfile.tracking.Contains(data.ParentID))
            {
                Tracingfromfile.tracking.Add(data.ProcessID);
                Console.WriteLine("Remaining process: {0}", Tracingfromfile.tracking.Count());
                Tracingfromfile.d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Parent\":\"" + data.ParentID + "\",\"Type\":\"ProcessStarted\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }

        }

        private static void processStopped(ProcessTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                Tracingfromfile.d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, JsonConvert.SerializeXmlNode(d) + "\n");
                Tracingfromfile.tracking.Remove(data.ProcessID);
                Console.WriteLine("Remaining process: {0}", Tracingfromfile.tracking.Count());
                if (Tracingfromfile.tracking.Count() == 0)
                {
                    Console.WriteLine("Process Finished");
                }
            }
        }

    }
}