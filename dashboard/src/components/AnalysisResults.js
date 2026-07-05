import { BarChart3, Network, Activity } from 'lucide-react';

export default function AnalysisResults() {
  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Analysis Results</h2>
        <div className="flex gap-2">
          <button className="btn btn-secondary text-sm">Export PDF</button>
          <button className="btn btn-primary text-sm">Share Results</button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 bg-surface-700/50 rounded-lg p-1 w-fit">
        <button className="px-4 py-2 text-sm rounded-md bg-primary-600 text-white">
          Knowledge Graph
        </button>
        <button className="px-4 py-2 text-sm rounded-md text-surface-300 hover:text-white">
          Embeddings
        </button>
        <button className="px-4 py-2 text-sm rounded-md text-surface-300 hover:text-white">
          Pathway Map
        </button>
        <button className="px-4 py-2 text-sm rounded-md text-surface-300 hover:text-white">
          Heatmap
        </button>
      </div>

      {/* Graph Visualization Placeholder */}
      <div className="bg-surface-700/30 rounded-xl border border-surface-600/50 p-8 min-h-[400px] flex flex-col items-center justify-center text-center">
        <Network className="w-16 h-16 text-primary-400 mb-4" />
        <h3 className="text-lg font-medium text-white mb-2">
          Multi-Omics Knowledge Graph
        </h3>
        <p className="text-sm text-surface-400 max-w-md">
          Interactive network visualization showing cross-omics relationships,
          with nodes colored by omics type and edges weighted by association strength.
        </p>
        <div className="flex gap-4 mt-6">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-400" />
            <span className="text-xs text-surface-400">Genomics</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-400" />
            <span className="text-xs text-surface-400">Transcriptomics</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-400" />
            <span className="text-xs text-surface-400">Proteomics</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-400" />
            <span className="text-xs text-surface-400">Spatial</span>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid-3col mt-6">
        <div className="stat-card">
          <div>
            <p className="stat-value text-accent-500">2,341</p>
            <p className="stat-label">Cross-omics Edges</p>
          </div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-value text-accent-500">847</p>
            <p className="stat-label">Enriched Pathways</p>
          </div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-value text-accent-500">92.1%</p>
            <p className="stat-label">Variance Explained</p>
          </div>
        </div>
      </div>
    </div>
  );
}