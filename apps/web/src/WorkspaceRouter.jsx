import { useState } from 'react';
import ReaderApp from './App.jsx';
import AlignmentWorkbench from './components/AlignmentWorkbench.jsx';

export default function WorkspaceRouter() {
  const [mode, setMode] = useState('reader');
  if (mode === 'alignment') return <AlignmentWorkbench onBack={() => setMode('reader')} />;
  return (
    <>
      <nav className="mode-switcher" aria-label="Workspace mode">
        <button className="active" disabled>Reader</button>
        <button onClick={() => setMode('alignment')}>Alignment</button>
      </nav>
      <ReaderApp />
    </>
  );
}
