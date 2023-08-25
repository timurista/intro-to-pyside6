import React from "react";
import { observer } from "mobx-react";
import { rootStore } from "../stores/RootStore";
import DocumentHistory from "./DocumentHistory";

const ChatInput: React.FC = observer(() => {
  const { input, setInput, clearInput } = rootStore.userInputStore;
  const { addHumanMessage, isAIResponding, chatHistory, documentHistory } =
    rootStore.aiAgentStore;

  const handleSendMessage = async () => {
    await addHumanMessage(input);
    clearInput();
  };

  return (
    <div className="mt-4 flex">
      <textarea
        className="flex-grow border p-4 rounded-l-md resize-y overflow-y-auto"
        rows={4}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message or upload a document..."
      ></textarea>
      <div className="flex flex-col justify-between ml-2">
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-r-md mb-2"
          onClick={handleSendMessage}
        >
          Send
        </button>
        {isAIResponding && (
          <button
            className="bg-red-500 text-white px-4 py-2 rounded-md mb-2"
            onClick={rootStore.aiAgentStore.cancelAIResponse}
          >
            Stop AI Response
          </button>
        )}
        <DocumentHistory />
        {chatHistory.length > 0 || documentHistory.length > 0 ? (
          <button
            className="bg-green-500 text-white px-4 py-2 rounded-md"
            onClick={rootStore.aiAgentStore.clearHistory}
          >
            Clear History
          </button>
        ) : null}
      </div>
    </div>
  );
});

export default ChatInput;
