import { Opportunity } from "./types/apiTypes";
import React, { useState } from 'react';

export interface OpportunityCardProps {
  opportunity: Opportunity;
}

export default function OpportunityCard({ opportunity }: OpportunityCardProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isChecked, setIsChecked] = useState(false);

  const toggleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIsChecked(e.target.checked);
  };

  // Separate the concerns by having the title only control the description
  const toggleDescription = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`opportunity-card ${isOpen ? 'open' : ''}`}>
      <div className="card-header">
        {/* Checkbox is now a standalone input with its own click handler */}
        <input
          type="checkbox"
          className="opportunity-checkbox"
          id={`checkbox-${opportunity.OpportunityID}`}
          checked={isChecked}
          onChange={toggleCheckbox}
        />
        {/* The label is for the checkbox and should only describe it, not contain any other interactive elements */}
        <label htmlFor={`checkbox-${opportunity.OpportunityID}`} className="opportunity-checkbox-label" />
        {/* The title is now a separate element that can be clicked to toggle the description without affecting the checkbox */}
        <div className="opportunity-title" onClick={toggleDescription}>
          {opportunity.OpportunityTitle}
        </div>
      </div>
      {isOpen && (
        <div className="opportunity-body">
          <p className="opportunity-description">{opportunity.Description}</p>
        </div>
      )}
    </div>
  );
}

