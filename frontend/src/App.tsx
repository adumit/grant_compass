import {
  createBrowserRouter,
  createSearchParams,
  RouterProvider,
  useNavigate,
} from "react-router-dom";
import { Search } from "./Search";
import "./index.css";
import SearchInput from "./SearchInput";

let router = createBrowserRouter([
  {
    path: "/",
    Component() {
      const navigate = useNavigate();

      function goToSearch() {
        const inputField = document.getElementById("searchInput") as HTMLInputElement;
        navigate({pathname: "/search", search:`?${createSearchParams({q: inputField?.value})}`})
      }

      return (
        <div style={{display: "flex", flexDirection:"column", justifyContent: "center"}}>
          <h1 style={{display: "flex", justifyContent: "center"}}>{"Welcome to Grant Compass!"}</h1>
          <div style={{display: "flex", justifyContent: "center"}}>
            <SearchInput handleClick={goToSearch} />
          </div>
        </div>
      );
    },
  },
  {
    path: "/search",
    element: <Search />
  }
]);

export default function App() {
  return <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />;
}