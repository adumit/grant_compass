import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Search } from "./Search";
import "./index.css";

let router = createBrowserRouter([
  {
    path: "/",
    Component() {
      return (
        <div>
          <h1>{"Welcome to Grant Compass!"}</h1>
          <Search />
        </div>
      );
    },
  }
]);

export default function App() {
  return <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />;
}