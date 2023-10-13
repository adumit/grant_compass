export class Opportunity {
  "OpportunityID": string;
  "OpportunityTitle": string;
  "Description": string;
}

export class SearchResponse {
  "Top matches": Opportunity[];
}
