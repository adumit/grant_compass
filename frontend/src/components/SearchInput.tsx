import React, { useState } from 'react';
import './css/SearchInput.css';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import Collapse from '@mui/material/Collapse';
import Box from '@mui/material/Box';
import SearchIcon from '@mui/icons-material/Search';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';


export interface SearchInputProps {
  query?: string;
  handleClick: Function;
  handleFileUpload?: Function; // Optional in case you only want to use it when expanded
}

export default function SearchInput({ query, handleClick, handleFileUpload }: SearchInputProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [inputValue, setInputValue] = useState(query || '');

  const keyDownHandler = (event: React.KeyboardEvent<HTMLElement>) => {
    if (event.code === "Enter") {
      handleClick();
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Enter your query..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={keyDownHandler}
          InputProps={{
            endAdornment: (
              <IconButton onClick={() => handleClick(inputValue)}>
                <SearchIcon />
              </IconButton>
            ),
          }}
        />
        <IconButton onClick={toggleExpand}>
          {isExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </IconButton>
      </Box>
      <Collapse in={isExpanded}>
        <Box sx={{ mt: 2 }}>
          <TextField
            fullWidth
            multiline
            minRows={3}
            maxRows={6}
            variant="outlined"
            placeholder="Enter your query or upload a document for analysis..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={keyDownHandler}
            id="searchInput"
          />
          <Button
            variant="contained"
            component="label"
            sx={{ mt: 2 }}
          >
            Upload File
            <input
              type="file"
              hidden
              onChange={handleFileUpload ? (e) => handleFileUpload(e) : undefined}
            />
          </Button>
        </Box>
      </Collapse>
    </Box>
  );
}
