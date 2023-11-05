import { useLocation } from 'react-router-dom';
import { Opportunity } from './types/apiTypes';

export default function GrantsPage() {
    const location = useLocation();
    const state = location.state as { selectedOpportunities: Array<Opportunity> };
    const selectedOpportunities = state?.selectedOpportunities || [];
  
    return (
      <div>
        <h1>Selected Grants</h1>
        <ul>
            {selectedOpportunities.map((opp) => (
                <li key={opp.OpportunityID}>{opp.OpportunityTitle}</li>
            ))}
        </ul>
      </div>
    );
  }