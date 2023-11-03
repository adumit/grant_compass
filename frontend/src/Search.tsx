import { useEffect, useState } from "react";
import { Opportunity, SearchResponse } from "./types/apiTypes";
import OpportunityCard from "./OpportunityCard";
import SearchInput from "./SearchInput";
import { useSearchParams } from "react-router-dom";

export function Search() {
  const [search, setSearch] = useSearchParams();
  const [query, setQuery] = useState<string>(search.get("q") ?? "");
  const [data, setData] = useState<SearchResponse>({"Top matches":[]});

  useEffect(() => {
    if (query && query !== "") {
      fetch(`http://localhost:8000/search/?search_text=${query}`)
      .then(response => response.json())
      .then(setData);

      setSearch({q: query})
    }
  }, [query]);

  function handleClick() {
    const inputField = document.getElementById("searchInput") as HTMLInputElement;
    if (inputField) {
      setQuery(inputField.value ?? "")
    }
  }

  return (
    <div style={{display:"flex", flexDirection:"column"}}>
      <div style={{display:"flex", position:"sticky", top:0, backgroundColor:"white"}}>
        <div style={{display:"flex", paddingLeft:10, paddingTop:5, paddingBottom:2}}>
          <SearchInput query={query} handleClick={handleClick}/>
        </div>
      </div>
      <ul>
        {data &&
          data["Top matches"].map((item: Opportunity) => (
          <OpportunityCard opportunity={item}/>
        ))}
      </ul>
    </div>
  );
}



