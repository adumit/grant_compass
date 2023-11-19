import React, { useEffect, useState, ChangeEvent, KeyboardEvent } from 'react';
import { Grid, TextField, Button, Box } from '@mui/material';
import OpportunityCard from "../OpportunityCard";
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
    navigate('/grants', { state: { selectedOpportunities } });
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' && query) {
      setSearchParams({ q: query });
      fetchData(query);
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  const fetchData = (queryValue: string) => {
    const rootUrl: string = process.env.REACT_APP_BACKEND_URL ?? "http://localhost:8000";
    fetch(`${rootUrl}/search/?search_text=${queryValue}`)
      .then(response => response.json())
      .then(setData);
  };

  useEffect(() => {
    if (query) {
      fetchData(query);
    }
  }, []); // You may want to execute this only once when the component mounts or when certain conditions are met

  const footerHeight: string = '100px'; // Adjust the value according to your footer's height

  return (
    <Box sx={{ pb: footerHeight, width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'center', padding: 2 }}>
        <TextField
          fullWidth
          label="Search Grants"
          variant="outlined"
          value={query}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
          onKeyPress={(e: KeyboardEvent<HTMLDivElement>) => {
            if (e.key === 'Enter') {
              setSearchParams({ q: query });
              fetchData(query);
            }
          }}
          sx={{ flexGrow: 1, maxWidth: '1000px', mr: 2 }} // Adjust the maxWidth as needed for your design
        />
        <Button variant="contained" onClick={handleTalkToGrantsClick} sx={{ whiteSpace: 'nowrap' }}>
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
