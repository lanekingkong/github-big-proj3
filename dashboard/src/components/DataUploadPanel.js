import { useState } from 'react';
import { Upload, X, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react';

const OMNICS_TYPES = [
  { id: 'genomics', label: 'Genomics', formats: 'VCF, PLINK, BED, GWAS', color: 'primary' },
  { id: 'transcriptomics', label: 'Transcriptomics', formats: 'h5ad, mtx, tsv, loom', color: 'accent' },
  { id: 'proteomics', label: 'Proteomics', formats: 'MaxQuant, DIA-NN, Spectronaut', color: 'green' },
  { id: 'metabolomics', label: 'Metabolomics', formats: 'mzML, mzXML, cdf', color: 'yellow' },
  { id: 'spatial', label: 'Spatial Omics', formats: 'Visium, MERFISH, Xenium', color: 'purple' },
];

export default function DataUploadPanel() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    const newFiles = files.map((file) => ({
      id: Date.now() + Math.random(),
      name: file.name,
      size: (file.size / 1024 / 1024).toFixed(2),
      type: detectOmicsType(file.name),
      status: 'ready',
    }));
    setUploadedFiles((prev) => [...prev, ...newFiles]);
  };

  const detectOmicsType = (filename) => {
    const ext = filename.toLowerCase();
    if (ext.includes('.vcf') || ext.includes('.bed') || ext.includes('.bim')) return 'genomics';
    if (ext.includes('.h5ad') || ext.includes('.mtx') || ext.includes('.loom')) return 'transcriptomics';
    if (ext.includes('.mzml') || ext.includes('.raw')) return 'proteomics';
    return 'genomics';
  };

  const removeFile = (id) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const statusIcon = (status) => {
    switch (status) {
      case 'ready': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'processing': return <Loader className="w-4 h-4 text-blue-400 animate-spin" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-400" />;
      default: return null;
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Multi-Omics Data Upload</h2>
        <button
          className="btn btn-primary text-sm"
          disabled={uploadedFiles.length === 0}
        >
          Start Processing
        </button>
      </div>

      {/* Drop Zone */}
      <div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer
          ${dragActive
            ? 'border-primary-500 bg-primary-500/10'
            : 'border-surface-600 hover:border-surface-500 bg-surface-700/30'
          }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <Upload className="w-10 h-10 text-surface-400 mx-auto mb-3" />
        <p className="text-surface-300 text-sm">
          Drag & drop multi-omics data files here
        </p>
        <p className="text-surface-500 text-xs mt-1">
          or click to browse files
        </p>
      </div>

      {/* Supported Formats */}
      <div className="grid-3col mt-4">
        {OMNICS_TYPES.map((type) => (
          <div
            key={type.id}
            className="bg-surface-700/30 rounded-lg p-3 border border-surface-600/50"
          >
            <p className="text-sm font-medium text-white">{type.label}</p>
            <p className="text-xs text-surface-400 mt-1">{type.formats}</p>
          </div>
        ))}
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="mt-4">
          <p className="text-sm font-medium text-surface-300 mb-2">
            Uploaded Files ({uploadedFiles.length})
          </p>
          <div className="space-y-2">
            {uploadedFiles.map((file) => (
              <div
                key={file.id}
                className="flex items-center justify-between bg-surface-700/50 rounded-lg px-4 py-2.5"
              >
                <div className="flex items-center gap-3">
                  <FileText className="w-4 h-4 text-surface-400" />
                  <div>
                    <p className="text-sm text-white">{file.name}</p>
                    <p className="text-xs text-surface-400">
                      {file.size} MB - {file.type}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {statusIcon(file.status)}
                  <button
                    onClick={() => removeFile(file.id)}
                    className="text-surface-500 hover:text-red-400 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}