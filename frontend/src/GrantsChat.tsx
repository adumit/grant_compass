import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './grantsPage.css';
import { Opportunity } from './types/apiTypes';


interface Message {
  type: 'user' | 'bot';
  text: string;
}

type GrantsPageState = {
  selectedOpportunities: Opportunity[];
};

export default function GrantsPage() {
  const location = useLocation();
  const { selectedOpportunities } = location.state as GrantsPageState || { selectedOpportunities: [] };
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState<Array<Message>>([]);

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;

    const newUserMessage: Message = { type: 'user', text: chatInput };
    setMessages(prevMessages => [...prevMessages, newUserMessage]);

    setChatInput('');

    // Simulate a response
    setTimeout(() => {
      const newBotMessage: Message = { type: 'bot', text: "Here's the information about the grant..." };
      setMessages(prevMessages => [...prevMessages, newBotMessage]);
    }, 1500);
  };

  return (
    <div className="grants-page" style={{ display: 'flex', padding: '20px' }}>
      <div className="selected-grants" style={{ flex: 1, marginRight: '20px' }}>
        {/* Map through the selected opportunities and display them */}
        <ul>
          {selectedOpportunities.map(opportunity => (
            <li key={opportunity.OpportunityID}>{opportunity.OpportunityTitle}</li>
          ))}
        </ul>
      </div>
      <div className="chat-interface" style={{ flex: 1 }}>
        {/* Chat messages */}
        <div className="messages" style={{ height: '300px', overflowY: 'auto' }}>
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              {message.text}
            </div>
          ))}
        </div>
        {/* Chat input */}
        <div className="chat-input" style={{ marginTop: '20px' }}>
          <input
            type="text"
            value={chatInput}
            onChange={e => setChatInput(e.target.value)}
            placeholder="Type here"
            style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}
