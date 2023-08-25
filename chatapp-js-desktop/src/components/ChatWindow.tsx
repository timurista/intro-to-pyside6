import React from "react";
import { observer } from "mobx-react";
import { rootStore } from "../stores/RootStore";
import MessageItem from "./MessageItem";

import "github-markdown-css";

export const ChatWindow: React.FC = observer(() => {
  const { chatHistory, deleteFromHistory, editChatMessage } =
    rootStore.aiAgentStore;

  return (
    <div className="bg-gray-100 p-4 rounded-md overflow-y-auto h-96">
      {chatHistory.map((message, index) =>
        message.sender === "human" ? (
          <MessageItem
            key={index}
            content={message.content}
            className="bg-blue-200"
            onDelete={() => deleteFromHistory(index)}
            onEdit={(newContent) => editChatMessage(index, newContent)}
          />
        ) : (
          <MessageItem
            key={index}
            content={message.content}
            className="bg-gray-300"
            onDelete={() => deleteFromHistory(index)}
            onEdit={(newContent) => editChatMessage(index, newContent)}
          />
        )
      )}
    </div>
  );
});

export default ChatWindow;
