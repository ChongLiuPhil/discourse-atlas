import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@xyflow/react/dist/style.css';
import './styles.css';
import './alignment.css';
import WorkspaceRouter from './WorkspaceRouter.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <WorkspaceRouter />
  </StrictMode>,
);
