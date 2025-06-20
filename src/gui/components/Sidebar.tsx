import React from 'react';

export type Section =
  | 'dashboard'
  | 'files'
  | 'memory'
  | 'services'
  | 'audit'
  | 'settings';

type Props = {
  active: Section;
  onChange: (s: Section) => void;
};

const Sidebar: React.FC<Props> = ({ active, onChange }) => {
  const sections: { id: Section; label: string }[] = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'files', label: 'File Hierarchy' },
    { id: 'memory', label: 'Memory & Learning' },
    { id: 'services', label: 'API/Service Control' },
    { id: 'audit', label: 'Audit & Contradictions' },
    { id: 'settings', label: 'Settings' },
  ];

  return (
    <nav className="sidebar">
      <ul>
        {sections.map((s) => (
          <li key={s.id} className={s.id === active ? 'active' : ''}>
            <button type="button" onClick={() => onChange(s.id)}>
              {s.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Sidebar;
