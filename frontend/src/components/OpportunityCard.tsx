import { Opportunity } from "../types/apiTypes";
import React, { useState } from 'react';
import { Card, Checkbox, Typography, Accordion, AccordionSummary, AccordionDetails, CardHeader } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export interface OpportunityCardProps {
  opportunity: Opportunity;
}

export default function OpportunityCard({ opportunity, onCheckboxChange }: OpportunityCardProps & { onCheckboxChange: (opp: Opportunity, isChecked: boolean) => void }) {
  const [isOpen, setIsOpen] = useState(false);
  const [isChecked, setIsChecked] = useState(false);

  const toggleCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIsChecked(e.target.checked);
    // Call the passed callback with the opportunity ID and the checked state
    onCheckboxChange(opportunity, e.target.checked);
  };

  // Separate the concerns by having the title only control the description
  const toggleDescription = () => {
    setIsOpen(!isOpen);
  };

  return (
    <Card raised sx={{ maxWidth: 1200, marginBottom: 2, width: '100%' }}>
      <CardHeader
        action={
          <Checkbox
            checked={isChecked}
            onChange={toggleCheckbox}
            id={`checkbox-${opportunity.OpportunityID}`}
          />
        }
        title={<Typography variant="subtitle1" noWrap>{opportunity.OpportunityTitle}</Typography>}
        titleTypographyProps={{ variant: 'body2' }}
      />
      <Accordion expanded={isOpen} onChange={toggleDescription}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="body2">View Details</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography variant="caption">{opportunity.Description}</Typography>
        </AccordionDetails>
      </Accordion>
    </Card>
  );
}

