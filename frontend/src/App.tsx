import React from 'react';
import { createBrowserRouter, RouterProvider, useNavigate } from "react-router-dom";
import './index.css';
import './App.css';
import SearchInput from "./components/SearchInput";
import Search from "./Search";
import GrantsPage from './GrantsChat';
import Header from './components/Header';
import Footer from './components/Footer';

// Define the router outside the App component
const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/search",
    element: <Search />,
  },
  {
    path: '/grants',
    element: <GrantsPage />,
  },
]);

function HomePage() {
  const navigate = useNavigate();

  function goToSearch() {
    const inputField = document.getElementById("searchInput") as HTMLInputElement;
    navigate({ pathname: "/search", search: `?q=${inputField?.value}` });
  }

  function handleFileUpload() {}

  return (
    <div className="home-container">
      <h1 className="home-title">{"Welcome to Grant Compass!"}</h1>
      <div className="search-container">
        <SearchInput handleClick={goToSearch} handleFileUpload={handleFileUpload} />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <>
      <Header />
      <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />
      <Footer />
    </>
  );
}