//Name: Craig McMillan
//Student Number: S2390641
//Date: 14/03/26
//This file // This file initialises and renders the React application

import ReactDOM from 'react-dom/client';
import { BrowserRouter} from 'react-router-dom';
import App from './App'
import './index.css'



ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
);
