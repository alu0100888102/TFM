using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using System.Xml;
using System.Windows.Forms;
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
                finder.Title = "File to analyse";
                Console.WriteLine("File to analyse");
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
                Tracingfromfile.dumpfile = finder.FileName;
                if(dumpfile == filePath)
                {
                    Console.WriteLine("Choose an output file");
                    return;
                }
                Console.WriteLine(dumpfile);
                try
                {
                    File.WriteAllText(dumpfile, string.Empty);
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
                    Thread.Sleep(2,000);
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

            Tracingfromfile.tracking = new List<int>();
            Tracingfromfile.d = new XmlDocument();
            //Initializing ETW session
            Tracingfromfile.kernelSession = new TraceEventSession("ChaChaRealSmooth");
            Console.CancelKeyPress += delegate (object sender, ConsoleCancelEventArgs e) { kernelSession.Dispose(); };

            //subscribe to kernel events
            kernelSession.EnableKernelProvider(KernelTraceEventParser.Keywords.All);

            //Setup function handlers
            kernelSession.Source.Kernel.ProcessStart += processStarted; //Process Start
            kernelSession.Source.Kernel.ProcessStop += processStopped;  //Process Stop
            kernelSession.Source.Kernel.UdpIpRecv += general;   //Udp package recived
            kernelSession.Source.Kernel.UdpIpSend += general;   //Udp package sent
            kernelSession.Source.Kernel.ImageLoadGroup += general;  //DLL file loaded
            kernelSession.Source.Kernel.ImageUnloadGroup += general;    //DLL file unloaded
            kernelSession.Source.Kernel.SystemConfigNIC += general; //NIC configuration altered
            kernelSession.Source.Kernel.SystemConfigVideo += general;   //Video configuration altered
            kernelSession.Source.Kernel.SystemConfigServices += general;    //Services configuration altered
            kernelSession.Source.Kernel.SystemConfigPower += general;   //Power configuration altered
            kernelSession.Source.Kernel.SystemConfigIRQ += general; //IRQ configuration altered
            kernelSession.Source.Kernel.SystemConfigPnP += general; //PnP configuration altered
            kernelSession.Source.Kernel.SystemConfigNetwork += general; //Network configuration altered
            kernelSession.Source.Kernel.SystemConfigIDEChannel += general;  //IDE Channel configuration altered
            kernelSession.Source.Kernel.SystemConfigLogDisk += general; //Loggical Disk configuration altered
            kernelSession.Source.Kernel.SystemConfigPhyDisk += general; //Physical Disk configuration altered
            kernelSession.Source.Kernel.PerfInfoISR += general; //ISR periferers
            kernelSession.Source.Kernel.PerfInfoDPC += general; //DPC periferers
            kernelSession.Source.Kernel.SystemConfigCPU += general; //CPU configuration altered
            kernelSession.Source.Kernel.DiskIORead += general;  //Read from physical disk
            kernelSession.Source.Kernel.DiskIOWrite += general; //Write from physical disk
            kernelSession.Source.Kernel.DiskIODriverMajorFunctionCall += general;   //Driver from physical disk called
            kernelSession.Source.Kernel.DiskIODriverMajorFunctionReturn += general; //Driver from physical disk function returned
            kernelSession.Source.Kernel.ThreadStartGroup += general;    //Thread started
            kernelSession.Source.Kernel.ThreadEndGroup += general;  //Thread stopped
            kernelSession.Source.Kernel.TcpIpSend += general;   //Tcp package sent
            kernelSession.Source.Kernel.TcpIpRecv += general;   //Tcp package received
            kernelSession.Source.Kernel.TcpIpSendIPV6 += general;   //IPV6 package sent
            kernelSession.Source.Kernel.TcpIpRecvIPV6 += general;   //IPV6 package received
            kernelSession.Source.Kernel.FileIOFileCreate += general;    //New file created
            kernelSession.Source.Kernel.FileIOFileDelete += general;    //File deleted
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
                Console.WriteLine("Remaining process: {0}", Tracingfromfile.tracking.Count());
                File.AppendAllText(@Tracingfromfile.dumpfile, JsonConvert.SerializeXmlNode(d) + "\n");
            }
            else if (Tracingfromfile.tracking.Contains(data.ParentID))
            {
                Tracingfromfile.tracking.Add(data.ProcessID);
                Console.WriteLine("Remaining process: {0}", Tracingfromfile.tracking.Count());
                Tracingfromfile.d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Parent\":\"" + data.ParentID + "\",\"Type\":\"ProcessStarted\",\"Payload\":" + JsonConvert.SerializeXmlNode(d) + "}\n");
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