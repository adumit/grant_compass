import { useEffect, useState } from "react";

export function Search() {
  const [query, setQuery] = useState("");
  const [data, setData] = useState<{"Top matches": {"OpportunityID": string, "OpportunityTitle": string}[]}>({"Top matches":[]});

  useEffect(() => {
    if (query !== "") {
      fetch(`http://localhost:8000/search/?search_text=${query}`)
      .then(response => response.json())
      .then(setData);
    }
  }, [query]);

  function handleClick() {
    const inputField = document.getElementById("searchInput") as HTMLInputElement;
    if (inputField && inputField.value !== "") {
      setQuery(inputField.value)
    }
  }

  return (
    <div>
      <input placeholder="Enter search" id="searchInput"/>
      <button onClick={handleClick}>
        Search
      </button>
      <ul>
        {data &&
          data["Top matches"].map((item: {"OpportunityID": string, "OpportunityTitle": string}) => (
          <li key={item.OpportunityID}>
            <h3>{item.OpportunityTitle}</h3>
          </li>
        ))}
      </ul>
    </div>
  );
}



