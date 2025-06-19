import React, { useState } from 'react';
import Topbar from './components/Topbar';
import Sidebar, { Section } from './components/Sidebar';
import Dashboard from './components/Dashboard';
import FileHierarchy from './components/FileHierarchy';
import MemoryLearning from './components/MemoryLearning';
import ApiServiceControl from './components/ApiServiceControl';
import AuditContradictions from './components/AuditContradictions';
import Settings from './components/Settings';

const App: React.FC = () => {
  const [section, setSection] = useState<Section>('dashboard');

  const renderSection = () => {
    switch (section) {
      case 'dashboard':
        return <Dashboard />;
      case 'files':
        return <FileHierarchy />;
      case 'memory':
        return <MemoryLearning />;
      case 'services':
        return <ApiServiceControl />;
      case 'audit':
        return <AuditContradictions />;
      case 'settings':
        return <Settings />;
      default:
        return null;
    }
  };

  return (
    <div className="gui-root">
      <Topbar />
      <div className="workspace">
        <Sidebar active={section} onChange={setSection} />
        <main className="main-panel">{renderSection()}</main>
      </div>
    </div>
  );
};

export default App;
