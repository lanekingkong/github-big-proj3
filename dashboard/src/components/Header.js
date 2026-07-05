import { Beaker, Github, Menu } from 'lucide-react';
import { useState } from 'react';

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="bg-surface-800 border-b border-surface-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <Beaker className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">BioOmicsBridge</h1>
            <p className="text-xs text-surface-400">Multi-Omics Data Integration</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <a
            href="https://github.com/yourusername/BioOmicsBridge"
            target="_blank"
            rel="noopener noreferrer"
            className="text-surface-400 hover:text-white transition-colors"
          >
            <Github className="w-5 h-5" />
          </a>

          <div className="hidden md:flex items-center gap-4">
            <span className="badge badge-success">v1.0.0</span>
            <button className="btn btn-secondary text-sm">Documentation</button>
            <button className="btn btn-primary text-sm">New Analysis</button>
          </div>

          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden text-surface-400 hover:text-white"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}