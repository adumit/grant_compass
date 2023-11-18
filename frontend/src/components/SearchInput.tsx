import React, { useState } from 'react';
import './css/SearchInput.css';

export interface SearchInputProps {
  query?: string;
  handleClick: Function;
  handleFileUpload?: Function; // Optional in case you only want to use it when expanded
}

export default function SearchInput({ query, handleClick, handleFileUpload }: SearchInputProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const keyDownHandler = (event: React.KeyboardEvent<HTMLElement>) => {
    if (event.code === "Enter") {
      handleClick();
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="search-container" onMouseEnter={() => {/* Show tooltip */}} onMouseLeave={() => {/* Hide tooltip */}}>
      <div className={`search-bar-container ${isExpanded ? 'expanded' : ''}`}>
        {isExpanded ? (
          <textarea 
            className="search-textarea"
            id="searchInput" 
            defaultValue={query} 
            onKeyDown={keyDownHandler as React.KeyboardEventHandler<HTMLTextAreaElement>}
            rows={4}
            placeholder="Enter your query or upload a document for analysis..."
          />
        ) : (
          <input 
            className="search-input"
            id="searchInput" 
            type="text"
            defaultValue={query} 
            onKeyDown={keyDownHandler as React.KeyboardEventHandler<HTMLInputElement>}
            placeholder="Enter your query..."
          />
        )}
        <button className="default-button search-button" onClick={() => handleClick()}>
          Search
        </button>
        <button className="default-button expand-button" onClick={toggleExpand}>
          {isExpanded ? "▲" : "▼"}
        </button>
      </div>
      
      {isExpanded && (
        <div className="button-group">
          <button className="default-button upload-button" onClick={() => handleFileUpload && handleFileUpload()}>
            Upload File
          </button>
          <button className="default-button clear-button" onClick={() => {/* Clear text area */}}>
            Clear
          </button>
        </div>
      )}

      <div className="tooltip">Search tips
        <span className="tooltiptext">Enter keywords to search for grants or upload a file to analyze grant opportunities.</span>
      </div>
    </div>
  );
}
