import { Opportunity } from "./types/apiTypes";

export interface OpportunityCardProps {
  opportunity: Opportunity;
}

export default function OpportunityCard({opportunity}: OpportunityCardProps) {
  const opportunityUrl = `https://grants.gov/search-results-detail/${opportunity.OpportunityID}`;

  return (
    <li key={opportunity.OpportunityID}>
      <h2>
        <a href={opportunityUrl} target="_blank" rel="noopener noreferrer">
          {opportunity.OpportunityTitle}
        </a>
      </h2>
      <h3>{opportunity.Description}</h3>
    </li>
  );
}
