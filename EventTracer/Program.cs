using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Security.Permissions;
using Newtonsoft.Json;
using System.Xml;

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
        static List<int> tracking;
        static TraceEventSession kernelSession;
        static Process baseProcess;
        static string dumpfile;

        static void Main(string[] args)
        {
            //Check admin privileges
            if (TraceEventSession.IsElevated() == false)
            {
                Console.WriteLine("Please run me as Administrator");
                return;
            }

            string filePath = string.Empty;
            Console.WriteLine("File to analyze");
//            filePath = Console.ReadLine();
            filePath = "E:\\Games\\League of Legends\\LeagueClient.exe";
            if (!File.Exists(filePath))
            {
                Console.WriteLine("The input file {0} does not exists", filePath);
                return;
            }

            Console.WriteLine("Output file");
//            dumpfile = Console.ReadLine();
            dumpfile = "E:\\DumpPile\\test1.txt";
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
        }

        public void begin()
        {

            try
            {
                ThreadStart ths = new ThreadStart(() => {
                    Thread.Sleep(2000);
                    baseProcess.Start();
                    Tracingfromfile.tracking.Add(baseProcess.Id);
                });
                Thread th = new Thread(ths);
                th.Start();
                kernelSession.Source.Process();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }

        public Tracingfromfile(string filename)
        {

            tracking = new List<int>();

            //Initializing ETW session
            kernelSession = new TraceEventSession("ChaChaRealSmooth");
            Console.CancelKeyPress += delegate (object sender, ConsoleCancelEventArgs e) { kernelSession.Dispose(); };

            //subscribe to kernel events
            kernelSession.EnableKernelProvider(KernelTraceEventParser.Keywords.All);

            //Setup function handlers
            kernelSession.Source.Kernel.ProcessStart += processStarted;
            kernelSession.Source.Kernel.ProcessStop += processStopped;
            kernelSession.Source.Kernel.UdpIpRecv += UdpIpRecv;
            kernelSession.Source.Kernel.UdpIpSend += UdpIpSend;
            kernelSession.Source.Kernel.UdpIpFail += UdpIpFail;
            kernelSession.Source.Kernel.ImageLoadGroup += ImageLoad;
            kernelSession.Source.Kernel.ImageUnloadGroup += ImageUnload;
            kernelSession.Source.Kernel.SystemConfigNIC += SystemConfigNIC;
            kernelSession.Source.Kernel.SystemConfigVideo += SystemConfigVideo;
            kernelSession.Source.Kernel.SystemConfigServices += SystemConfigServices;
            kernelSession.Source.Kernel.SystemConfigPower += SystemConfigPower;
            kernelSession.Source.Kernel.SystemConfigIRQ += SystemConfigIRQ;
            kernelSession.Source.Kernel.SystemConfigPnP += SystemConfigPnP;
            kernelSession.Source.Kernel.SystemConfigNetwork += SystemConfigNetwork;
            kernelSession.Source.Kernel.SystemConfigIDEChannel += SystemConfigIDEChannel;
            kernelSession.Source.Kernel.SystemConfigLogDisk += SystemConfigLogDisk;
            kernelSession.Source.Kernel.SystemConfigPhyDisk += SystemConfigPhyDisk;
            kernelSession.Source.Kernel.TcpIpConnectIPV6 += TcpIpConnectIPV6;
            kernelSession.Source.Kernel.TcpIpDisconnectIPV6 += TcpIpDisconnectIPV6;
            kernelSession.Source.Kernel.PerfInfoISR += PerfInfoISR;
            kernelSession.Source.Kernel.PerfInfoDPC += PerfInfoDPC;
            kernelSession.Source.Kernel.SystemConfigCPU += SystemConfigCPU;
            kernelSession.Source.Kernel.DiskIORead += DiskIORead;
            kernelSession.Source.Kernel.DiskIOWrite += DiskIOWrite;
            kernelSession.Source.Kernel.DiskIODriverMajorFunctionCall += DiskIODriverMajorFunctionCall;
            kernelSession.Source.Kernel.DiskIODriverMajorFunctionReturn += DiskIODriverMajorFunctionReturn;
            kernelSession.Source.Kernel.ThreadStartGroup += ThreadStartGroup;
            kernelSession.Source.Kernel.ThreadEndGroup += ThreadEndGroup;
            kernelSession.Source.Kernel.TcpIpSend += TcpIpSend;
            kernelSession.Source.Kernel.TcpIpRecv += TcpIpRecv;
            kernelSession.Source.Kernel.TcpIpDisconnect += TcpIpDisconnect;
            kernelSession.Source.Kernel.TcpIpConnect += TcpIpConnect;
            kernelSession.Source.Kernel.TcpIpSendIPV6 += TcpIpSendIPV6;
            kernelSession.Source.Kernel.TcpIpRecvIPV6 += TcpIpRecvIPV6;
            kernelSession.Source.Kernel.FileIOMapFile += FileIOMapFile;
            kernelSession.Source.Kernel.FileIOUnmapFile += FileIOUnmapFile;
            kernelSession.Source.Kernel.FileIOWrite += FileIOWrite;
            kernelSession.Source.Kernel.FileIORead += FileIORead;
            kernelSession.Source.Kernel.FileIOFileCreate += FileIoFileCreate;
            kernelSession.Source.Kernel.FileIOFileDelete += FileIOFileDelete;

            //setting up the staring process
            baseProcess = new Process();
            baseProcess.StartInfo.UseShellExecute = true;
            baseProcess.StartInfo.FileName = filename;
            baseProcess.StartInfo.CreateNoWindow = false;
        }

        private static void FileIOFileDelete(FileIONameTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"FileIOFileDelete\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void FileIoFileCreate(FileIONameTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"FileIoFileCreate\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void FileIORead(FileIOReadWriteTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"FileIORead\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void FileIOWrite(FileIOReadWriteTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"FileIOWrite\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void FileIOUnmapFile(MapFileTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"FileIOUnmapFile\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void FileIOMapFile(MapFileTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"FileIOMapFile\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpRecvIPV6(TcpIpV6TraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpRecvIPV6\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpSendIPV6(TcpIpV6SendTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpSendIPV6\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpConnect(TcpIpConnectTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpConnect\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpDisconnect (TcpIpTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpDisconnect\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpRecv(TcpIpTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpRecv\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpSend(TcpIpSendTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpSend\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void ThreadEndGroup(ThreadTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"ThreadEnd/DCStop\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void ThreadStartGroup(ThreadTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"ThreadStart/DCStart\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void DiskIODriverMajorFunctionReturn(DriverMajorFunctionReturnTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"DiskIODriverMajorFunctionReturn\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void DiskIODriverMajorFunctionCall(DriverMajorFunctionCallTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"DiskIODriverMajorFunctionCall\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void DiskIORead(DiskIOTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"DiskIORead\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void DiskIOWrite(DiskIOTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"DiskIOWrite\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigCPU(SystemConfigCPUTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigCPU\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void PerfInfoDPC(DPCTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"PerfInfoDPC\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void PerfInfoISR(ISRTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"PerfInfoISR\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpDisconnectIPV6(TcpIpV6TraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpDisconnectIPV6\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void TcpIpConnectIPV6(TcpIpV6ConnectTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"TcpIpConnectIPV6\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigPhyDisk(SystemConfigPhyDiskTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigPhyDisk\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigLogDisk(SystemConfigLogDiskTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigLogDisk\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigIDEChannel(SystemConfigIDEChannelTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigNIC\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigNetwork(SystemConfigNetworkTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigNetwork\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigPnP(SystemConfigPnPTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigPnP\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigIRQ(SystemConfigIRQTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigIRQ\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigPower(SystemConfigPowerTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigPower\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigServices(SystemConfigServicesTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigServices\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigVideo(SystemConfigVideoTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigVideo\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void SystemConfigNIC(SystemConfigNICTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"SystemConfigNIC\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void ImageUnload(ImageLoadTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"DllImageUnload/DCStop\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void ImageLoad(ImageLoadTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"DllImageLoad/DCStart\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void UdpIpRecv(UdpIpTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"UdpIpRecv\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void UdpIpSend(UdpIpTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"UdpIpSend\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void UdpIpFail(UdpIpFailTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"UdpIpFail\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
        }

        private static void processStarted(ProcessTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"ProcessStarted\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }
            else if (Tracingfromfile.tracking.Contains(data.ParentID))
            {
                Tracingfromfile.tracking.Add(data.ProcessID);
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Parent\":\""+data.ParentID+",\"Type\":\"ProcessStarted\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
            }

        }

        private static void processStopped(ProcessTraceData data)
        {
            if (Tracingfromfile.tracking.Contains(data.ProcessID))
            {
                XmlDocument d = new XmlDocument();
                d.LoadXml(data.Dump());
                File.AppendAllText(@Tracingfromfile.dumpfile, "{\"ID\":\"" + data.ProcessID + "\",\"Type\":\"ProcessStopped\",\"Payload\"" + JsonConvert.SerializeXmlNode(d) + "}");
                Tracingfromfile.tracking.Remove(data.ProcessID);
                if (Tracingfromfile.tracking.Count() == 0)
                {
                    Console.WriteLine("Process Finished");
                }
            }
        }

    }
}
