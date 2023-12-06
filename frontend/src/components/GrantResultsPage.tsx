import { useEffect, useState, ChangeEvent, KeyboardEvent } from 'react';
import { Grid, TextField, Button, Box } from '@mui/material';
import OpportunityCard from "./OpportunityCard";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Opportunity, SearchResponse } from "../types/apiTypes";

export default function GrantResults() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState<string>(searchParams.get("q") ?? "");
  const [data, setData] = useState<SearchResponse>({ "Top matches": [] });
  const [selectedOpportunities, setSelectedOpportunities] = useState<Opportunity[]>([]);
  const navigate = useNavigate();

  const handleOpportunityCheckboxChange = (opp: Opportunity, isChecked: boolean) => {
    setSelectedOpportunities(prevSelected => {
      if (isChecked) {
        return [...prevSelected, opp];
      } else {
        return prevSelected.filter(otherOpp => otherOpp !== opp);
      }
    });
  };

  const handleTalkToGrantsClick = () => {
    const params: URLSearchParams = new URLSearchParams();
    selectedOpportunities.map(opp => params.append("id", opp.OpportunityID))
    navigate({ pathname: '/grants', search: `?${params.toString()}` }, { state: { selectedOpportunities } });
  };

  // Update the search bar string as characters are typed
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  // Update the page query params, triggering data reload, when a user hits the enter key
  const handleKeyPress = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' && query) {
      setSearchParams({ q: query });
    }
  };

  // Ensure the query and data match the search param any time the params are updated
  // This covers page load, on-page searches, and back navigation
  useEffect(() => {
    const queryValue: string = searchParams.get("q") ?? "";
    setQuery(queryValue);
    fetchData(queryValue);
  }, [searchParams]);

  // Pull data from the backend and set the page results
  const fetchData = (queryValue: string) => {
    const rootUrl: string = process.env.REACT_APP_BACKEND_URL ?? "http://localhost:8000";
    fetch(`${rootUrl}/search/?search_text=${queryValue}`)
      .then(response => response.json())
      .then(setData);
  };

  const footerHeight: string = '100px'; // Adjust the value according to your footer's height

  return (
    <Box sx={{ pb: footerHeight, width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'center', padding: 2 }}>
        <TextField
          fullWidth
          label="Search Grants"
          variant="outlined"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyPress}
          sx={{ flexGrow: 1, maxWidth: '1000px', mr: 2 }} // Adjust the maxWidth as needed for your design
        />
        <Button variant="contained" onClick={handleTalkToGrantsClick} disabled={selectedOpportunities.length === 0}>
          Talk to grants
        </Button>
      </Box>
      <Grid container justifyContent="center" spacing={2}>
        {data["Top matches"].map((item: Opportunity) => (
          <Grid item xs={12} key={item.OpportunityID} sx={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
            <OpportunityCard opportunity={item} onCheckboxChange={handleOpportunityCheckboxChange}/>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
