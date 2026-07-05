import {
  Upload,
  GitBranch,
  BarChart3,
  Target,
  Settings,
  HelpCircle,
  Database,
  Activity,
  BookOpen,
} from 'lucide-react';

const navItems = [
  { id: 'upload', icon: Upload, label: 'Data Upload', section: '#upload' },
  { id: 'pipeline', icon: GitBranch, label: 'Pipeline', section: '#pipeline' },
  { id: 'analysis', icon: BarChart3, label: 'Analysis', section: '#analysis' },
  { id: 'targets', icon: Target, label: 'Target Discovery', section: '#targets' },
];

const bottomItems = [
  { id: 'datasets', icon: Database, label: 'Datasets' },
  { id: 'monitor', icon: Activity, label: 'System Monitor' },
  { id: 'docs', icon: BookOpen, label: 'Documentation' },
  { id: 'help', icon: HelpCircle, label: 'Help' },
];

export default function Sidebar() {
  const scrollTo = (sectionId) => {
    const element = document.querySelector(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <aside className="hidden lg:flex flex-col w-64 bg-surface-800/50 border-r border-surface-700 min-h-[calc(100vh-73px)]">
      <nav className="flex-1 p-4 space-y-1">
        <div className="mb-4">
          <p className="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-2">
            Workflow
          </p>
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => scrollTo(item.section)}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg
                         text-surface-300 hover:text-white hover:bg-surface-700
                         transition-colors text-sm"
            >
              <item.icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>

        <div>
          <p className="text-xs font-semibold text-surface-400 uppercase tracking-wider mb-2 pt-4 border-t border-surface-700">
            Resources
          </p>
          {bottomItems.map((item) => (
            <button
              key={item.id}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg
                         text-surface-300 hover:text-white hover:bg-surface-700
                         transition-colors text-sm"
            >
              <item.icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      </nav>

      <div className="p-4 border-t border-surface-700">
        <div className="flex items-center gap-3 px-3">
          <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-xs font-bold">
            BB
          </div>
          <div>
            <p className="text-sm text-white font-medium">BioOmicsBridge</p>
            <p className="text-xs text-surface-400">Team Edition</p>
          </div>
        </div>
      </div>
    </aside>
  );
}