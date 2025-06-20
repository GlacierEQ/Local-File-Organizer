import React from 'react';

const Topbar: React.FC = () => (
  <header className="topbar">
    <div className="operator-info">
      <span>Operator</span>
    </div>
    <div className="system-status">
      <span>Connected</span>
    </div>
  </header>
);

export default Topbar;
