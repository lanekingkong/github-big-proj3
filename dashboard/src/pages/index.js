import Head from 'next/head';
import DataUploadPanel from '../components/DataUploadPanel';
import PipelineMonitor from '../components/PipelineMonitor';
import AnalysisResults from '../components/AnalysisResults';
import TargetDiscovery from '../components/TargetDiscovery';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';

export default function Home() {
  return (
    <>
      <Head>
        <title>BioOmicsBridge - Dashboard</title>
        <meta name="description" content="AI-Powered Multi-Omics Data Integration" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-surface-900 text-white">
        <Header />

        <div className="flex">
          <Sidebar />

          <main className="flex-1 p-6 space-y-6">
            <section id="upload">
              <DataUploadPanel />
            </section>

            <section id="pipeline">
              <PipelineMonitor />
            </section>

            <section id="analysis">
              <AnalysisResults />
            </section>

            <section id="targets">
              <TargetDiscovery />
            </section>
          </main>
        </div>
      </div>
    </>
  );
}