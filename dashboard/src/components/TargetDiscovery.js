import { Target, Dna, Shield, Zap, Info, ExternalLink } from 'lucide-react';

const MOCK_TARGETS = [
  {
    rank: 1,
    name: 'TARGET_0001',
    gene: 'GENE12',
    score: 0.94,
    pathway: 'Inflammatory response',
    druggability: 'high',
    evidence: 'GWAS + proteomic',
    confidence: '★★★★★',
  },
  {
    rank: 2,
    name: 'TARGET_0042',
    gene: 'GENE47',
    score: 0.91,
    pathway: 'Metabolic reprogramming',
    druggability: 'high',
    evidence: 'Transcriptomic + PPI',
    confidence: '★★★★☆',
  },
  {
    rank: 3,
    name: 'TARGET_0018',
    gene: 'GENE03',
    score: 0.88,
    pathway: 'Cell cycle regulation',
    druggability: 'medium',
    evidence: 'Multi-omics',
    confidence: '★★★★☆',
  },
  {
    rank: 4,
    name: 'TARGET_0055',
    gene: 'GENE89',
    score: 0.85,
    pathway: 'Apoptosis signaling',
    druggability: 'high',
    evidence: 'Proteomic + clinical',
    confidence: '★★★☆☆',
  },
  {
    rank: 5,
    name: 'TARGET_0031',
    gene: 'GENE21',
    score: 0.83,
    pathway: 'DNA repair',
    druggability: 'medium',
    evidence: 'Genomic + literature',
    confidence: '★★★☆☆',
  },
];

export default function TargetDiscovery() {
  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Drug Target Discovery</h2>
        <span className="badge badge-success">
          {MOCK_TARGETS.length} targets found
        </span>
      </div>

      {/* Summary Stats */}
      <div className="grid-3col mb-6">
        <div className="stat-card">
          <Target className="w-6 h-6 text-red-400" />
          <div>
            <p className="stat-value">5</p>
            <p className="stat-label">High-confidence targets</p>
          </div>
        </div>
        <div className="stat-card">
          <Dna className="w-6 h-6 text-blue-400" />
          <div>
            <p className="stat-value">3</p>
            <p className="stat-label">Novel targets</p>
          </div>
        </div>
        <div className="stat-card">
          <Shield className="w-6 h-6 text-green-400" />
          <div>
            <p className="stat-value">92%</p>
            <p className="stat-label">Druggability rate</p>
          </div>
        </div>
      </div>

      {/* Targets Table */}
      <div className="overflow-x-auto">
        <table className="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Target ID</th>
              <th>Gene</th>
              <th>Score</th>
              <th>Pathway</th>
              <th>Druggability</th>
              <th>Evidence</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_TARGETS.map((target) => (
              <tr key={target.rank}>
                <td>
                  <span className="font-bold text-primary-400">#{target.rank}</span>
                </td>
                <td>
                  <span className="font-mono text-sm text-white">{target.name}</span>
                </td>
                <td>
                  <span className="text-sm text-surface-300">{target.gene}</span>
                </td>
                <td>
                  <div className="flex items-center gap-2">
                    <div className="w-16 progress-bar">
                      <div
                        className="progress-fill"
                        style={{ width: `${target.score * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-mono text-primary-400">
                      {target.score.toFixed(2)}
                    </span>
                  </div>
                </td>
                <td>
                  <span className="text-sm text-surface-300">{target.pathway}</span>
                </td>
                <td>
                  <span
                    className={`badge ${
                      target.druggability === 'high'
                        ? 'badge-success'
                        : 'badge-warning'
                    }`}
                  >
                    {target.druggability}
                  </span>
                </td>
                <td>
                  <span className="text-xs text-surface-400">{target.evidence}</span>
                </td>
                <td>
                  <div className="flex gap-2">
                    <button className="p-1.5 rounded-md text-surface-400 hover:text-white hover:bg-surface-700 transition-colors">
                      <Info className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 rounded-md text-surface-400 hover:text-white hover:bg-surface-700 transition-colors">
                      <ExternalLink className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Action Bar */}
      <div className="flex justify-between items-center mt-6 pt-4 border-t border-surface-700">
        <p className="text-xs text-surface-400">
          Targets ranked by composite score (embedding + network centrality + druggability).
          Click info icon for explainable AI evidence chain.
        </p>
        <div className="flex gap-2">
          <button className="btn btn-secondary text-sm">Export CSV</button>
          <button className="btn btn-primary text-sm">Generate Report</button>
        </div>
      </div>
    </div>
  );
}