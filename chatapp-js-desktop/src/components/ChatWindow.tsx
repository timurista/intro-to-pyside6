import React from "react";
import { observer } from "mobx-react";
import ReactMarkdown from "react-markdown";
import { AiOutlineDelete } from "react-icons/ai"; // Import the delete icon
import { rootStore } from "../stores/RootStore";

import "github-markdown-css";

interface MessageItemProps {
  content: string;
  className: string;
  onDelete: () => void;
}

const MessageItem: React.FC<MessageItemProps> = ({
  content,
  className,
  onDelete,
}) => {
  return (
    <div
      className={`flex justify-between items-start p-2 m-2 markdown-body rounded-md shadow-md text-black ${className}`}
    >
      <div className="text-left react-markdown flex-grow">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
      {onDelete && (
        <button
          onClick={onDelete}
          className="text-red-500 ml-2 hover:bg-red-200 p-1 rounded"
        >
          <AiOutlineDelete size={24} />
        </button>
      )}
    </div>
  );
};
export const ChatWindow: React.FC = observer(() => {
  const { chatHistory, deleteFromHistory } = rootStore.aiAgentStore;

  return (
    <div className="bg-gray-100 p-4 rounded-md overflow-y-auto h-96">
      {chatHistory.map((message, index) =>
        message.sender === "human" ? (
          <MessageItem
            key={index}
            content={message.content}
            className="bg-blue-200"
            onDelete={() => deleteFromHistory(index)}
          />
        ) : (
          <MessageItem
            key={index}
            content={message.content}
            className="bg-gray-300"
            onDelete={() => deleteFromHistory(index)}
          />
        )
      )}
    </div>
  );
});

export default ChatWindow;
