import React, { Suspense } from "react";
import { observer } from "mobx-react";
import { rootStore } from "../stores/RootStore";
// import MessageItem from "./MessageItem";
import GhostLoader from "./GhostLoader";

const MessageItem = React.lazy(() => import("./MessageItem"));

import "github-markdown-css";

export const ChatWindow: React.FC = observer(() => {
  const { chatHistory, deleteFromHistory, editChatMessage } =
    rootStore.aiAgentStore;

  return (
    <div className="bg-gray-100 p-4 rounded-md overflow-y-auto h-96">
      {chatHistory.map((message, index) => (
        <Suspense fallback={<GhostLoader />} key={index}>
          <MessageItem
            content={message.content}
            className={
              message.sender === "human" ? "bg-blue-200" : "bg-gray-300"
            }
            onDelete={() => deleteFromHistory(index)}
            onEdit={(newContent) => editChatMessage(index, newContent)}
            defaultExpanded={index === chatHistory.length - 1}
          />
        </Suspense>
      ))}
    </div>
  );
});

export default ChatWindow;
