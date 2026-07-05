import { GitBranch, CheckCircle2, Circle, ArrowRight, Clock } from 'lucide-react';

const PIPELINE_STEPS = [
  { id: 'ingest', label: 'Data Ingestion', status: 'completed', time: '2.3s' },
  { id: 'qc', label: 'Quality Control', status: 'completed', time: '5.1s' },
  { id: 'normalize', label: 'Normalization', status: 'completed', time: '3.7s' },
  { id: 'harmonize', label: 'Harmonization', status: 'running', time: 'running...' },
  { id: 'integrate', label: 'Integration', status: 'pending', time: '-' },
  { id: 'embed', label: 'Embedding', status: 'pending', time: '-' },
  { id: 'analyze', label: 'Analysis', status: 'pending', time: '-' },
  { id: 'discover', label: 'Target Discovery', status: 'pending', time: '-' },
];

export default function PipelineMonitor() {
  const completedSteps = PIPELINE_STEPS.filter((s) => s.status === 'completed').length;
  const progress = (completedSteps / PIPELINE_STEPS.length) * 100;

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Integration Pipeline</h2>
        <span className="badge badge-info">In Progress</span>
      </div>

      {/* Overall Progress */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-surface-300">Overall Progress</span>
          <span className="text-sm text-primary-400 font-medium">{Math.round(progress)}%</span>
        </div>
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Pipeline Steps */}
      <div className="space-y-1">
        {PIPELINE_STEPS.map((step, index) => (
          <div key={step.id}>
            {/* Connector line */}
            {index > 0 && (
              <div className="flex items-center ml-[19px] h-4">
                <div
                  className={`w-0.5 h-full ${
                    step.status === 'completed' || PIPELINE_STEPS[index - 1].status === 'completed'
                      ? 'bg-primary-500'
                      : 'bg-surface-700'
                  }`}
                />
              </div>
            )}

            <div
              className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${
                step.status === 'running'
                  ? 'bg-primary-500/10 border border-primary-500/30'
                  : 'hover:bg-surface-700/30'
              }`}
            >
              {/* Status icon */}
              {step.status === 'completed' ? (
                <CheckCircle2 className="w-5 h-5 text-green-400" />
              ) : step.status === 'running' ? (
                <div className="w-5 h-5 rounded-full border-2 border-primary-400 border-t-transparent animate-spin" />
              ) : (
                <Circle className="w-5 h-5 text-surface-600" />
              )}

              <div className="flex-1">
                <p
                  className={`text-sm font-medium ${
                    step.status === 'running' ? 'text-primary-300' : 'text-white'
                  }`}
                >
                  {step.label}
                </p>
                {step.status === 'running' && (
                  <p className="text-xs text-primary-400/70 mt-0.5">
                    Applying batch correction and cross-platform normalization...
                  </p>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Clock className="w-3.5 h-3.5 text-surface-500" />
                <span className="text-xs text-surface-400 font-mono">{step.time}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Stats */}
      <div className="grid-3col mt-6">
        <div className="stat-card">
          <div>
            <p className="stat-value">12,847</p>
            <p className="stat-label">Features Processed</p>
          </div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-value">5</p>
            <p className="stat-label">Omics Types</p>
          </div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-value">98.3%</p>
            <p className="stat-label">Data Completeness</p>
          </div>
        </div>
      </div>
    </div>
  );
}