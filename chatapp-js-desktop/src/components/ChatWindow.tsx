import React from "react";
import { observer } from "mobx-react";
import { rootStore } from "../stores/RootStore";
import { HumanMessageItem } from "./HumanMessageItem";
import { AIMessageItem } from "./AIMessageItem";

export const ChatWindow: React.FC = observer(() => {
  const { chatHistory } = rootStore.aiAgentStore;

  return (
    <div className="bg-gray-100 p-4 rounded-md overflow-y-auto h-96">
      {chatHistory.map((message, index) =>
        message.sender === "human" ? (
          <HumanMessageItem key={index} content={message.content} />
        ) : (
          <AIMessageItem key={index} content={message.content} />
        )
      )}
    </div>
  );
});

export default ChatWindow;
