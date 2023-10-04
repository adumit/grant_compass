import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import "./index.css";

let router = createBrowserRouter([
  {
    path: "/",
    Component() {
      return (
      <div>
        <h1>{"Welcome to Grant Compass!"}</h1>
      </div>);
    },
  }
]);

export default function App() {
  return <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />;
}