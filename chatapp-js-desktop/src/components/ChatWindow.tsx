import React from "react";
import { observer } from "mobx-react";
import ReactMarkdown from "react-markdown";
import { rootStore } from "../stores/RootStore";

import "github-markdown-css";

interface MessageItemProps {
  content: string;
  className: string;
}

const MessageItem: React.FC<MessageItemProps> = ({ content, className }) => {
  return (
    <div
      className={`p-2 m-2 markdown-body rounded-md shadow-md text-black text-left react-markdown ${className}`}
    >
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
};

export const ChatWindow: React.FC = observer(() => {
  const { chatHistory } = rootStore.aiAgentStore;

  return (
    <div className="bg-gray-100 p-4 rounded-md overflow-y-auto h-96">
      {chatHistory.map((message, index) =>
        message.sender === "human" ? (
          <MessageItem
            key={index}
            content={message.content}
            className="bg-blue-200"
          />
        ) : (
          <MessageItem
            key={index}
            content={message.content}
            className="bg-gray-300"
          />
        )
      )}
    </div>
  );
});

export default ChatWindow;
