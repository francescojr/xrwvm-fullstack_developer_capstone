import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import { Routes, Route, useLocation } from "react-router-dom";
import Dealers from './components/Dealers/Dealers';
import Dealer from './components/Dealers/Dealer';
import PostReview from "./components/Dealers/PostReview";


function App() {
  const location = useLocation();
  
  console.log('Current path:', location.pathname);
  
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers/>} />
      <Route path="/dealer/:id" element={<Dealer/>} />
      <Route path="/postreview/:id" element={<PostReview/>} />
      <Route path="*" element={<div>404 - Page not found. Path: {location.pathname}</div>} />
    </Routes>
  );
}

export default App;
