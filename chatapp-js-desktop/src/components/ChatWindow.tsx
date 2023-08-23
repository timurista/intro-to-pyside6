import React, { useState } from "react";
import { observer } from "mobx-react";
import ReactMarkdown from "react-markdown";
import {
  AiOutlineDelete,
  AiOutlineEdit,
  AiOutlineSave,
  AiOutlineClose,
} from "react-icons/ai"; // Import the delete icon
import { rootStore } from "../stores/RootStore";

import "github-markdown-css";

interface MessageItemProps {
  content: string;
  className: string;
  onDelete: () => void;
  onEdit: (content: string) => void;
}

const MessageItem: React.FC<MessageItemProps> = ({
  content,
  className,
  onDelete,
  onEdit,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(content);

  const handleEdit = () => {
    if (onEdit) onEdit(editedContent);
    setIsEditing(false);
  };
  return (
    <div
      className={`flex justify-between items-start p-2 m-2 markdown-body rounded-md shadow-md text-black ${className}`}
    >
      {isEditing ? (
        <textarea
          value={editedContent}
          onChange={(e) => setEditedContent(e.target.value)}
          className="flex-grow mr-2 p-1 border rounded-md background-white"
          style={{
            minHeight: "250px",
            backgroundColor: "white",
          }}
        />
      ) : (
        <div className="text-left react-markdown flex-grow">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}

      <div className="flex flex-col justify-between items-end">
        {isEditing ? (
          <>
            <button
              onClick={() => setIsEditing(false)}
              className="text-orange-500 ml-2 hover:bg-orange-200 p-1 rounded mb-2"
            >
              <AiOutlineClose size={24} />
            </button>
            <button
              onClick={handleEdit}
              className="text-green-500 ml-2 hover:bg-green-200 p-1 rounded mb-2"
            >
              <AiOutlineSave size={24} />
            </button>
          </>
        ) : (
          <button
            onClick={() => setIsEditing(true)}
            className="text-blue-500 ml-2 hover:bg-blue-200 p-1 rounded mb-2"
          >
            <AiOutlineEdit size={24} />
          </button>
        )}
        {onDelete && (
          <button
            onClick={onDelete}
            className="text-red-500 ml-2 hover:bg-red-200 p-1 rounded mb-2"
          >
            <AiOutlineDelete size={24} />
          </button>
        )}
      </div>
    </div>
  );
};
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
