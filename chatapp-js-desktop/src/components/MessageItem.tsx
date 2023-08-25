// MessageItem.tsx

import React, { useState } from "react";
import {
  AiOutlineDelete,
  AiOutlineEdit,
  AiOutlineSave,
  AiOutlineClose,
  AiOutlineArrowDown,
  AiOutlineArrowUp,
} from "react-icons/ai";
import ReactMarkdown from "react-markdown";
import "./MessageItem.css";

interface MessageItemProps {
  content: string;
  className: string;
  onDelete: () => void;
  onEdit: (content: string) => void;
  defaultExpanded?: boolean;
}

const MessageItem: React.FC<MessageItemProps> = ({
  content,
  className,
  onDelete,
  onEdit,
  defaultExpanded = false,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [editedContent, setEditedContent] = useState(content);

  const tokenCount = content.split(" ").length;

  const handleEdit = () => {
    if (onEdit) onEdit(editedContent);
    setIsEditing(false);
  };

  const expandedClasses = `max-h-32 overflow-hidden relative faded-bottom`;

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
            minHeight: isEditing
              ? tokenCount > 100
                ? "300px"
                : "50px"
              : "auto",
            backgroundColor: "white",
          }}
        />
      ) : (
        <div
          className={`text-left flex-grow w-3/4 react-markdown ${
            !isExpanded ? expandedClasses : "overflow-y-auto"
          }`}
        >
          <div className="text-left text-xs mt-2">{tokenCount} tokens</div>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}

      <div className="flex flex-col justify-between items-end">
        {!isEditing && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-blue-500 ml-2 hover:bg-blue-200 p-1 rounded mb-2"
          >
            {isExpanded ? (
              <AiOutlineArrowUp size={24} />
            ) : (
              <AiOutlineArrowDown size={24} />
            )}
          </button>
        )}
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

export default MessageItem;
