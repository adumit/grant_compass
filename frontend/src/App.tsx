import React from 'react';
import { createBrowserRouter, RouterProvider, useNavigate, createSearchParams } from "react-router-dom";
import './index.css';
import './App.css';
import SearchInput from "./components/SearchInput";
import GrantResults from "./components/GrantResultsPage";
import GrantsPage from './GrantsChat';
import Header from './components/Header';
import Footer from './components/Footer';
import { Container, Typography, Box } from '@mui/material';


// Define the router outside the App component
const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/search",
    element: <GrantResults />,
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
    navigate({ pathname: "/search", search:`?${createSearchParams({q: inputField?.value})}`});
  }

  function handleFileUpload() {}

  return (
    <Container>
      <Box textAlign="center" my={5}>
        <Typography variant="h3" component="h1" gutterBottom>
          Welcome to Grant Compass
        </Typography>
        <SearchInput handleClick={goToSearch} handleFileUpload={handleFileUpload} />
      </Box>
    </Container>
  );
}

export default function App() {
  return (
    <>
      <Header />
      <meta name="viewport" content="initial-scale=1, width=device-width" />
      <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />
      <Footer />
    </>
  );
}