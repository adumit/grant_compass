import { Opportunity } from "./types/apiTypes";

export interface OpportunityCardProps {
  opportunity: Opportunity;
}

export default function OpportunityCard({opportunity}: OpportunityCardProps) {

  return (
    <li key={opportunity.OpportunityID}>
      <h2>{opportunity.OpportunityTitle}</h2>
      <h3>{opportunity.Description}</h3>
    </li>
  );
}
