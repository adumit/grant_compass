import { useEffect, useState } from "react";
import { Opportunity, SearchResponse } from "./types/apiTypes";
import OpportunityCard from "./OpportunityCard";
import { useSearchParams, useNavigate } from "react-router-dom";
import SearchInput from "./SearchInput";


export function Search() {
  const [search, setSearch] = useSearchParams();
  const [query, setQuery] = useState<string>(search.get("q") ?? "");
  const [data, setData] = useState<SearchResponse>({"Top matches":[]});
  const [selectedOpportunities, setSelectedOpportunities] = useState<Array<Opportunity>>([]);

  const handleOpportunityCheckboxChange = (opp: Opportunity, isChecked: boolean) => {
    setSelectedOpportunities(prevSelected => {
      if (isChecked) {
        // Add to selected opportunities
        return [...prevSelected, opp];
      } else {
        // Remove from selected opportunities
        return prevSelected.filter(otherOpp => otherOpp !== opp);
      }
    });
  };

  const navigate = useNavigate(); // useNavigate is a hook from react-router-dom

  const handleTalkToGrantsClick = () => {
    // Navigate to the new page and pass the selected opportunities as state
    navigate('/grants', { state: { selectedOpportunities } });
  };

  useEffect(() => {
    if (query && query !== "") {
      const rootUrl = process.env.REACT_APP_BACKEND_URL ?? "http://localhost:8000";
      fetch(`${rootUrl}/search/?search_text=${query}`)
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
      <div style={{display:"flex", justifyContent: "space-between", position:"sticky", top:0, backgroundColor:"white", padding: "10px"}}>
        <div style={{flexGrow: 1}}>
          <SearchInput query={query} handleClick={handleClick}/>
        </div>
        <button className="default-button" onClick={handleTalkToGrantsClick}>
          Talk to grants
        </button>
      </div>
      <ul>
        {data["Top matches"].map((item) => (
          <OpportunityCard key={item.OpportunityID} opportunity={item} onCheckboxChange={handleOpportunityCheckboxChange}/>
        ))}
      </ul>
    </div>
  );
}
